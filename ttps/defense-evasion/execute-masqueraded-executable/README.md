# Masquerade as a built-in system executable

## Description
Renames malicious executables to match legitimate Windows system binaries (e.g., svchost.exe, lsass.exe, explorer.exe) to blend with normal system operations. Creates a test executable that masquerades as a system binary in a non-standard location.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **executable_filepath**: File path where the generated executable will be dropped and executed from. The filename should be the name of a built-in system utility. (default: `C:\Users\Public\svchost.exe`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/execute-masqueraded-executable/ttp.yaml \
  --executable_filepath "C:\Temp\explorer.exe"
```

## Steps
1. **create_and_execute_masqueraded_executable**: Uses PowerShell's Add-Type cmdlet to compile a simple C# program that outputs "tweet, tweet" into an executable file at the specified path with a masqueraded name (e.g., svchost.exe), then launches the masqueraded executable using Start-Process.
