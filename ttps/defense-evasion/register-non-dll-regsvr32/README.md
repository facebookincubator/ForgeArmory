# Regsvr32 Registering Non DLL

## Description
Abuses regsvr32.exe to register and execute DLL files renamed with non-standard extensions (.jpg, .png, .txt). Replicates Gozi banking trojan behavior. regsvr32.exe reads file headers, not extensions, allowing disguised DLLs to execute while evading file-type based security controls.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **original_dll_path**: Path to original dll file to rename (default: `C:\Windows\System32\shell32.dll`)
- **renamed_dll_path**: Path to renamed dll file to be registered (default: `C:\Users\Public\shell32.jpg`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/register-non-dll-regsvr32/ttp.yaml \
  --original_dll_path "C:\Windows\System32\comctl32.dll" \
  --renamed_dll_path "C:\Temp\image.png"
```

## Steps
1. **ensure_renamed_dll_exists**: Copies the original DLL file from the system directory to a new location with a non-DLL file extension (e.g., .jpg) to simulate adversary behavior of disguising malicious DLLs.
2. **register_non_dll_file**: Executes regsvr32.exe with the /s (silent) parameter to register the renamed DLL file without displaying any dialog boxes, demonstrating how adversaries can register malicious code with altered file extensions.
