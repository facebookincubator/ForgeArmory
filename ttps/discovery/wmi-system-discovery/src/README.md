## Description:
This script collects and displays various system information, including OS info, CPU info, drive info, hotfix info, local user info, domain user info, recent files, network info, and process info.

## Dependencies:
wmi library (install with `pip install wmi`)

## Usage:
```
python system_info_collector.py
```

## Example Output:
The script will display a formatted output of the collected system information, including:

- OS Info: Computer name, OS name, version, manufacturer, Windows directory, system directory, boot device, and system drive.
- CPU Info: CPU name, manufacturer, number of cores, and number of logical processors.
- Drive Info: List of drives, including device ID, file system, size, and free space.
- HotFix Info: List of installed hotfixes.
- Local User Info: List of local users, including name, domain, SID, account type, and disabled status.
- Domain User Info: Information about the current domain user, including name, domain, SID, account type, and disabled status.
- Recent Files: List of recently accessed files in the user's profile.
- Network Info: Network configuration information, including host name, primary DNS suffix, node type, IP routing enabled, WINS proxy enabled, and DNS suffix search list.
- Process Info: List of running processes, including name, process ID, and parent process ID.

## MITRE Attack Mapping:
- T1082: System Information Discovery (collection of system information, including OS, CPU, and network configuration)
- T1033: System Owner/User Discovery (collection of local user and domain user information)
