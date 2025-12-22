# Adding custom paths for application execution

## Description
Modifies Windows App Paths registry keys to hijack legitimate application names. When users try to launch applications (e.g., msedge.exe), malicious executables run instead. Provides persistence across reboots and evades detection by running under legitimate application names.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **app_name**: path of application to be modified (default: `msedge.exe`)
- **new_path**: New App Path Added (default: `C:\Windows\System32\notepad.exe`)
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/add-custom-path-override/ttp.yaml \
  --app_name "chrome.exe" \
  --new_path "C:\Malware\payload.exe"
```

## Steps
1. **backup_registry**: Exports the current App Paths registry settings for the specified application to a backup file for restoration during cleanup.
2. **modify_app_path**: Modifies the App Paths registry entry for the specified application, redirecting it to execute a different binary instead of the legitimate application.
