# TTP Check For File And Process

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP (Tactic, Technique, and Procedure) connects to a windows host that is running Microsoft Endpoint Defender (MDE).
This TTP checks for the presence of a given file in a given path, and whether a process is running with a given name.
Whether the file should exist or not is parameterized.
The check works within the current drive (expected to be C:).

You can run the TTP using the following example command (adjust arguments as
needed):

```bash
ttpforge run forgearmory//utils/check-for-file-and-process/ttp.yaml --arg path_to_check=ttpforge --arg file_name=dumy.exe --arg should_exist=True
```

Running through BAS CLI:

```bash
bas run --group-id corp_windows forgearmory//utils/check-for-file-and-process/ttp.yaml --arg path_to_check=ttpforge --arg file_name=dumy.exe --arg should_exist=True
```

## Steps

1. **check_parameters**: Checks if the parameters are valid.
2. **check_for_file_existence**: Checks if the file exists or not.
3. **check_for_process_existence**: Checks if the process exists or not.
