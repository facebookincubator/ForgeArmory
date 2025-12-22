# GPP Passwords (findstr)

## Description
Searches for encrypted cpassword values in Group Policy Preference (GPP) XML files within the SYSVOL share. These passwords use weak AES encryption with a published key and can be easily decrypted. Although MS14-025 (2014) prevents new passwords, existing cpasswords in SYSVOL remain vulnerable.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/enumerate-gpp-cpasswords/ttp.yaml
```

## Steps
1. **check_domain_joined**: Verifies that the computer is joined to an Active Directory domain. If the computer is not domain-joined, the test exits with an error since GPP passwords are only relevant in domain environments.
2. **search_gpp_passwords**: Uses findstr to recursively search for the string "cpassword" in all XML files within the SYSVOL share of the domain controller, which is accessible via the %logonserver% environment variable.
