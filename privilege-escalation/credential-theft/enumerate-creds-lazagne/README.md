# enumerate-creds-lazagne

Employ [LaZagne](https://github.com/AlessandroZ/LaZagne) for
extracting credentials stored on disk and in memory of a target system.

## Arguments

- **lazagne_path**: Defines the path where LaZagne will be installed and run.
- **cleanup**: When true, the script attempts to clean the artifacts
  created during the execution of this TTP.

## Pre-requisites

1. The system should have Python3, pip3, and git installed.
1. If LaZagne is not installed, the project will be cloned from its
   GitHub repository.

## Examples

Execute the `LaZagne` tool at a specified path.
Post execution, it cleans up associated artifacts:

```bash
ttpforge -c config.yaml \
    run ttps/privilege-escalation/credential-theft/enumerate-creds-lazagne/enumerate-creds-lazagne.yaml \
    --arg lazagne_path=/tmp/lazagne \
    --arg cleanup=true
```

## Steps

1. **Setup**: Checks for the presence of Python3
   pip3, and git.
   If absent, an error message is displayed and the
   script exits. If present, it checks for LaZagne
   tool at the specified path. If absent, it
   clones the tool from its GitHub repository.

1. **Run LaZagne**: Identifies the operating system
   of the target and runs the LaZagne tool
   accordingly.

1. **Cleanup**: If the `cleanup` argument is set
   to `true`, a cleanup
   script is executed to remove artifacts created
   during script's execution.
