# BitBlt Screen Capture

## Description
This TTP uses the BitBlt API to take a screenshot on a Windows system. It first checks if Go is installed, then builds and executes a Go-based screenshot binary that captures the screen and saves it as a PNG file.

## Arguments
This TTP takes no arguments.

## Requirements
- Platform: Windows
- Go (Golang) must be installed on the system
- Internet connectivity to download the `github.com/kbinani/screenshot` Go module

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//collection/bitblt-screen-capture/ttp.yaml
```

## Steps
1. **check_for_golang**: Checks if Go is installed on the system by running `where go`. Exits with an error if Go is not found.
2. **take_screenshot**: Initializes a Go module, downloads the screenshot dependency, builds the Go screenshot binary, and executes it to capture a screenshot saved as `screenshot.png`. The cleanup step deletes the screenshot file, Go module files, and the compiled binary.
