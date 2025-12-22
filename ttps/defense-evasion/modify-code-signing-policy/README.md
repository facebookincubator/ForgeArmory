# Code Signing Policy Modification

## Description
Modifies Windows code signing policy using bcdedit to enable test signing mode, allowing unsigned or self-signed drivers to load. Requires Secure Boot to be disabled. Once enabled, adversaries can load rootkits and kernel-mode malware with kernel-level privileges.

Adapted from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

## Requirements
1. Administrator/elevated privileges are required to execute this TTP
2. Secure Boot must be disabled for this technique to work properly

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/modify-code-signing-policy/ttp.yaml
```

## Steps
1. **enable_test_signing**: Uses bcdedit (Boot Configuration Data Editor) to enable test signing mode, which allows the system to load unsigned or test-signed drivers and kernel-mode code.
