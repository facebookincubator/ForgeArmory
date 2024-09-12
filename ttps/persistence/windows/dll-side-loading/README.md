# DLL Side-Loading using the Notepad++ GUP.exe binary

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP uses GUP, an open source signed binary used by Notepad++ for software updates that is vulnerable to DLL Side-Loading. This enables the libcurl dll to be loaded and upon execution, calc.exe will be opened.

Derived from [Atomic Red Team T1574.002](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1574.002/T1574.002.md#atomic-test-1---dll-side-loading-using-the-notepad-gupexe-binary)

## Arguments
- **process_name**:  a string flag specifying the name of created calc process. Default is "CalculatorApp".
- **gup_exe**: a path flag specifying location of GUP.exe. Default is "bin\GUP.exe".
- **curl_dll**: a path flag specifying location of libcurl.dll. Default is "bin\libcurl.dll".

## Pre-requisites
- Windows operating system equipped with powershell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//persistence/windows/dll-side-loading/dll-side-loading.yaml
```
```bash
ttpforge run forgearmory//persistence/windows/dll-side-loading/dll-side-loading.yaml --arg process_name=calc
```
```bash
ttpforge run forgearmory//persistence/windows/dll-side-loading/dll-side-loading.yaml --arg gup_exe=bin\myGUP.exe --arg curl_dll=bin\mylibcurl.dll
```

## Steps
1. **execute_GUP** : This step downloads GUP.exe, if not provided, and executes binary
2. **cleanup**: Stops the process for calculator app and delete files that were downloaded

## Manual Reproduction
```bash

#Run bin\GUP.exe (ensure libcurl.dll exist)
bin\GUP.exe

#Stops calculator process
stop-process -name CalculatorApp

```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0003 Persistence / TA0004 Privilege Escalation
- **Techniques**:
    - T1574 Hijack Execution Flow
- **Subtechniques**:
    - T1574.002 DLL Side-Loading
