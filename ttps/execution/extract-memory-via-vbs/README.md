# Extract Memory via VBA

## Description
Demonstrates malware techniques for extracting data from memory using VBA macros in Office documents. The test retrieves a memory pointer to a string and copies its contents to disk, emulating how information stealers and APTs extract credentials, encryption keys, or sensitive data from memory. Direct memory access via pointers bypasses file-based security controls and operates below typical script execution, making detection difficult.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **ms_product**: Maldoc application Word (default: `Word`)
- **invoke_maldoc_script_path**: Path to Invoke-MalDoc.ps1 script (default: `./Invoke-MalDoc.ps1`)
- **macro_file_path**: Path to macro code file (default: `./T1059.005-macrocode.txt`)

## Requirements
1. Microsoft Office (specifically Microsoft Word) must be installed on the system
2. The Invoke-MalDoc.ps1 PowerShell script and macro code file must be present at the specified paths

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/extract-memory-via-vbs/ttp.yaml \
  --invoke_maldoc_script_path "C:\Tools\Invoke-MalDoc.ps1" \
  --macro_file_path "C:\Payloads\memory-extraction-macro.txt"
```

## Steps
1. **check_office_installed**: Verifies that Microsoft Word is installed by attempting to create a Word COM object, then stops any running Word processes to ensure a clean execution environment.
2. **ensure_invoke_maldoc_exists**: Verifies that the Invoke-MalDoc.ps1 PowerShell script exists at the specified path before attempting execution.
3. **ensure_macro_file_exists**: Verifies that the macro code file exists at the specified path before attempting to inject it. If the file is not found, the test exits with an error.
4. **extract_memory_via_vba**: Sets TLS 1.2 as the security protocol, sources the Invoke-MalDoc.ps1 script, and executes the Invoke-Maldoc function with the macro file to inject and execute the memory extraction VBA code within Word, calling the "Extract" subroutine from the macro to perform the memory extraction operation.
