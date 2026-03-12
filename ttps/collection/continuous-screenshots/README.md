# TTP to capture recurring screenshots

## Description
This TTP captures recurring screenshots on a macOS system, simulating how adversaries gather information about system state and user activity through periodic screen captures.

## Arguments
- **interval**: The interval in seconds between each screenshot capture. Default: `2`
- **count**: The count of screenshots to capture. Default: `10`

## Requirements
- macOS (darwin) platform
- Python 3 must be available

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//collection/continuous-screenshots/ttp.yaml --arg interval=5 --arg count=20
```

## Steps
1. **Capturing recurring screenshots**: Executes a Python 3 script (`continuous_screenshots.py`) with the specified interval and count arguments to capture screenshots at regular intervals. Captured screenshots stored in `/tmp/captures` are removed during cleanup.
