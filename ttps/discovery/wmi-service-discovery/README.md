# WMI Service Discovery and Enumeration

## Description
This TTP performs Windows service reconnaissance using Windows Management Instrumentation (WMI) classes. It enumerates all running services and their configurations, analyzes services running with high privileges (LocalSystem, LocalService, NetworkService), identifies potential privilege escalation targets such as unquoted service paths and services outside standard directories, and lists available WMI service methods.

## Arguments
- **filter_privileged_only**: Only show services running as LocalSystem, LocalService, or NetworkService. Default: `false`.

## Requirements
- Platform: Windows
- PowerShell

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//reconnaissance/wmi-service-discovery/ttp.yaml --arg filter_privileged_only=true
```

## Steps
1. **enumerate_all_services**: Queries the `Win32_Service` WMI class to enumerate all Windows services, providing an overview of running, stopped, and paused services, as well as distribution by start mode (automatic, manual, disabled).
2. **analyze_privileged_services**: Analyzes services by privilege level, categorizing them by account type (LocalSystem, LocalService, NetworkService, user accounts) and displaying details of running LocalSystem services.
3. **identify_potential_privilege_escalation_targets**: Identifies services with potential security issues including unquoted service paths with spaces, services running as LocalSystem, services with executables outside standard directories, and services running under user accounts.
4. **enumerate_service_methods**: Lists the available WMI methods for the `Win32_Service` class, highlighting methods useful for service manipulation such as Create, Delete, StartService, StopService, and ChangeStartMode.
