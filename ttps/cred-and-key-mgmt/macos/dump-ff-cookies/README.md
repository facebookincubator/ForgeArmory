# Dump Firefox Cookies

This TTP will simply read from the cookies.json file if Firefox is installed.

## Pre-requisites

1. Firefox must be installed on the system.
1. The user must have necessary permissions to access the Firefox cookies.
1. The TTP must be run on a system that supports JXA (JavaScript for
   Automation), such as macOS.

## Accompanying Code

The JavaScript code (JXA) used in this TTP reads the cookies from the Firefox
cookies.sqlite database and prints the values. It navigates through the
user's Firefox profiles, accessing the cookies.sqlite file to extract
the cookies.

## Examples

You can run the TTP using the following example:

```bash
ttpforge run forgearmory//cred-and-key-mgmt/macos/dump-ff-cookies/dump-ff-cookies.yaml
```

## Steps

1. **dump-cookies**: This step checks if Firefox is installed and if so,
   reads from the cookies.json file. It attempts to kill any running Firefox
   processes and reads from the cookies.sqlite database using a JXA script.

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0006 Credential Access
- **Techniques**:
  - T1539 Steal Web Session Cookie
