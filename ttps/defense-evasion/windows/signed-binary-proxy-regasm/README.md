# Regasm Uninstall Method Call Test

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is designed to execute the Uninstall Method, No Admin Rights Required. Derived from [Atomic Red Team T1218.009](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1218.009/T1218.009.md#t1218009---signed-binary-proxy-execution-regsvcsregasm)

 Upon execution, "I shouldn't really execute either." will be displayed.


## Arguments
- **src_file**: a string variable specifying the location of the CSharp file. Default is $PWD\src\T1218.009.cs

## Pre-requisites
- Windows operating system equipped with powershell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//defense-evasion/windows/signed-binary-proxy-regasm/signed-binary-proxy-regasm.yaml
```
```bash
ttpforge run forgearmory//defense-evasion/windows/signed-binary-proxy-regasm/signed-binary-proxy-regasm.yaml --arg script\script.cs
```

## Steps
1. **execute** : Downloads CSharp file and executes by using Regasm for proxy execution of code
2. **cleanup**: Removes the payload.dll file generated from execute and delete the downloaded CSharp file

## Manual Reproduction
```bash
C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe /r:System.EnterpriseServices.dll /out:"payload.dll" /target:library "src\T1218.009.cs"

C:\Windows\Microsoft.NET\Framework\v4.0.30319\regasm.exe /U payload.dll
```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0005 Defense Evasion
- **Techniques**:
    - T1218 System Binary Proxy Execution
- **Subtechniques**:
    - T1218.009 Regsvcs/Regasm
