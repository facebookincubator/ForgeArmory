## Description:
This script utilizes a Bring Your Own Vulnerable Driver (BYOVD) technique to interact with the vulnerable `TfSysMon` kernel driver. It loads the driver, communicates with it via `DeviceIoControl`, and terminates processes based on the provided target list. The script includes options to specify the driver path, URL, and SHA256 hash for verification. It leverages Windows API functions to control the driver and manage processes.

## Dependencies:

- Custom helper module `helper.py` that defines `WindowsAPIFunctions`

## Usage:
```
python byovd_sysmon.py [options]
```

## Options:
- `--service-name`: Name of the service to load the driver (default: `SysMon`)
- `--driver-path`: Path to the driver file on the local machine (default: `C:\Windows\System32\drivers\sysmon.sys`)
- `--driver-url`: URL to download the driver file (default: `C2/sysmon.sys`)
- `--driver-sha256`: SHA-256 hash of the driver file for integrity verification (default: `1c1a4ca2cbac9fe5954763a20aeb82da9b10d028824f42fff071503dcbe15856`)
- `--device-driver`: Device driver path used for interaction (default: `\\.\TfSysMon`)
- `--duration`: Time in seconds for which the script will run, terminating the specified processes (default: 180 seconds)
- `--targets`: Comma-separated list of process names to terminate (default: key processes associated with security software like `MsMpEng.exe`, `NisSrv.exe`)
- `--debug`: Enable debug logging for detailed information (default: disabled)

## Example:
```
python byovd_sysmon.py --service-name MyService --driver-path C:\path\to\driver.sys --duration 300 --targets MsMpEng.exe,AnotherProcess.exe --debug
```

## MITRE Attack Mapping:
- **T1562.001**: Impair Defenses: Disable or Modify Tools (terminating security processes such as AV or EDR software).

## Additional Information:
- The script must be run with administrator privileges to load and unload drivers.
- Ensure that the specified driver file exists and is accessible, or provide a valid URL for download.
- Custom helper functions are required from `helper.py` (for `WindowsAPIFunctions` and other functionality).
