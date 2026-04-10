# WMI Antivirus Product Discovery

## Description
This TTP performs antivirus product reconnaissance using Windows Management Instrumentation (WMI). It queries the `AntiVirusProduct` class under the `root\SecurityCenter2` namespace to identify installed security products and their current status, checks Windows Defender status through multiple methods, and enumerates installed firewall products.

## Arguments
This TTP takes no arguments.

## Requirements
- Platform: Windows
- PowerShell

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//reconnaissance/wmi-antivirus-discovery/ttp.yaml
```

## Steps
1. **discover_antivirus_products**: Queries the `AntiVirusProduct` WMI class from the `SecurityCenter2` namespace to discover installed antivirus products, displaying their name, GUID, executable paths, product state, and analyzing whether definitions are up to date.
2. **discover_windows_defender_status**: Checks Windows Defender status using three methods: `Get-MpComputerStatus` cmdlet, WMI `MSFT_MpComputerStatus` class, and the `WinDefend` service status. Reports on real-time protection, signature ages, and overall enablement.
3. **discover_firewall_products**: Queries the `FirewallProduct` WMI class from the `SecurityCenter2` namespace to discover installed firewall products and their enablement status.
