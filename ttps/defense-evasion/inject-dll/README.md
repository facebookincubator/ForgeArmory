# DLL Injection

## Description
This TTP shows how an attacker injects malicious code as a DLL into a legitimate process to execute arbitrary code.

## Creating/Compiling your own malicious EXE

### Prerequisites
- Install Visual Studio and a C++ workload or for command-line toolset only, install [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)

### Steps
1. Create a new cpp file with the base similar to `inject.cpp` to inject your different DLL into a PE.
2. Compile the EXE using clang - `cl /EHsc /W4 /DUNICODE /D_UNICODE inject.cpp`
3. Create another cpp file with your desired arbitrary code to run. Make sure to refer to this page for understanding the concept of deadlock in DLLs and best practices: https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-best-practices
4. Compile the cpp file into a DLL using clang - `cl /LD mal.cpp` (Make sure to include or exclude any libraries needed if you decide to update the code).
4. Calculate the hash of both the EXE and DLL using `certutil -hashfile <inject.exe/mal.dll> SHA256` and update the YAML file with the hash in the step `Verifying dll/exe file presence and checksum`.
5. Ensure the EXE and DLL are in the same directory as the YAML file before running the TTP.
