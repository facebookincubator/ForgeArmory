# Linux Ransomware Test TTPForge Runner

This repository stores the code for automating a ransomware test on Linux hosts.

## PRE-REQ

1. openssl needs to be installed. This is usually installed on most modern Linux and macOS hosts by default.

## Available TTPs

**Note: clean-up is enabled by default.**
**Note: This can be adjusted by modifying the .yaml file referenced in each TTP**

1. Recursively encrypt a target directory and will append the specified file extension to each encrypted file. Note: set append_extension="" to not append a file extension and keep the filename the same.

- From the root security-ttpcode directory, run:

```bash
ttpforge run forgearmory//impact/simulate-ransomware-event/ttp.yaml --arg file_path="file_path_here" --arg append_extension="add_file_extension_here"
```

Under the hood this TTP first generates a cert key chain (creates ca.pem, ca.csr, and ca.key the the working dir). Then this TTP simply traverses all subdirectories under the directory specified in the file_path argument and uses openssl to encrypt each file found. All encrypted files are written to: $HOME/encrypted-list.txt. This TTP then waits for 30 seconds to decrypt all files listed in the $HOME/encrypted-list.txt file by using the ca.key file created.
