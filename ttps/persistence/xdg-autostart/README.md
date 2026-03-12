# XDG Autostart

## Description

This TTP demonstartes how an attacker can establish persistence at user level using XDG Autostart.

## Creating/Compiling your own malicious file

### Prerequisites

- gcc (Installed by default on most Linux distributions)

### Steps

1. Create your C file that you want to run when user logs into the machine. Replace the contents of `xdg-binary.c` with your code.
2. Ensure the C file and the .desktop file are in the same directory as the YAML file before running the TTP.
