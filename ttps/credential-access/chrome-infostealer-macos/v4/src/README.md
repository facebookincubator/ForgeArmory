## Description
MacOS Chrome InfoStealer Simulation V4 is a Python script designed to simulate the extraction of sensitive information from macOS systems. This version focuses on using native APIs for credential access that enables offline decryption:

1. **User Password Acquisition**:
   - Retrieves the user's password using native macOS Security framework API calls
   - Displays a native password dialog that looks identical to legitimate system prompts
   - Validates the password against the keychain to ensure it's correct

2. **Keychain Database Acquisition**:
   - Copies the user's keychain database to memory
   - Reports the size of the copied keychain database

3. **Chrome Credential Access**:
   - Copies Chrome browser credential files (Cookies, Login Data, Web Data) to memory
   - Optionally zips the files and saves them to disk
   - Supports multiple Chrome profiles with detection and selection capabilities

4. **System Information Gathering**:
   - Executes system commands to gather information about the host
   - Provides hardware information using system_profiler
   - Supports custom command execution for targeted information gathering

## Key Differences from V3

### Native Password Dialog

V4 improves upon V3's password acquisition approach:

- **V3**: Uses osascript (AppleScript) to display a dialog for password entry
- **V4**: Uses native macOS AppKit framework to create a password dialog that looks identical to legitimate system prompts

### Enhanced Social Engineering

The native dialog in V4 provides a more convincing social engineering attack:

- Looks identical to legitimate system password prompts
- Supports custom icons to match the context of the prompt
- Validates the entered password against the keychain to ensure it's correct
- Shows validation errors that match system behavior
- Configurable maximum attempts to prevent lockouts

## Detection Evasion Improvements

### Dialog Appearance Evasion

- **Authentic UI**: The native dialog is visually indistinguishable from legitimate system password prompts, making it much harder for users to identify as malicious
- **Custom Icons**: Supports using system icons (like those from system applications) to enhance legitimacy
- **System Behavior**: Mimics system behavior for incorrect passwords, further enhancing the illusion

### API Usage Evasion

- **Direct Framework Access**: Uses the AppKit and Security frameworks directly through ctypes rather than spawning processes
- **No AppleScript**: Avoids the use of osascript, which is commonly monitored by security tools
- **Low-Level API Calls**: Makes direct calls to Objective-C runtime and Security framework APIs, which are less commonly monitored than higher-level utilities

### Password Validation Technique

- **Keychain Validation**: Uses the Security framework to validate passwords against the keychain
- **Lock/Unlock Cycle**: Temporarily locks the keychain if needed to validate the password
- **Proper Cleanup**: Ensures proper release of resources to avoid detection through resource leaks

## MITRE ATTACK Mapping

- [T1056.002: GUI Input Capture](https://attack.mitre.org/techniques/T1056/002/)
- [T1555.003: Credentials from Web Browsers](https://attack.mitre.org/techniques/T1555/003)
- [T1555.001: Keychain](https://attack.mitre.org/techniques/T1555/001)

## Usage Options

The script provides the following command-line options:

### Core Functionality Options
- `-p`, `--getPassword`: Retrieve user's password using a native system dialog
- `-k`, `--getKeychain`: Copy the user's keychain database to memory
- `-d`, `--diskCopy`: Copy Chrome data files to disk
- `-m`, `--memCopy`: Copy Chrome data files to memory
- `-s`, `--systemInfo`: Run system information commands
- `-c`, `--commands`: Custom system commands to run (use with --systemInfo)

### Profile Options
- `-l`, `--listProfiles`: List available Chrome profiles
- `--profile`: Chrome profile to use (default: Default)
- `-a`, `--allProfiles`: Process all available Chrome profiles

### Dialog Customization Options
- `--promptTitle`: Title for the password prompt dialog (default: 'Authentication Required')
- `--promptText`: Text for the password prompt dialog
- `--iconPath`: Path to an icon file (.icns) to use for the password dialog
- `--noValidate`: Don't validate the password against the keychain
- `--maxAttempts`: Maximum number of password attempts (default: 3)

### Other Options
- `-v`, `--verbose`: Enable verbose logging
- `-o`, `--output`: Specify output file name for disk copies
- `--no-cleanup`: Don't delete files after creating them (for --diskCopy)
- `--network-info`: Run network-related commands (ifconfig, netstat, etc.)
- `--user-info`: Run user-related commands (whoami, id, groups, etc.)

## Examples

### Complete Data Collection
```bash
# Collect all necessary data for offline decryption
python main.py --getPassword --getKeychain --memCopy --allProfiles
```

### Customized Password Prompt
```bash
# Use a custom dialog to trick the user
python main.py --getPassword --getKeychain --memCopy --promptTitle "Software Update" --promptText "macOS needs your password to install important security updates." --iconPath "/System/Library/CoreServices/Software Update.app/Contents/Resources/SoftwareUpdate.icns"
```

### System Information Gathering
```bash
# Collect credentials and system information
python main.py --getPassword --getKeychain --memCopy --systemInfo --network-info --user-info
```

### Advanced Password Options
```bash
# Customize password validation behavior
python main.py --getPassword --maxAttempts 5 --noValidate --getKeychain --memCopy
```

## Offline Decryption Process

With the data collected by this script, an attacker would perform the following offline decryption process:

1. **Decrypt the Keychain Database**:
   - Use a tool like chainbreaker to decrypt the keychain database with the user's password

2. **Extract the Chrome Safe Storage Password**:
   - Search for the "Chrome Safe Storage" entry in the decrypted keychain
   - Extract the password value

3. **Derive the AES Key**:
   - Use the Chrome Safe Storage password to derive the AES encryption key
   - This involves PBKDF2 with specific parameters (iterations=1003, salt="saltysalt", key_length=16)

4. **Decrypt Chrome Credential Files**:
   - Use the derived AES key to decrypt the Chrome credential files
   - Extract cookies, saved passwords, and other sensitive information

## Additional Info

### Constraints/Assumptions

- **Native UI Requirements**: This approach requires the AppKit and Security frameworks to be available
- **Password Validation**: The validation process temporarily locks the keychain, which might be noticeable to the user
- **Icon Files**: Custom icons must be in .icns format and accessible to the script
- **Chrome Profile Detection**: The script detects Chrome profiles by checking for the existence of specific files

## TODO: Future Enhancements

### Data Exfiltration Simulation

Add functionality that simulates exfiltration of the collected data to common messaging applications and services:

- **Messaging Applications**:
  - Telegram: Implement API-based file uploads to Telegram bots/channels
  - Discord: Add webhook-based exfiltration to Discord servers/channels
  - Slack: Simulate data exfiltration via Slack API

- **Cloud Services**:
  - Implement exfiltration to cloud storage services (Dropbox, Google Drive)
  - Add support for anonymous file sharing services
