//go:build mage

/*
Copyright © 2023-present, Meta Platforms, Inc. and affiliates
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/go-playground/validator/v10"
	"github.com/l50/goutils/v2/dev/lint"
	mageutils "github.com/l50/goutils/v2/dev/mage"
	"github.com/l50/goutils/v2/git"
	"github.com/l50/goutils/v2/sys"
	"github.com/xeipuuv/gojsonschema"
	"gopkg.in/yaml.v3"
)

func init() {
	os.Setenv("GO111MODULE", "on")
}

// InstallDeps Installs go dependencies
func InstallDeps() error {
	fmt.Println("Installing dependencies.")

	if err := lint.InstallGoPCDeps(); err != nil {
		return fmt.Errorf("failed to install pre-commit dependencies: %v", err)
	}

	if err := mageutils.InstallVSCodeModules(); err != nil {
		return fmt.Errorf("failed to install vscode-go modules: %v", err)
	}

	return nil
}

func installCommitMsgHook() error {
	// Define the path to the commit-msg hook file
	gitDirPath := filepath.Join(".git", "hooks", "commit-msg")

	// Check if the hook file already exists
	if _, err := os.Stat(gitDirPath); os.IsNotExist(err) {
		fmt.Println("Installing commit-msg pre-commit hook.")
		cmd := "pre-commit"
		args := []string{"install", "--hook-type", "commit-msg"}
		if _, err := sys.RunCommand(cmd, args...); err != nil {
			return err
		}
	} else if err != nil {
		return fmt.Errorf("error checking for commit-msg hook: %v", err)
	}

	return nil
}

// RunPreCommit runs all pre-commit hooks locally
func RunPreCommit() error {
	if err := installCommitMsgHook(); err != nil {
		return err
	}

	fmt.Println("Updating pre-commit hooks.")
	if err := lint.UpdatePCHooks(); err != nil {
		return err
	}

	fmt.Println("Clearing the pre-commit cache to ensure we have a fresh start.")
	if err := lint.ClearPCCache(); err != nil {
		return err
	}

	fmt.Println("Running all pre-commit hooks locally.")
	if err := lint.RunPCHooks(); err != nil {
		return err
	}

	return nil
}

// loadSchema loads and unmarshals the schema from a YAML file.
func loadSchema(schemaPath string) (map[string]interface{}, error) {
	schemaContent, err := os.ReadFile(schemaPath)
	if err != nil {
		return nil, fmt.Errorf("error reading schema file: %v", err)
	}

	var schema map[string]interface{}
	err = yaml.Unmarshal(schemaContent, &schema)
	if err != nil {
		return nil, fmt.Errorf("error unmarshalling schema: %v", err)
	}

	return schema, nil
}

// ValidateYAML checks if a YAML file is compliant with the schema.
func ValidateYAML(schemaPath, filePath string) error {
	// Load the YAML schema
	yamlSchema, err := loadSchema(schemaPath)
	if err != nil {
		return err
	}

	validate := validator.New()

	if filePath == "ttps" {
		err := validateAllYAML(schemaPath, yamlSchema, filePath, validate)
		if err != nil {
			return err
		}
	} else {
		err := inspectAndValidate(filePath, yamlSchema, validate, 0) // Added depth as 0 for initial call
		if err != nil {
			return err
		}
	}

	return nil
}

// validateAllYAML checks if YAML in the repo is compliant with the schema.
func validateAllYAML(schemaPath string, schema map[string]interface{}, searchDir string, validate *validator.Validate) error {
	// Start directory walk to validate each YAML file
	return filepath.WalkDir(searchDir, func(filePath string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}

		// Only consider .yaml files
		if strings.HasSuffix(strings.ToLower(d.Name()), ".yaml") {
			fmt.Printf("Checking: %s\n", filePath)
			fmt.Printf("Validating: %s against the TTPForge schema (%s)\n", filePath, schemaPath)

			return inspectAndValidate(filePath, schema, validate, 0) // Added the depth parameter here
		}

		return nil
	})
}

func inspectAndValidate(filePath string, schema map[string]interface{}, validate *validator.Validate, depth int) error {
	// Check if the file exists
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		return fmt.Errorf("file %s does not exist", filePath)
	}

	fileContent, err := os.ReadFile(filePath)
	if err != nil {
		return fmt.Errorf("error reading file %s: %v", filePath, err)
	}

	var yamlData map[string]interface{}
	err = yaml.Unmarshal(fileContent, &yamlData)
	if err != nil {
		return fmt.Errorf("error unmarshalling file %s: %v", filePath, err)
	}

	// Validate the YAML data against the YAML schema
	err = validateYAMLAgainstSchema(yamlData, schema)
	if err != nil {
		return err
	}

	repoRoot, err := git.RepoRoot()
	if err != nil {
		return fmt.Errorf("failed to get repo root: %v", err)
	}

	// Check for SubTTPSteps and validate referenced files
	if steps, ok := yamlData["steps"].([]interface{}); ok {
		for _, step := range steps {
			if stepMap, ok := step.(map[string]interface{}); ok {
				if ttpPath, ok := stepMap["ttp"].(string); ok {
					// This is a SubTTPStep, so validate the referenced file
					absTtpPath := filepath.Join(repoRoot, "ttps", ttpPath)

					// Check if the referenced TTP file exists
					if _, err := os.Stat(absTtpPath); os.IsNotExist(err) {
						return fmt.Errorf("referenced TTP file %s does not exist", absTtpPath)
					}

					// This is a SubTTPStep, so validate the referenced file
					err = inspectAndValidate(absTtpPath, schema, validate, depth+1)
					if err != nil {
						return err
					}
				}
			}
		}
	}

	// Only print the success message for the top-level invocation
	if depth == 0 {
		fmt.Println("YAML is valid according to the schema.")
	}

	return nil
}

func validateYAMLAgainstSchema(yamlData map[string]interface{}, schema map[string]interface{}) error {
	schemaLoader := gojsonschema.NewGoLoader(schema)
	documentLoader := gojsonschema.NewGoLoader(yamlData)

	result, err := gojsonschema.Validate(schemaLoader, documentLoader)
	if err != nil {
		return err
	}

	if !result.Valid() {
		var errors []string
		for _, desc := range result.Errors() {
			// Append each error to the errors slice
			errors = append(errors, desc.String())
		}
		return fmt.Errorf("this YAML does not match the schema: %s", strings.Join(errors, "; "))
	}

	// Custom validation: Check for "name" property when "ttp" is defined
	if steps, ok := yamlData["steps"].([]interface{}); ok {
		for _, step := range steps {
			if stepMap, ok := step.(map[string]interface{}); ok {
				// Check for the presence of "name" property when "ttp" is defined
				if _, nameExists := stepMap["name"]; !nameExists {
					return fmt.Errorf("the \"name\" property is missing when \"ttp\" is defined in a step")
				}
			}
		}
	}

	return nil
}
