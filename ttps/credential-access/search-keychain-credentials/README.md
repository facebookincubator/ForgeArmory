# Key Search

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP searches for any files at `~/.ssh`, `~/.aws`, `~/.gcloud`,
and `~/.azure`.

## Pre-requisites

1. The user must have the necessary permissions to search for the specified
   files.
1. This TTP is specific to systems that support the Swift language.
1. The code must be executed on a macOS system.
1. The user must have the necessary permissions to access the TCC folder and
   compile Swift code.
1. macOS Developer tools must be installed as the TTP requires Swift. To install
   developer tools:

   ```bash
   xcode-select --install
   ```

## Examples

You can run the TTP using the following example:

```bash
ttpforge run forgearmory//credential-access/search-keychain-credentials/ttp.yaml
```

## Steps

1. **keysearch**: This step compiles and executes the Swift source file for
   this TTP, then searches for any files at the specified paths, including
   ~/.ssh, ~/.aws, ~/.gcloud, and ~/.azure.

## Accompanying Code

The Swift code used in this TTP searches for key-related files at specified
paths and prints the contents if found.

## MITRE ATT&CK Mapping

- **Tactics**:
  - T0006 Credential Access
- **Techniques**:
  - T1552 Unsecured Credentials
- **Sub-techniques**:
  - T1552.001 Unsecured Credentials: Credentials In Files
