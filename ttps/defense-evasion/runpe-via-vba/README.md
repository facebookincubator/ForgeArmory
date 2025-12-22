# RunPE via VBA

## Description
Demonstrates RunPE (process hollowing) via VBA macros in Office documents. Creates a legitimate process in suspended state, unmaps its memory, injects malicious code, and resumes execution. The injected code runs under the legitimate Word process context, evading security monitoring.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **ms_product**: Maldoc application (Word) (default: `Word`)
- **macro_file_path**: Path to macro code file (default: `./T1055.012-macrocode.txt`)
- **invoke_maldoc_path**: Path to Invoke-MalDoc.ps1 script (default: `./Invoke-MalDoc.ps1`)

## Requirements
1. Microsoft Office (specifically Microsoft Word) must be installed on the system
2. The Invoke-MalDoc.ps1 PowerShell script and macro code file must be present at the specified paths

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/runpe-via-vba/ttp.yaml \
  --macro_file_path "C:\Payloads\malicious-macro.txt" \
  --invoke_maldoc_path "C:\Tools\Invoke-MalDoc.ps1"
```

## Steps
1. **check_microsoft_office**: Verifies that Microsoft Word is installed by attempting to create a Word COM object, then stops any running Word processes to ensure a clean execution environment. If Word is not installed, the test exits with an error.
2. **ensure_invoke_maldoc_exists**: Verifies that the Invoke-MalDoc.ps1 PowerShell script exists at the specified path before attempting execution. If the script is not found, the test exits with an error.
3. **ensure_macro_file_exists**: Verifies that the macro code file exists at the specified path before attempting to inject it. If the file is not found, the test exits with an error.
4. **execute_runpe_via_vba**: Sources the Invoke-MalDoc.ps1 script and executes the Invoke-MalDoc function with the specified macro file and office product to inject and execute the RunPE code within the Word process, calling the "Exploit" subroutine from the macro.
