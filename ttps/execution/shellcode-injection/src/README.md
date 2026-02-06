## Description:
This script downloads encrypted shellcode from a specified URL, decrypts it using AES-CBC, and then executes the decrypted shellcode in memory. It utilizes Windows APIs such as `VirtualAlloc`, `RtlMoveMemory`, and `CreateThread` to allocate memory, move the shellcode, and execute it in a new thread in the executing (current) python process.

## Dependencies:
- `pycryptodome` library for AES decryption (install with `pip install pycryptodome`)

## Usage:
```
python shellcode_loader.py
```

### Configuration:
Modify the script to change the AES encryption key, initialization vector (IV), and the URL from which the shellcode is downloaded:
- **AES_KEY**: The AES encryption key (default: `D(G+KbPeShVmYq4t`)
- **AES_IV**: The AES initialization vector (default: `8y/B?E(G+KbPeShV`)
- **URL**: The URL to download the encrypted shellcode from (default: `SLIVERC2/files.woff`)

## Example:
```
python shellcode_loader.py
```

## MITRE Attack Mapping:
- **T1027**: Obfuscated Files or Information (the shellcode is encrypted before being downloaded and executed in memory).
- **T1055**: Process Injection (injecting and executing shellcode in a process using Windows API calls).
- **T1218**: Signed Binary Proxy Execution (leveraging Windows APIs to execute shellcode).

## Additional Information:
- Ensure that the URL points to a valid file containing encrypted shellcode, and that the AES key and IV are correct.
