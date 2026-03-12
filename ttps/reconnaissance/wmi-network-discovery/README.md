# WMI Network Information Discovery

## Description
This TTP performs network reconnaissance using Windows Management Instrumentation (WMI) classes. It enumerates network adapters, checks for virtualization indicators in network hardware, discovers IP configuration details, routing tables, network shares, and network protocols.

## Arguments
- **check_vm_indicators**: Whether to check for virtualization indicators in network hardware. Default: `true`.

## Requirements
- Platform: Windows
- PowerShell

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//reconnaissance/wmi-network-discovery/ttp.yaml --arg check_vm_indicators=false
```

## Steps
1. **enumerate_network_adapters**: Queries the `Win32_NetworkAdapter` WMI class to enumerate all network adapters, displaying name, description, manufacturer, MAC address, adapter type, connection status, and speed.
2. **check_virtualization_indicators**: Analyzes network adapters for VM indicators by checking manufacturer names, adapter names/descriptions, and MAC address prefixes against known virtualization vendors (VMware, VirtualBox, Hyper-V, Xen, QEMU). Skipped if the `check_vm_indicators` argument is set to `false`.
3. **enumerate_network_configuration**: Queries the `Win32_NetworkAdapterConfiguration` WMI class for active network configurations including IP addresses, subnet masks, default gateways, DNS servers, DHCP settings, and MAC addresses.
4. **enumerate_routing_table**: Queries the `Win32_IP4RouteTable` WMI class to enumerate the IP routing table, displaying destinations, masks, next hops, interface indices, metrics, and identifying default routes.
5. **enumerate_network_shares**: Queries the `Win32_Share` WMI class to enumerate network shares, analyzing share types (disk, print queue, IPC, admin) and identifying potentially interesting non-default shares.
6. **enumerate_network_protocols**: Queries the `Win32_NetworkProtocol` WMI class to enumerate available network protocols, displaying delivery guarantees, sequencing, connection orientation, and broadcast/multicast support.
