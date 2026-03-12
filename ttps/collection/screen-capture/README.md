# Screen Capture

## Description
This TTP executes the macOS `screencapture` binary to take a screenshot and save it to a specified file.

## Arguments
- **filename**: Name of the file to save the screenshot to. Default: `foo.jpg`

## Requirements
- macOS (darwin) platform
- `screencapture` binary must be available

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//collection/screen-capture/ttp.yaml --arg filename=screenshot.png
```

## Steps
1. **Screen Capture**: Executes `screencapture` with the specified filename to capture the current screen. The captured file is removed during cleanup.
