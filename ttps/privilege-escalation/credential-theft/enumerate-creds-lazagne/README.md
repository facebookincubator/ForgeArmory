# enumerate-creds-lazagne

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP employs the [LaZagne](https://github.com/AlessandroZ/LaZagne) tool for
extracting credentials stored on disk and in memory of a target system.

## Arguments

- **lazagne_path**: Specifies the path where LaZagne will be installed and run.
  (Default: `/tmp/lazagne`)

## Pre-requisites

1. A system with Python3, pip3, and git installed.
1. If LaZagne is not present on the system, the project will be cloned
   from its GitHub repository.

## Examples

You can execute the TTP using the following examples:

Run the `LaZagne` tool at a specified path. Upon completion, it will clean
up any associated artifacts:

```bash
ttpforge run forgearmory//privilege-escalation/credential-theft/enumerate-creds-lazagne/enumerate-creds-lazagne.yaml
```

[Insert any additional examples here, if necessary.]

## Steps

1. **Setup**: This step verifies the presence of `python3`, `pip3`, and `git`
   on the target system. If any of these tools are missing, it will display an
   error message and exit. If LaZagne isn't found at the specified path, the
   script will clone the tool from its GitHub repository.

1. **Run LaZagne**: During this step, the operating system of the target is
   identified, and the LaZagne tool is executed accordingly.
