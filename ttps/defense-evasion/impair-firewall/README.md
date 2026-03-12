# Temporarily Disable pf

## Description
This TTP temporarily disables the `pf` (packet filter) firewall on macOS by running `pfctl -d`. This simulates an adversary impairing host-based defenses by disabling the system firewall.

## Arguments
- **sleepval**: The number of seconds to sleep before performing cleanup and re-enabling the firewall.

## Requirements
- macOS (darwin) platform
- Root/sudo privileges required
- `pfctl` must be available

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//defense-evasion/impair-firewall/ttp.yaml --arg sleepval=30
```

## Steps
1. **disablepf**: Checks for root privileges and runs `pfctl -d` to disable the pf firewall. During cleanup, the firewall is re-enabled with `pfctl -e` after sleeping for the specified duration.
