# LOTL Ransomware Encryption

![Meta TTP](https://img.shields.io/badge/Meta_TTP-red)

This TTP leverages the `zip` command available on Linux systems to encrypt files in a specified directory, simulating a ransomware attack using tools already present on the machine. The command encrypts the contents of the target directory and requires a password for decryption, illustrating a data encryption impact scenario often used by threat actors.

## Arguments

- **target_dir**: The directory to encrypt.

  Default: /dev/shm

- **encryption_key**: The password used to encrypt the directory.

  Default: password

## Requirements

1. Access to a Linux system where the `zip` and `unzip` commands are available.
2. Permission to modify files within the target directory.

## Examples

You can run the TTP using the following command (adjust arguments as needed):

```bash
ttpforge run forgearmory//impact/simulate-ltol-ransomware/ttp.yaml \
    --arg target_dir="/path/to/target/dir" \
    --arg encryption_key="your_encryption_key"
```

## Steps

1. **encrypt_dir**: Encrypts the specified directory using the provided encryption key. The directory is compressed into a zip file, which is encrypted with the password.

   ```bash
   zip -r -P {{ .Args.encryption_key }} ttpforge.zip {{ .Args.target_dir }}
   ```

1. **cleanup**: Attempts to restore the original state by decrypting and unzipping the encrypted directory.

   ```bash
   unzip -o -P {{ .Args.encryption_key }} ttpforge.zip
   ```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0040 Impact
- **Techniques**:
  - T1486 Data Encrypted for Impact
