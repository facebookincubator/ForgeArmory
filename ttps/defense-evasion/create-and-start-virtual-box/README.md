# Create and Start VirtualBox virtual machine

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP is designed to create a simple VirtualBox VM and start up the machine. The cleanup command stops and deletes the newly created VM, associated files, and uninstalls virtual box if it was installed. Derived from [Atomic Red Team T1564.006](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1564.006/T1564.006.md#atomic-test-2---create-and-start-virtualbox-virtual-machine)

## Arguments
- **vm_name**: a string variable specifying the name of the new virtual machine. Default: "TTP VM"
- **vb_exe**: a string variable specifying the path to the VirtualBox executable. Default: "$PWD\bin\VirtualBox\VirtualBox.exe"
- **vb_manage**: a string variable specifying the path to the Path to the executable for VBoxManage, the command-line interface to VirtualBox. Default: "$PWD\bin\VirtualBox\VBoxManage.exe"
- **vb_download**: a string variable specifying the URL of the installer for VirtualBox. Default: "https://download.virtualbox.org/virtualbox/6.1.32/VirtualBox-6.1.32-149290-Win.exe"
- **vb_installer**: a string variable specifying the Executable for the Virtualbox installer. Default: "VirtualBox-6.1.32-149290-Win.exe"

Other Virtual Box Versions: https://download.virtualbox.org/virtualbox

## Pre-requisites
- Windows operating system equipped with powershell

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//defense-evasion/create-and-start-virtual-box/ttp.yaml
```
```bash
ttpforge run forgearmory//defense-evasion/create-and-start-virtual-box/ttp.yaml --arg vm_name="Forge VM"
```
```bash
ttpforge run forgearmory//defense-evasion/create-and-start-virtual-box/ttp.yaml --arg vb_exe=C:\Program Files\Oracle\VirtualBox\VirtualBox.exe --arg vb_manage=C:\Program Files\Oracle\VirtualBox\VBoxManage.exe
```
```bash
ttpforge run forgearmory//defense-evasion/create-and-start-virtual-box/ttp.yaml --arg vb_download="https://download.virtualbox.org/virtualbox/7.0.20/VirtualBox-7.0.20-163906-Win.exe" --arg vb_installer=VirtualBox-7.0.20-163906-Win.exe
```
## Steps
1. **setup_and_start_virtual_box** : Downloads Virtual Box if not provided and creates and starts a vm
2. **cleanup**: Powers off and unregisters the vm created, uninstall Virtual Box if installed, and deletes files that were downloaded

## Manual Reproduction
```bash
    #Create VM
    &"VirtualBox\VBoxManage.exe" createvm --name "TTP VM" --register

    #Register VM
    &"VirtualBox\VBoxManage.exe" modifyvm "TTP VM" --firmware efi

    #Start VM
    &"VirtualBox\VBoxManage.exe" startvm "TTP VM"

    #Power off VM
    &"VirtualBox\VBoxManage.exe" controlvm "TTP VM" poweroff

    #Waiting for VM to power off
    Start-Sleep -Seconds 20

    #Delete VM
    &"VirtualBox\VBoxManage.exe" unregistervm "TTP VM" --delete

```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0005 Defense Evasion
- **Techniques**:
    - T1564 Hide Artifacts
- **Subtechniques**:
    - T1564.006 Run Virtual Instance
