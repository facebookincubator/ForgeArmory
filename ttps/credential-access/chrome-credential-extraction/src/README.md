## Description:
This script extracts Chrome's saved passwords, tokens, and cookies by copying relevant data files (such as `Web Data`, `Login Data`, and `Cookies` files) to a temporary directory. It decrypts the sensitive information using the Windows Data Protection API (DPAPI) and AES-GCM decryption methods. The extracted data can be saved to a file or printed to the console. The script also allows terminating the `chrome.exe` process to unlock the necessary files for extraction.

## Dependencies:
- `pycryptodome` library for AES decryption (install with `pip install pycryptodome`)

## Usage:
```
python chrome_credential_extractor.py [options]
```

## Options:
- `--config`: Path to the configuration file (default: `config.json` in the script's directory).

### Configuration File (JSON Format):
The script uses a configuration file that defines output settings, including the paths for saving the extracted passwords, tokens, and cookies. Example configuration file (`config.json`):
```json
{
  "output": {
    "save_to_file": true,
    "passwords_file": "extracted_passwords.json",
    "tokens_file": "extracted_tokens.json",
    "cookies_file": "extracted_cookies.json"
  }
}
```

## Example:
```
python chrome_credential_extractor.py --config /path/to/config.json
```

## MITRE Attack Mapping:
- **T1555.003**: Credentials from Web Browsers (stealing credentials stored in Chrome).


## Additional Information:
- The `chrome.exe` parent process will be terminated to ensure files can be copied successfully.
- You may need to modify the script or configuration file paths based on the actual Chrome installation directory and the output directory.
- The master key is retrieved from Chrome’s `Local State` file using Windows DPAPI, and this key is used to decrypt the tokens and passwords.
