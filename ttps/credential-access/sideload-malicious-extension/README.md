# Sideload Malicious Chrome Extension

## Description
This TTP drops a modified version of the CookieBro Chrome extension, kills current Chrome windows, and opens a new Chrome window using the `--load-extension` flag to temporarily load the modified extension. The extension browses to the cookie editor which forces a download of the browser cookies as a JSON file, simulating credential theft via browser extension sideloading.

## Arguments
This TTP takes no arguments.

## Requirements
- Platform: Windows
- Google Chrome must be installed
- The modified CookieBro extension files (`com.google.chrome-init` directory) and `DCC.bat` script must be present in the TTP directory

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//credential-access/sideload-malicious-extension/ttp.yaml
```

## Steps
1. **export_cookies**: Copies the modified CookieBro extension to the current user's Downloads directory, then executes a batch script (`DCC.bat`) that closes Chrome, temporarily loads the modified extension to dump cookies, and verifies whether the `cookies.json` file was successfully exported. The cleanup step copies and displays the cookies file, then deletes it along with the extension directory.
