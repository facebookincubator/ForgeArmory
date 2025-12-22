# Encoded VBS code execution

## Description
Demonstrates how adversaries execute encoded VBScript from malicious Office documents to evade static analysis and signature-based detection. VBA macros decode and execute the VBScript payload using the ScriptControl ActiveX object. Upon successful execution, a message box displays "ART T1059.005". Commonly seen in phishing campaigns with weaponized Office documents. Requires 64-bit Microsoft Office due to ScriptControl ActiveX usage.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **invoke_maldoc_script_path**: Path to Invoke-MalDoc.ps1 script (default: `./Invoke-MalDoc.ps1`)
- **macro_file_path**: Path to macro code file (default: `./T1059.005-macrocode.txt`)

## Requirements
1. 64-bit version of Microsoft Office (Word) must be installed on the system. You can validate this by opening WinWord -> File -> Account -> About Word
2. The Invoke-MalDoc.ps1 PowerShell script and encoded macro code file must be present at the specified paths

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/execute-encoded-vbs/ttp.yaml \
  --invoke_maldoc_script_path "C:\Tools\Invoke-MalDoc.ps1" \
  --macro_file_path "C:\Payloads\encoded-macro.txt"
```

## Steps
1. **check_office_64bit**: Verifies that a 64-bit version of Microsoft Word is installed by creating a Word COM object and checking its installation path. If a 32-bit version is detected (path contains "(x86)") or Word is not installed, the test exits with an error.
2. **ensure_invoke_maldoc_exists**: Verifies that the Invoke-MalDoc.ps1 PowerShell script exists at the specified path before attempting execution. If the script is not found, the test exits with an error.
3. **ensure_macro_file_exists**: Verifies that the encoded macro code file exists at the specified path before attempting to inject it. If the file is not found, the test exits with an error.
4. **execute_encoded_vbs**: Sets TLS 1.2 as the security protocol, sources the Invoke-MalDoc.ps1 script, and executes the Invoke-Maldoc function with the encoded macro file to inject and execute the encoded VBScript within Word, calling the "Exec" subroutine from the macro.
