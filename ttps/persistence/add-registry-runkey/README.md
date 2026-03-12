# Registry Run Key Persistence

## Description
This TTP builds a screenshot binary using Go and adds it to the Windows Registry Run Key for persistence. The binary is added to `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnceEx` so that it executes automatically on the next logon. This simulates a common persistence technique used by adversaries.

## Arguments
This TTP takes no arguments.

## Requirements
- Platform: Windows
- Superuser (Administrator) privileges are required
- Go (Golang) must be installed on the system
- Internet connectivity to download Go module dependencies
- The `runkey_persist.bat` script must be present in the TTP directory

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/add-registry-runkey/ttp.yaml
```

## Steps
1. **check_for_golang**: Checks if Go is installed on the system. Exits with an error if Go is not found.
2. **build_binary**: Initializes a Go module, downloads the screenshot dependency, and builds the binary.
3. **add_persistence**: Executes `runkey_persist.bat` to add the binary to the Registry Run Key for persistence. The cleanup step deletes the Go module files, the compiled binary, and removes the Registry Run Key entry.
