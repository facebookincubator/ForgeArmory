# Export Tableau sites

## Description
This TTP runs a sensitive command to export sites on Tableau Server. It invokes the `tsm sites export` help command to simulate access to sensitive Tableau Server management functionality.

## Arguments
This TTP takes no arguments.

## Requirements
1. Tableau Server Manager (`tsm`) CLI must be available on the system.

## Examples
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//collection/export-tableau-sites/ttp.yaml
```

## Steps
1. **run_sensitive_command**: Executes the `tsm sites export --help` command.
