# Disable User Session Actions

## Description
Disables critical user session actions (Change Password, Lock Workstation, Logoff, Shutdown) through registry modifications. Frequently employed by ransomware to trap users and prevent them from securing accounts or shutting down compromised systems.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-user-session-actions/ttp.yaml
```

## Steps
1. **disable_change_password**: Sets DisableChangePassword to 1 in the HKCU Policies\System registry key, preventing users from changing their password.
2. **disable_lock_workstation**: Sets DisableLockWorkstation to 1, preventing users from locking their workstation.
3. **disable_logoff_button**: Sets both NoLogOff and StartMenuLogOff to 1 in the Policies\Explorer registry key, removing logoff options from the Start menu and other UI elements.
4. **disable_shutdown_button**: Sets shutdownwithoutlogon to 0 in HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System, preventing users from shutting down without logging in.
