# macOS TTPForge Runner

This repository stores the code for automating common macOS tactics, techniques, and procedures (TTPs).


## PRE-REQ:

1. macOS Developer tools must already be installed, as several TTPs require swift to be instealled. To install developer tools:

```
xcode-select --install
```

2. For one of the TTPs (swiftspy_exec.yaml execution), Terminal must be granted "Input Monitoring" permissions: 
```
Privay & Security -> Input Monitoring
```

3. For one of the TTPs (dump_cookies.yaml execution), Firefox must be installed.

## Available TTPs:

**Note: clean-up is enabled by default for each TTP. This can be adjusted by modifing the .yaml file referenced in each TTP**

1. Launch a fake authentication prompt using the osascript binary. 

- From the root ForgeArmory directory, run: 

```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/prompt_cli/prompt_cli.yaml
```

2. Launch a fake authentication prompt using the osascript library (API calls).

- From the root ForgeArmory directory, run: 

```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/prompt_api/prompt_api.yaml
```

3. Dump clipboard contents using the osascript binary.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/clipdump_cli/clipdump_cli.yaml
```

4. Dump clipboard contents using NSPasteboard API calls.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/clipdump_api/clipdump_api.yaml
```

5. Search for ssh and cloud credentials on disk.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/keysearch/keysearch.yaml
```

6. Set up launch agent persistence.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/launchagent/launchagent.yaml
```

7. Set up login item persistence.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/loginitem/loginitem.yaml
```

8. Perform a dylib injection.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/injectdylib/injectdylib.yaml
```

9. Copy the user's login keychain to temp.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/copykeychain/copykeychain.yaml
```

10. Local network host enumeration.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/service_discovery/service_discovery.yaml
```

11. Gather system information.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/system_info/system_info.yaml
```

12. Execute the SwiftBelt system enumerator.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/swiftbelt_exec/swiftbelt_exec.yaml
```

13. Set up .zshrc persistence.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/zshrc_persist/zshrc_persist.yaml
```

14. Stealthy TCC Folder Access Check (via API calls).

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/tcc_access_check_api/check.yaml
```

15. Dylib Execution.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/run_dylib/rundylib.yaml
```

16. Read browser (Firefox) cookies.

**Pre-requisite: Firefox is installed**

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/dump_cookies/dump_cookies.yaml
```

17. Check if the screen is locked.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/lockscreen_check/lockscreen_check.yaml
```

18. Remove the com.apple.quarantine attribute.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/remove_quarantine_attrib/remove_attrib.yaml
```

19. Load a dylib using tclsh.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/tcl_load_dylib/tcl_load_dylib.yaml
```

20. Search for aws keys using mdfind.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/mdfind_aws_keys/mdfind_aws_keys.yaml
```

21. List device configuration profile information for the target host.

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/list_config_profiles/list_config_profiles.yaml
```

22. Run the SwiftSpy keylogger (code used from: https://github.com/slyd0g/SwiftSpy)

- From the root ForgeArmory directory, run: 
```
ttpforge run -c ttpforge-repo-config.yaml ttps/macOS/swiftspy_exec/swiftspy_exec.yaml
```
