## Description
MacOS Chrome InfoStealer Simulation V2 is a Python script designed to simulate the extraction of sensitive information from Google Chrome on macOS systems. The script provides comprehensive functionality for credential access and system reconnaissance:

1. **Chrome Credential Access**:
   - Retrieves the Chrome safe storage password using native macOS Security framework API calls
   - Copies Chrome browser credential files (Cookies, Login Data, Web Data) to memory
   - Optionally zips the files and saves them to disk
   - Supports multiple Chrome profiles with detection and selection capabilities

2. **System Information Gathering**:
   - Executes system commands to gather information about the host
   - Provides hardware information using system_profiler
   - Supports custom command execution for targeted information gathering

## Key Improvements Over V1

### Detection Evasion Improvements

- **Command-line Telemetry Evasion**: Bypasses detection mechanisms that monitor command-line arguments by using native API calls instead of the `/usr/bin/security` utility. Security tools like Endpoint Detection and Response (EDR) solutions, command-line logging systems, and SIEM correlation rules often trigger on specific command patterns like `security find-generic-password -ga 'Chrome'`.

- **Process Creation Evasion**: Eliminates the creation of child processes (`security` and `SecurityAgent`), which are commonly monitored by security tools. Process creation events are high-value telemetry sources for security teams, and v2 leaves no trace in process monitoring tools.

- **Behavioral Analysis Evasion**: Many detection tools use behavioral analysis to identify suspicious patterns. The subprocess approach in v1 creates a recognizable pattern (parent-child process relationship with specific arguments) that can be easily fingerprinted by security tools.


## MITRE ATTACK Mapping

- [T1555.003: Credentials from Web Browsers](https://attack.mitre.org/techniques/T1555/003)
- [T1555.001: Keychain](https://attack.mitre.org/techniques/T1555/001)

## Usage Options

The script provides the following command-line options:

### Core Functionality Options
- `-g`, `--getSafe`: Retrieve the Chrome safe storage password using native API
- `-d`, `--diskCopy`: Copy Chrome data files to disk
- `-m`, `--memCopy`: Copy Chrome data files to memory
- `-s`, `--systemInfo`: Run system information commands
- `-c`, `--commands`: Custom system commands to run (use with --systemInfo)

### Profile Options
- `-l`, `--listProfiles`: List available Chrome profiles
- `-p`, `--profile`: Chrome profile to use (default: Default)
- `-a`, `--allProfiles`: Process all available Chrome profiles

### Other Options
- `-v`, `--verbose`: Enable verbose logging
- `-o`, `--output`: Specify output file name for disk copies
- `--no-cleanup`: Don't delete files after creating them (for --diskCopy)
- `--network-info`: Run network-related commands (ifconfig, netstat, etc.)
- `--user-info`: Run user-related commands (whoami, id, groups, etc.)

## Examples

### Chrome Credential Access
```bash
# Basic usage - get safe storage password and copy files to memory
python main.py --getSafe --memCopy

# Use a specific profile
python main.py --getSafe --diskCopy --profile "Profile 1"

# List available profiles
python main.py --listProfiles

# Process all profiles
python main.py --allProfiles --getSafe --memCopy

# Save output to a specific file and keep the file
python main.py --getSafe --diskCopy --output "chrome_data.zip" --no-cleanup
```

### System Information Gathering
```bash
# Get hardware information
python main.py --systemInfo

# Run custom commands
python main.py --systemInfo --commands "uname -a" "ifconfig" "ls -la ~"

# Get network information
python main.py --network-info

# Get user information
python main.py --user-info
```

### Combined Operations
```bash
# Get Chrome credentials and system information
python main.py --getSafe --memCopy --systemInfo --verbose

# Process all profiles and get network information
python main.py --allProfiles --diskCopy --network-info

# Retrieve safe storage password, copy Chrome data files for all profiles to memory
# Retrieve system information and enable verbose logging
python main.py --getSafe --memCopy --allProfiles --systemInfo --verbose
```

## Additional Info

### Constraints/Assumptions

- **Native API Access**: The script uses the macOS Security framework directly, which requires the script to be run on macOS.
- **Chrome Profile Detection**: The script detects Chrome profiles by checking for the existence of specific files. If Chrome changes its file structure in future versions, the profile detection might need to be updated.

## TODO: Future Enhancements

### Data Exfiltration Simulation

A planned enhancement is to add functionality that simulates exfiltration of the collected data to common messaging applications and services:

- **Messaging Applications**:
  - Telegram: Implement API-based file uploads to Telegram bots/channels
  - Discord: Add webhook-based exfiltration to Discord servers/channels
  - Slack: Simulate data exfiltration via Slack API

- **Cloud Services**:
  - Implement exfiltration to cloud storage services (Dropbox, Google Drive)
  - Add support for anonymous file sharing services

- **Stealth Options**:
  - Data chunking to avoid detection of large file transfers
  - Encryption of data before exfiltration
  - Timing controls to simulate realistic exfiltration patterns

This enhancement would provide a more complete simulation of real-world credential theft operations, where attackers not only collect sensitive data but also move it off the compromised system through communication channels that might evade detection.
