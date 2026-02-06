# @nolint

import argparse
import getpass
import os
import socket
import sys
import time
from datetime import datetime

import wmi


def get_os_info():
    try:
        c = wmi.WMI()
        os_info = c.Win32_OperatingSystem()[0]
        return f"""
OS Info:
Computer Name: {os_info.CSName}
OS Name: {os_info.Caption}
Version: {os_info.Version}
Manufacturer: {os_info.Manufacturer}
Windows Directory: {os_info.WindowsDirectory}
System Directory: {os_info.SystemDirectory}
Boot Device: {os_info.BootDevice}
System Drive: {os_info.SystemDrive}
"""
    except Exception as e:
        return f"Error retrieving OS info: {str(e)}"


def get_cpu_info():
    try:
        c = wmi.WMI()
        cpu_info = c.Win32_Processor()[0]
        return f"""
CPU Info:
Name: {cpu_info.Name}
Manufacturer: {cpu_info.Manufacturer}
Cores: {cpu_info.NumberOfCores}
Logical Processors: {cpu_info.NumberOfLogicalProcessors}
"""
    except Exception as e:
        return f"Error retrieving CPU info: {str(e)}"


def get_drive_info():
    try:
        c = wmi.WMI()
        drives = c.Win32_LogicalDisk()
        drive_info = ""
        for drive in drives:
            size = int(drive.Size) if drive.Size else 0
            free_space = int(drive.FreeSpace) if drive.FreeSpace else 0
            drive_info += f"""
Drive: {drive.DeviceID}
File System: {drive.FileSystem}
Size: {size // (1024**3)} GB
Free Space: {free_space // (1024**3)} GB
"""
        return drive_info
    except Exception as e:
        return f"Error retrieving drive info: {str(e)}"


def get_hotfix_info():
    try:
        c = wmi.WMI()
        hotfixes = c.Win32_QuickFixEngineering()
        return "\n".join([f"HotFix ID: {fix.HotFixID}" for fix in hotfixes])
    except Exception as e:
        return f"Error retrieving hotfix info: {str(e)}"


def get_local_user_info():
    try:
        c = wmi.WMI()
        users = c.Win32_UserAccount(LocalAccount=True)
        user_info = ""
        for user in users:
            user_info += f"""
Name: {user.Name}
Domain: {user.Domain}
SID: {user.SID}
Account Type: {user.AccountType}
Disabled: {user.Disabled}
Local Account: {user.LocalAccount}
"""
        return user_info
    except Exception as e:
        return f"Error retrieving user info: {str(e)}"


def get_domain_user_info():
    try:
        # Get the current username
        current_user = getpass.getuser()

        c = wmi.WMI()

        # Query for the current user's domain account information
        query = f"SELECT Name, Domain, SID, AccountType, Disabled, LocalAccount FROM Win32_UserAccount WHERE Name = '{current_user}'"
        users = c.query(query)

        user_info = ""
        for user in users:
            user_info += f"""
Name: {user.Name}
Domain: {user.Domain}
SID: {user.SID}
Account Type: {user.AccountType}
Disabled: {user.Disabled}
Local Account: {user.LocalAccount}
"""
        return user_info
    except Exception as e:
        return f"Error retrieving user info: {str(e)}"


def list_recent_files():
    try:
        recent_folder = os.path.expanduser(
            "~\\AppData\\Roaming\\Microsoft\\Windows\\Recent"
        )
        files = os.listdir(recent_folder)
        file_info = (
            f"Directory of {recent_folder}\t | There are {len(files)} entries\n\n"
        )
        for file in files:
            full_path = os.path.join(recent_folder, file)
            file_stat = os.stat(full_path)
            mod_time = time.strftime(
                "%d %b %Y %H:%M", time.localtime(file_stat.st_mtime)
            )
            if os.path.isdir(full_path):
                file_info += f"{mod_time}  DIR  {file}\n"
            else:
                file_info += f"{mod_time}  {file_stat.st_size}  {file}\n"
        return file_info
    except Exception as e:
        return f"Error listing recent files: {str(e)}"


def get_network_info():
    try:
        c = wmi.WMI()
        net_info = "Windows IP Configuration\n\n"

        computer_system = c.Win32_ComputerSystem()[0]
        network_config = c.Win32_NetworkAdapterConfiguration(IPEnabled=True)[0]

        net_info += f"   Host Name . . . . . . . . . . . . : {computer_system.Name}\n"
        net_info += f"   Primary Dns Suffix  . . . . . . . : {getattr(network_config, 'DNSDomain', '')}\n"
        net_info += f"   Node Type . . . . . . . . . . . . : Hybrid\n"
        net_info += f"   IP Routing Enabled. . . . . . . . : {'Yes' if getattr(network_config, 'IPXMediaType', None) else 'No'}\n"
        net_info += f"   WINS Proxy Enabled. . . . . . . . : {'Yes' if getattr(network_config, 'WINSEnableLMHostsLookup', False) else 'No'}\n"
        net_info += f"   DNS Suffix Search List. . . . . . : {', '.join(getattr(network_config, 'DNSDomainSuffixSearchOrder', []))}\n\n"

        network_adapters = c.Win32_NetworkAdapter()

        for adapter in network_adapters:
            adapter_config = c.Win32_NetworkAdapterConfiguration(Index=adapter.Index)[0]

            adapter_name = getattr(adapter, "NetConnectionID", "") or getattr(
                adapter, "Name", "Unknown Adapter"
            )
            net_info += f"{adapter_name}:\n\n"

            if not getattr(adapter, "NetEnabled", False):
                net_info += (
                    "   Media State . . . . . . . . . . . : Media disconnected\n"
                )

            net_info += f"   Connection-specific DNS Suffix  . : {getattr(adapter_config, 'DNSDomain', 'None')}\n"
            net_info += f"   Description . . . . . . . . . . . : {getattr(adapter, 'Name', '')}\n"
            net_info += f"   Physical Address. . . . . . . . . : {getattr(adapter, 'MACAddress', 'None')}\n"
            net_info += f"   DHCP Enabled. . . . . . . . . . . : {'Yes' if getattr(adapter_config, 'DHCPEnabled', False) else 'No'}\n"
            net_info += f"   Autoconfiguration Enabled . . . . : Yes\n"

            ip_addresses = getattr(adapter_config, "IPAddress", None) or []
            ip_subnets = getattr(adapter_config, "IPSubnet", None) or []

            for i, ip in enumerate(ip_addresses):
                if ":" not in ip:  # IPv4 address
                    net_info += f"   IPv4 Address. . . . . . . . . . . : {ip}"
                    net_info += "(Preferred)\n" if i == 0 else "\n"
                    if i < len(ip_subnets):
                        net_info += (
                            f"   Subnet Mask . . . . . . . . . . . : {ip_subnets[i]}\n"
                        )
                else:  # IPv6 address
                    net_info += f"   IPv6 Address. . . . . . . . . . . : {ip}\n"

            if getattr(adapter, "NetEnabled", False):
                try:
                    link_local = [
                        addr
                        for addr in socket.getaddrinfo(socket.gethostname(), None)
                        if addr[0] == socket.AF_INET6 and addr[4][0].startswith("fe80")
                    ][0][4][0]
                    net_info += f"   Link-local IPv6 Address . . . . . : {link_local}\n"
                except IndexError:
                    pass

            dhcp_lease_obtained = getattr(adapter_config, "DHCPLeaseObtained", None)
            if dhcp_lease_obtained:
                try:
                    lease_obtained = datetime.fromtimestamp(
                        int(dhcp_lease_obtained)
                    ).strftime("%A, %B %d, %Y %I:%M:%S %p")
                    net_info += (
                        f"   Lease Obtained. . . . . . . . . . : {lease_obtained}\n"
                    )
                except (ValueError, OSError, OverflowError):
                    pass

            dhcp_lease_expires = getattr(adapter_config, "DHCPLeaseExpires", None)
            if dhcp_lease_expires:
                try:
                    lease_expires = datetime.fromtimestamp(
                        int(dhcp_lease_expires)
                    ).strftime("%A, %B %d, %Y %I:%M:%S %p")
                    net_info += (
                        f"   Lease Expires . . . . . . . . . . : {lease_expires}\n"
                    )
                except (ValueError, OSError, OverflowError):
                    pass

            default_gateway = getattr(adapter_config, "DefaultIPGateway", None) or []
            if default_gateway:
                net_info += (
                    f"   Default Gateway . . . . . . . . . : {default_gateway[0]}\n"
                )

            dhcp_server = getattr(adapter_config, "DHCPServer", "")
            if dhcp_server:
                net_info += f"   DHCP Server . . . . . . . . . . . : {dhcp_server}\n"

            dns_servers = getattr(adapter_config, "DNSServerSearchOrder", None) or []
            if dns_servers:
                net_info += f"   DNS Servers . . . . . . . . . . . : {dns_servers[0]}\n"
                for dns in dns_servers[1:]:
                    net_info += f"                                       {dns}\n"

            net_info += f"   NetBIOS over Tcpip. . . . . . . . : {'Enabled' if getattr(adapter_config, 'TcpipNetbiosOptions', 0) == 0 else 'Disabled'}\n"

            net_info += "\n"

        return net_info
    except Exception as e:
        return f"Error retrieving network info 3: {str(e)}"


def get_process_info():
    try:
        c = wmi.WMI()
        processes = c.Win32_Process()

        # Sort processes by Name
        sorted_processes = sorted(processes, key=lambda p: p.Name.lower())

        process_info = "Name                        ProcessId ParentProcessId\n"
        process_info += "----                        --------- ---------------\n"

        for process in sorted_processes:
            name = process.Name
            process_id = process.ProcessId
            parent_process_id = process.ParentProcessId

            # Format the output to align with the PowerShell command
            process_info += f"{name:<28} {process_id:<9} {parent_process_id}\n"

        return process_info
    except Exception as e:
        return f"Error retrieving process info: {str(e)}"


MODULES = {
    "os": ("OS Info", get_os_info),
    "cpu": ("CPU Info", get_cpu_info),
    "drive": ("Drive Info", get_drive_info),
    "hotfix": ("HotFix Info", get_hotfix_info),
    "local-users": ("Local User Info", get_local_user_info),
    "domain-users": ("Domain User Info", get_domain_user_info),
    "recent-files": ("Recent Files", list_recent_files),
    "network": ("Network Info", get_network_info),
    "processes": ("Process Info", get_process_info),
}

ALL_MODULE_NAMES = list(MODULES.keys())


def main():
    parser = argparse.ArgumentParser(description="WMI System Information Discovery")
    parser.add_argument(
        "--modules",
        default="all",
        help="Comma-separated list of modules to run, or 'all' "
        "(choices: all," + ",".join(ALL_MODULE_NAMES) + ")",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Write output to file instead of stdout",
    )
    args = parser.parse_args()

    if args.modules == "all":
        selected = ALL_MODULE_NAMES
    else:
        selected = [m.strip() for m in args.modules.split(",")]
        for m in selected:
            if m not in MODULES:
                print(f"Unknown module: {m}", file=sys.stderr)
                print(
                    f"Available modules: {', '.join(ALL_MODULE_NAMES)}", file=sys.stderr
                )
                sys.exit(1)

    output_file = None
    if args.output:
        output_file = open(args.output, "w")

    def out(text):
        if output_file:
            output_file.write(text + "\n")
        else:
            print(text)

    for mod_name in selected:
        label, func = MODULES[mod_name]
        out("=" * 30 + f" {label} " + "=" * 30)
        out(func())

    if output_file:
        output_file.close()


if __name__ == "__main__":
    main()
