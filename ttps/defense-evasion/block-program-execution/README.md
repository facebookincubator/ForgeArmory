# DisallowRun Execution Of Certain Applications

## Description
Modifies Windows Registry to prevent execution of specific applications (security tools, antivirus, registry editors, task managers) using DisallowRun policy. Makes it significantly harder for victims to identify and remove malware by restricting diagnostic and removal tools.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **reg_key**: Registry key to modify (default: `art`)
- **blocked_executable**: Name of the executable to block (default: `regedit.exe`)
- **backup_location**: Path where registry backup will be saved (default: `C:\Users\Public\backup.reg`)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/block-program-execution/ttp.yaml \
  --reg_key "block1" \
  --blocked_executable "taskmgr.exe"
```

## Steps
1. **backup_registry**: Exports the current state of the Explorer Policies registry key to a backup file.
2. **disallow_run_applications**: Modifies the registry to enable the DisallowRun policy (setting it to 1) and adds the specified executable to the DisallowRun list, preventing it from being executed.
