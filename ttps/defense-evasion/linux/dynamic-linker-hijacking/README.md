# Dynamic Linker Hijacking

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP enables the injection of a shared object into a program using LD_PRELOAD.

## Examples
You can run the TTP using the following example (after updating the arguments):
```bash
ttpforge run forgearmory//defense-evasion/linux/dynamic-linker-hijacking/dynamic-linker-hijacking.yaml
```

## Steps

1. **clone-ldpreload**: This step clones the LD_PRELOAD-run-at-load-time repository from GitHub (https://github.com/ProfessionallyEvil/LD_PRELOAD-run-at-load-time). This will checkout commit 665a62aa6d86a38541fa05d15a7309f366584a5e. A cleanup step is also provided to remove the repository post-execution.
2. **compile-binary**: This step compiles the "hello_world" binary target in the cloned repository.
3. **test-binary**: This step tests the "hello_world" binary to confirm it compiled without issues.
4. **create-shared-object**: This step creates a shared object named "inject.so" in the cloned repository.
5. **inject-shared-object**: This step injects the "inject.so" shared object into the "hello_world" program using LD_PRELOAD.

## Manual Reproduction Steps

```
# Escalate privileges to root
sudo su

# Set fwdproxy (if on a devserver)
export https_proxy="fwdproxy:8080"

git clone https://github.com/ProfessionallyEvil/LD_PRELOAD-run-at-load-time.git
cd LD_PRELOAD-run-at-load-time/

# Compile binary target
make hello_world

# Test it to confirm it compiled without issues
./hello_world

# Fix bug in Makefile
sed -i 's/-FPIC/-fPIC/g' Makefile

# Create shared object that we will inject into the hello_world program
make inject.so

# Inject the shared object into the hello_world program
LD_PRELOAD=./inject.so ./hello_world
```

## MITRE ATT&CK Mapping

- **Tactics**:
    - TA0005 Defense Evasion
- **Techniques**:
    - T1574 Hijack Execution Flow
- **Subtechniques**:
    - T1574.006 Hijack Execution Flow Dynamic Linker Hijacking
