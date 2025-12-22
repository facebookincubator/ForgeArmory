# Disable Authentication Security Features

## Description
Disables FIDO authentication and multi-factor authentication (MFA) through registry modifications. Weakens authentication posture, making it easier for attackers to bypass authentication controls and gain unauthorized access.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-authentication-security/ttp.yaml
```

## Steps
1. **disable_fido_authentication**: Modifies the HKLM\SOFTWARE\Policies\Microsoft\FIDO registry key to set AllowExternalDeviceSignon to 0, disabling FIDO external device authentication.
2. **disable_secondary_authentication**: Modifies the HKLM\SOFTWARE\Policies\Microsoft\SecondaryAuthenticationFactor registry key to set AllowSecondaryAuthenticationDevice to 0, disabling multi-factor authentication.
