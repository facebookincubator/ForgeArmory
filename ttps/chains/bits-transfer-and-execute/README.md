# Persist, Download, & Execute

## Description
Uses bitsadmin.exe to download a file via BITS and execute a payload upon transfer completion. The executed file differs from the downloaded one—the download merely triggers execution. This causes the payload (e.g., notepad) to run with svchost.exe as the parent process. BITS jobs persist in the queue for up to 90 days if not removed.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Arguments
- **command_path**: Path of command to execute (default: `C:\Windows\system32\notepad.exe`)
- **bits_job_name**: Name of BITS job (default: `AtomicBITS`)
- **local_file**: Local file path to save downloaded file (default: `C:\Windows\Temp\bitsadmin3_flag.ps1`)
- **remote_file**: Remote file to download (default: `https://raw.githubusercontent.com/redcanaryco/atomic-red-team/dd526047b8c399c312fee47d1e6fb531164da54d/LICENSE.md`)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//chains/bits-transfer-and-execute/ttp.yaml \
  --command_path "C:\Windows\system32\calc.exe" \
  --bits_job_name "MyBitsJob"
```

## Steps
1. **create_and_execute_bits_job**: Creates a BITS job, adds a file for download, sets a notification command to execute when the transfer completes, resumes the job, waits for completion, and then completes the job.
