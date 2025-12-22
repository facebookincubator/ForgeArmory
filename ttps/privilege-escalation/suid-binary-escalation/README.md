# SUID Binary Privilege Escalation

This TTP demonstrates how to use a SUID binary to escalate privileges. If no
parameters outside of the low privileged user are provided, the TTP will create
and execute a vulnerable scenario.

## Arguments

- **low_priv_user**: Low privileged user account to employ for privilege
  escalation. This argument is required
- **target_bin**: Target SUID binary to employ for privilege escalation.
  Defaults to `/usr/bin/vim`.
- **vuln_bin**: Filepath for the vulnerable bin. Defaults to `/usr/bin/vim-vuln`.
- **escalation_params**: Parameters provided to the vulnerable bin to execute
  the privilege escalation. Defaults to `"-c ':silent !sudo whoami' -c 'qa'"`.

## Requirements

- Platforms: Linux, Darwin
- Superuser privileges are required.

## Examples

To execute this TTP with the default parameters, you can use the following command:

```bash
ttpforge run forgearmory//privilege-escalation/suid-binary-escalation/ttp.yaml --arg low_priv_user=demo_user
```

This will attempt to escalate privileges using the default vulnerable
binary `/usr/bin/vim-vuln` and parameters.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0004: Privilege Escalation
- **Techniques**:
  - T1548: Abuse Elevation Control Mechanism
- **Subtechniques**:
  - T1548.001: Abuse Elevation Control Mechanism Setuid and Setgid

## Steps

1. **Create Vulnerable Binary**: Copies the target binary to the specified
  vulnerable binary path.

2. **Introduce Vulnerability**: Sets the SUID bit on the vulnerable binary to
   make it executable with elevated privileges.

3. **Hunt for SUID Binaries**: Searches for SUID binaries in common binary
   directories.

4. **Escalate Privilege**: Uses the vulnerable binary to escalate the
   privileges of the low privileged user and checks if the escalation was
   successful.
