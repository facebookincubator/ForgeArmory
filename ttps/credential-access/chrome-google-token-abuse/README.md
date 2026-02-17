# Chrome Google Token Abuse

This TTP simulates a threat actor abusing a Google Refresh Token to gain access to a user's Google account.

This TTP uses Python scripts that handles all three steps:
1. Retrieve Chrome Safe Storage password by using Terminal command to access encryption key
2. Extracting tokens from Chrome's Web Data file
3. Using tokens to request Google OAuth tokens
4. Formating Google OAuth tokens into valid session cookies allowing MFA bypass without traditional cookie theft

## Arguments
> Note: main.py is the main script that handles the TTP.

> The script is designed to parse several command line arguments that can be used to customize the behavior of the TTP, and the TTP yaml file can also be edited to account for these arguments for automation purposes.

- **output**: Output file for cookies (default: cookies.json)

- **timeout**: Timeout for keychain access in seconds (default: 30)

- **verbose**: Enable verbose logging

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//credential-access/chrome-google-token-abuse/chrome-google-token-abuse.yaml
```

# Steps
1. **grt-abuse**: Retrieve Chrome Safe Storage password by using Terminal command to access encryption key

## Manual Reproduction
```bash

# Runs the python script that extracts tokens from Chrome's Web Data file, uses them to request Google OAuth tokens, and formats them into browser-compatible cookies.

src/main.py --timeout=60 --output=cookies.json --verbose

```

## MITRE ATT&CK Mapping
- **Tactics**:
    - TA0006: Credential Access
- **Techniques**:
    - T1555: Credentials from Password Stores
- **Subtechniques**:
    - T1555.003: Credentials from Web Browsers
    - T1555.001: Keychain
