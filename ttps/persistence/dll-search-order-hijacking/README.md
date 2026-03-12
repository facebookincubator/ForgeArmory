# DLLSearchOrderHijacking
## Description
This TTP shows how an attacker hijacks the DLL search order to execute malicious code. The malicious DLL is found before the legitimate DLL, allowing the attacker to execute arbitrary code which in this case updates the registry to automatically open calculator on startup.
## Context
DLL Search Order Hijacking is a technique used by attackers to execute malicious code by hijacking the DLL search order. This can be done by placing a malicious DLL in a directory that is searched before the directory where the legitimate DLL is present, allowing the attacker to execute arbitrary code.
The search order for DLLs states that the operating system will first search for the DLL in the directory from which the application loaded, then in the system directories. This is exactly what the attacker is exploiting in this TTP. The attacker places a malicious DLL in the same directory as the application (explorer.exe), which is searched before the system directories. This loads the malicious ntshrui.dll before the legitimate ntshrui.dll present in C:\Windows\System32.
## Creating/Compiling your own malicious DLL
#### Prerequisites
- Install Visual Studio and a C++ workload or for command-line toolset only, install [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
#### Steps
1. Create a new cpp file with the arbitrary code you want to execute or use the provided code in the TTP.
2. Compile the cpp file into a DLL using clang - `cl /LD load.cpp advapi32.lib` (Make sure to include or exclude any libraries needed if you decide to update the code).
3. Calculate the hash of the DLL using `certutil -hashfile load.dll SHA256` and update the YAML file with the hash in the step `Verifying dll file presence and checksum`.
4. Ensure the DLL is in the same directory as the YAML file and rename the file ntshrui.dll before running the TTP.
