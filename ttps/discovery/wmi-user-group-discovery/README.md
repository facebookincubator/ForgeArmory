# WMI User and Group Discovery

## Description
This TTP performs user account and group reconnaissance using Windows Management Instrumentation (WMI) classes. It enumerates local user accounts and their security properties, domain user accounts (if applicable), local and domain groups, currently logged-on users, and logon sessions with type analysis.

## Arguments
- **include_domain_accounts**: Include domain accounts and groups in the enumeration (if the system is domain-joined). Default: `true`.

## Requirements
- Platform: Windows
- PowerShell

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//reconnaissance/wmi-user-group-discovery/ttp.yaml --arg include_domain_accounts=false
```

## Steps
1. **enumerate_local_user_accounts**: Queries the `Win32_UserAccount` WMI class to enumerate local user accounts, displaying name, SID, domain, disabled/locked status, and password properties. Performs a security analysis identifying enabled/disabled users, users without password requirements, and users with non-expiring passwords.
2. **enumerate_domain_user_accounts**: Queries the `Win32_UserAccount` WMI class for domain (non-local) user accounts, displaying the first 10 results. Skipped if the `include_domain_accounts` argument is set to `false`.
3. **enumerate_local_groups**: Queries the `Win32_Group` WMI class for local groups, displaying group names, descriptions, and SIDs. Identifies privileged groups such as Administrators, Power Users, Backup Operators, and Remote Desktop Users.
4. **enumerate_domain_groups**: Queries the `Win32_Group` WMI class for domain groups, displaying the first 15 results and highlighting high-privilege domain groups (Domain Admins, Enterprise Admins, etc.). Skipped if the `include_domain_accounts` argument is set to `false`.
5. **enumerate_logged_on_users**: Queries the `Win32_LoggedOnUser` WMI class to enumerate currently logged-on users, parsing domain, username, and logon ID from each session and displaying unique user sessions.
6. **enumerate_logon_sessions**: Queries the `Win32_LogonSession` WMI class to enumerate all logon sessions, grouping them by type (Interactive, Network, Batch, Service, RemoteInteractive, etc.) and displaying recent interactive sessions.
