# WMI Host and OS Information Discovery

## Description
This TTP performs host and operating system reconnaissance using Windows Management Instrumentation (WMI) classes. It gathers system information including computer system details, operating system information, processor specifications, and BIOS data. It also performs virtual machine detection analysis based on hardware indicators such as manufacturer, model, OEM strings, and BIOS information.

## Arguments
This TTP takes no arguments.

## Requirements
- Platform: Windows
- PowerShell

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//reconnaissance/wmi-host-os-discovery/ttp.yaml
```

## Steps
1. **gather_computer_system_info**: Queries the `Win32_ComputerSystem` WMI class to gather computer name, DNS hostname, domain, current user, manufacturer, model, system type, boot state, memory, and OEM strings. Performs VM detection analysis based on manufacturer, model, and OEM string indicators.
2. **gather_operating_system_info**: Queries the `Win32_OperatingSystem` WMI class to gather OS name, version, build number, architecture, install date, last boot time, directories, registered user, organization, serial number, memory usage, and system uptime.
3. **gather_processor_info**: Queries the `Win32_Processor` WMI class to gather processor name, manufacturer, architecture, core counts, clock speeds, and cache sizes. Performs VM detection based on low processor counts.
4. **gather_bios_info**: Queries the `Win32_BIOS` WMI class to gather BIOS manufacturer, name, version, release date, serial number, and SMBIOS version. Performs VM detection based on BIOS manufacturer and version strings.
