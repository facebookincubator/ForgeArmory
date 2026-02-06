## Description
MacOS Chrome InfoStealer Simulation V3 is a Python script designed to simulate the extraction of sensitive information from macOS systems. It provides comprehensive functionality for credential access and system reconnaissance found in most macOS infostealers

1. **User Password Acquisition**:
   - Retrieves the user's password using osascript to display a fake system dialog
   - Simulates a common social engineering technique used by malware
   - Provides customizable dialog title and text for different social engineering scenarios

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

## Key Differences from V1 and V2

### Offline Decryption Approach

V3 simulates a different attack vector compared to V1 and V2:

- **V1**: Uses `/usr/bin/security` command to directly retrieve the Chrome safe storage password
- **V2**: Uses native macOS Security framework API calls to directly retrieve the Chrome safe storage password
- **V3**: Collects the user's password and encrypted keychain database for offline decryption

### Advantages of the V3 Approach

1. **Broader Access**: By obtaining the user's password, an attacker potentially gains access to all keychain items, not just Chrome credentials
2. **Offline Processing**: All decryption can be done offline, reducing the time spent on the compromised system
3. **Evasion**: No direct access to the keychain API is required, potentially evading security monitoring

## MITRE ATTACK Mapping

- [T1056.002: GUI Input Capture](https://attack.mitre.org/techniques/T1056/002/)
- [T1555.003: Credentials from Web Browsers](https://attack.mitre.org/techniques/T1555/003)
- [T1555.001: Keychain](https://attack.mitre.org/techniques/T1555/001)

## Usage Options

The script provides the following command-line options:

### Core Functionality Options
- `-p`, `--getPassword`: Retrieve user's password using a fake system dialog
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
- `--promptTitle`: Title for the password prompt dialog (default: 'System Update Required')
- `--promptText`: Text for the password prompt dialog

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
python main.py --getPassword --getKeychain --memCopy --promptTitle "Adobe Creative Cloud" --promptText "Please enter your password to verify your Adobe subscription."
```

### System Information Gathering
```bash
# Collect credentials and system information
python main.py --getPassword --getKeychain --memCopy --systemInfo --network-info --user-info
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

- **User Interaction**: This approach requires user interaction to enter their password, which may alert them to the attack
- **Social Engineering**: The success rate depends on the effectiveness of the social engineering technique
- **Keychain Access**: The script assumes the user's keychain is accessible and not encrypted with a separate password
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
