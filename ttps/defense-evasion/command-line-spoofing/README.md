# Command Line Spoofing

## Description

This TTP spoofs the process command line as a means to thwart detection. TTP runs a C program compiled binary `spoofer.c` that spoofs the process command line. The C program is compiled using `gcc spoofer.c -o spoofer`. `prctl` is used to update the name of the calling process to `ps` and `strncpy` is to update the program name.

## Creating/Compiling your own malicious file

### Prerequisites

- gcc (Installed by default on most Linux distributions)

### Steps

1. Create your updated c file with the base similar to `spoofer.c`.
2. The program will compile the file using the command - `gcc spoofer.c -o prog`
3. Ensure the .c file is in the same directory as the YAML file before running the TTP.
