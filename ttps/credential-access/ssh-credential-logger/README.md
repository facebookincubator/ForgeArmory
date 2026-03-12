# SSH Credential Logger

## Description

This TTP creates a malicious SSH credential logger on a Linux system. TTP uses a compiled binary that logs the SSH username and password when someone tries to login.

## Creating/Compiling your own malicious executable

### Prerequisites

- gcc (Installed by default on most Linux distributions)
- pam_modules.h & pam_ext.h --> Install using `sudo dnf install pam-devel`

### Steps

1. Create your updated c file with the base similar to `mal_pam.c` to update what to do with the captured credential.
2. Compile the file into .o file using gcc - `gcc -fPIC -fno-stack-protector -c mal_pam.c`
3. Create a shared object file using gcc - `gcc -shared -o mal_pam.so mal_pam.o -lpam`
4. Calculate the hash of the so file using `sha256sum mal_pam.so` and update the YAML file with the hash in the step `checking if malicious file is present`.
5. Ensure the .so file and the .py file are in the same directory as the YAML file before running the TTP.
