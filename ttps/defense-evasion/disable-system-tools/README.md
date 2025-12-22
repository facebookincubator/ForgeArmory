# Disable Windows System Tools

## Description
Disables critical Windows administrative tools (Task Manager, Command Prompt, Registry Editor, Control Panel) through registry modifications. Employed by Agent Tesla malware and other threats to hinder investigation and remediation efforts. Significantly impairs victim's ability to investigate suspicious activity or remove malware.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **backup_location_1**: Path where registry backup 1 will be saved (default: `C:\Users\Public\backup1.reg`)
- **backup_location_2**: Path where registry backup 2 will be saved (default: `C:\Users\Public\backup2.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-system-tools/ttp.yaml \
  --backup_location_1 "C:\Temp\backup1.reg" \
  --backup_location_2 "C:\Temp\backup2.reg"
```

## Steps
1. **disable_taskmgr**: Creates the System registry key if it doesn't exist and sets DisableTaskmgr to 1, preventing users from opening Task Manager.
2. **disable_cmd**: Creates the Windows\System registry key and sets DisableCMD to 1, preventing users from accessing Command Prompt.
3. **disable_registry_tool**: Creates the policies\system registry key and sets DisableRegistryTools to 1, preventing users from opening Registry Editor.
4. **activate_nocontrolpanel**: Sets NoControlPanel to 1 in the Policies\Explorer registry key, preventing users from accessing Control Panel.
