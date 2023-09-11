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
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/go-playground/validator/v10"
	"github.com/l50/goutils/v2/git"
	"github.com/xeipuuv/gojsonschema"
	"gopkg.in/yaml.v3"
)

func init() {
	os.Setenv("GO111MODULE", "on")
}

const maxDepth = 10

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

	// Additional validation for edits
	err = validateEdits(yamlData)
	if err != nil {
		return err
	}

	// Additional validation for args
	err = validateArgs(yamlData)
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

	if depth >= maxDepth {
		return fmt.Errorf("maximum recursion depth reached")
	}

	return nil
}

func validateYAMLAgainstSchema(yamlData map[string]interface{}, schema map[string]interface{}) error {
	schemaStr, err := json.Marshal(schema)
	if err != nil {
		return fmt.Errorf("error converting schema to string: %v", err)
	}

	schemaLoader := gojsonschema.NewStringLoader(string(schemaStr))
	documentLoader := gojsonschema.NewGoLoader(yamlData)

	result, err := gojsonschema.Validate(schemaLoader, documentLoader)
	if err != nil {
		return err
	}

	if !result.Valid() {
		var errors []string
		for _, desc := range result.Errors() {
			// Append each error to the errors slice
			errors = append(errors, fmt.Sprintf("%s (field: %s)", desc.String(), desc.Field()))
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

func validateEdits(yamlData map[string]interface{}) error {
	steps, ok := yamlData["steps"].([]interface{})
	if !ok {
		return nil
	}

	for _, step := range steps {
		stepMap, ok := step.(map[string]interface{})
		if !ok {
			continue
		}

		// Check if this is an EditStep
		if _, exists := stepMap["edit_file"]; exists {
			edits, ok := stepMap["edits"].([]interface{})
			if !ok {
				return fmt.Errorf("edits is not a valid array")
			}

			for _, edit := range edits {
				editMap, ok := edit.(map[string]interface{})
				if !ok {
					return fmt.Errorf("an edit item is not valid")
				}

				// Check if the required fields are present
				if _, exists := editMap["old"]; !exists {
					return fmt.Errorf("an edit item is missing the 'old' field")
				}

				if _, exists := editMap["new"]; !exists {
					return fmt.Errorf("an edit item is missing the 'new' field")
				}
			}
		}
	}

	return nil
}

func validateArgs(yamlData map[string]interface{}) error {
	args, ok := yamlData["args"].([]interface{})
	if !ok {
		return nil
	}

	for _, arg := range args {
		argMap, ok := arg.(map[string]interface{})
		if !ok {
			return fmt.Errorf("an argument item is not valid")
		}

		// Check if the required fields are present
		if _, exists := argMap["name"]; !exists {
			return fmt.Errorf("an argument item is missing the 'name' field")
		}
	}

	return nil
}
