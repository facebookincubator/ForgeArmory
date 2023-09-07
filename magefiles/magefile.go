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

	"github.com/facebookincubator/ttpforge/pkg/blocks"
	"github.com/go-playground/validator/v10"
	"github.com/l50/goutils/v2/dev/lint"
	mageutils "github.com/l50/goutils/v2/dev/mage"
	"github.com/l50/goutils/v2/sys"
	"gopkg.in/yaml.v2"
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

// ValidateAllYAMLFiles checks if YAML in the repo is compliant with the schema.
func ValidateAllYAMLFiles(schemaPath, searchDir string) error {
	// Load the schema first
	schemaContent, err := os.ReadFile(schemaPath)
	if err != nil {
		return fmt.Errorf("error reading schema file: %v", err)
	}

	var schema blocks.TTP
	err = yaml.Unmarshal(schemaContent, &schema)
	if err != nil {
		return fmt.Errorf("error unmarshalling schema: %v", err)
	}

	validate := validator.New()

	// Start directory walk to validate each YAML file
	return filepath.WalkDir(searchDir, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}

		// Only consider .yaml files
		if strings.HasSuffix(strings.ToLower(d.Name()), ".yaml") {
			fmt.Printf("Checking: %s\n", path)
			return inspectAndValidate(path, schema, validate)
		}

		return nil
	})
}

func inspectAndValidate(filePath string, schema blocks.TTP, validate *validator.Validate) error {
	fileContent, err := os.ReadFile(filePath)
	if err != nil {
		return fmt.Errorf("error reading file %s: %v", filePath, err)
	}

	var ttp blocks.TTP
	err = yaml.Unmarshal(fileContent, &ttp)
	if err != nil {
		return fmt.Errorf("error unmarshalling file %s: %v", filePath, err)
	}

	if err = validate.Struct(ttp); err != nil {
		for _, err := range err.(validator.ValidationErrors) {
			fmt.Printf("Error in %s - Field: %s, Tag: %s, ActualTag: %s, Value: %v\n",
				filePath, err.Field(), err.Tag(), err.ActualTag(), err.Value())
		}
		return fmt.Errorf("file %s does not conform to the schema", filePath)
	}

	return nil
}
