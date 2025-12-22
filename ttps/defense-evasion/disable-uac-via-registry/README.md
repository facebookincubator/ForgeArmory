# Disable UAC via registry

## Description
Completely disables UAC through registry modifications (EnableLUA to 0, ConsentPromptBehaviorAdmin to 0). Observed in MedusaLocker, Purple Fox Rootkit, and Avaddon Ransomware. Enables privileged operations without security prompts.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/disable-uac-via-registry/ttp.yaml
```

## Steps
1. **disable_uac_registry**: Modifies the EnableLUA registry key in HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System, setting it to 0 to completely disable UAC.
2. **disable_uac_consent_prompt**: Sets the ConsentPromptBehaviorAdmin property to 0, disabling the UAC consent prompt for administrators.
