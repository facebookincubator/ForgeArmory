# Sideload Malicious Chrome Extension

> **NOTE:** Google has officially removed the `--load-extension` flag from Chrome 137+. This TTP will not work on Chrome 137 or later. See: https://github.com/cypress-io/cypress/issues/31690

This TTP demonstrates how an attacker can sideload a malicious browser extension to exfiltrate cookies from a victim's browser. The extension presents itself as a browsing history viewer but also contains capabilities to exfiltrate cookies to a C2 server via Telegram.

The TTP performs the following steps:
  1. Kills any running Chrome instances
  2. Launches Chrome with the modified malicious extension
  3. The malicious extension will automatically exfiltrate cookies to telegram messenger every hour

## Arguments
- **extension**: string variable specifying the browser extension to load for cookie extraction (default: "history")

- **wait_time**: int variable specifying time to wait (in seconds) before closing the browser, allowing the extension time to dump the cookie.json file. (default: 7)

- **auto_cleanup**: Automatically close Chrome after execution. Wait for the specified time and then closes Chrome also removing non-persistent extension files that were loaded (default: false)

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//credential-access/sideload-chrome-extension/sideload-chrome-extension.yaml
```

```bash
ttpforge run forgearmory//credential-access/sideload-chrome-extension/sideload-chrome-extension.yaml --arg wait_time=5 --arg auto_cleanup=true
```

```bash
ttpforge run forgearmory//credential-access/sideload-chrome-extension/sideload-chrome-extension.yaml --arg extension=history
```


# Steps
1. **prepare_and_load_extension**: Kill any running Chrome instances and launch Chrome with the specified malicious extension

2. **cleanup_browser**: (optional) Wait for the specified time and then close Chrome cleaning up any non-persistent extension files that were loaded

## Manual Reproduction
```bash
# Kill any running Chrome instances
pkill -i "Google Chrome" || true

# Launch Chrome with the malicious extension
open -a "Google Chrome" --args --load-extension=$(pwd)/src/history --restore-last-session

# Kill any running Chrome instances for cleanup
pkill -i "Google Chrome" || true

```

## MITRE ATT&CK Mapping
- **Tactics**:
    - TA0006: Credential Access
- **Techniques**:
    - T1539: Steal Web Session Cookie
