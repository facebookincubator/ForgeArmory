# TTP Development

This document introduces concepts to help developers 
create their own TTPs for use in TTPForge.

## TTP Anatomy

ForgeArmory TTPs are designed to be consumed by [TTPForge](https://github.com/facebookincubator/TTPForge), which provides an interface to execute TTPs across various targets and mediums. Each ForgeArmory TTP consists of metadata, optional argument declarations, and steps, which define the TTP implementation logic.

### Metadata

TTP metadata must include the name of the TTP and a description of that TTP's 
behavior. MITRE ATT&CK IDs are optional but recommended. If the TTP cannot be 
mapped to MITRE ATT&CK then the `mitre` mapping and its child mappings should be 
omitted.

An example of TTP metadata is shown below.
```text
---
name: Disable system security updates
description: |
  This TTP disables the automatic installation of macOS security updates.
mitre:
  tactics:
    - T0005 Defense Evasion
  techniques:
    - T1562 Impair Defenses
  subtechniques:
    - "T1562.001 Impair Defenses: Disable or Modify Tools"

```

### Arguments

Arguments are defined after the TTP metadata. Arguments are uniquely named, 
may be strongly typed, and may contain default values. Using an argument in 
the TTP is done with the argument syntax, `{{ .Args.arg_name }}`. 
A complete example is shown below.

```yaml
args:
  - name: a_message
  - name: a_number
    type: int
  - name: has_a_default
    default: this is the default value
steps:
  - name: print_args
    inline: |
      echo "hi! You passed the message: {{ .Args.a_message }}"
      echo "You passed the number: {{ .Args.a_number }}"
      echo "has_a_default has the value: '{{ .Args.has_a_default }}'"
```

### Steps

Steps are uniquely named blocks of implementation logic which are executed in sequence. Steps help developers organize and manage the complexity of TTPs.

In general, steps will fall into one of the following high-level categories;

- Assessment
- Shaping
- Execution
- Cleanup

Additionally, TTPs may be daisy-chained enabling developers to create complex sequences of TTPs. In doing so, each daisy-chained TTP is represented in the parent TTP as a sub-TTP. We'll see an example of this shortly and some recommendations on developing sub-TTPs as common building blocks.

#### Assessment

It is often necessary for a TTP to test execution requirements, such as whether a necessary environment variable is set, and bail out of the TTP if it is not. In this example, if the `AWS_DEFAULT_REGION` environment variable is not set then the TTP returns exit code 1 and no further blocks are executed.

```text
steps:
  - name: ensure-aws-creds-present
    inline: |
      set -e

      if [[ -z "${AWS_DEFAULT_REGION}" ]]; then
          echo "Error: AWS_DEFAULT_REGION must be set."
          exit 1
      fi
    
	<- snip ->
```

When creating assessment type blocks, it's preferable to place each test in its own block rather than a single block that tests all prerequisites. This will make your TTPs much easier to maintain as they become more complex.
#### Shaping

It is often necessary for a TTP to install dependencies, stage files, or otherwise shape the target environment prior to executing the core TTP logic.  As with assessment type blocks, when creating shaping type blocks, it's preferable to place each action in its own block.

```yaml
<- snip ->

  - name: setup
    inline: |
      set -e

      if [[ -d "{{ .Args.eiam_path }}" ]]; then
          echo "Info: enumerate-iam already present on the current system"
      else
          git clone https://github.com/andresriancho/enumerate-iam.git {{ .Args.eiam_path }}
      fi

<- snip ->
```

#### Execution

The execution blocks contain the core TTP logic. A single execution block may be sufficient for simple TTPs such as atomics, which contain a single procedure. For complex TTPs, the core logic should be broken up across multiple steps or sub-TTPs. In general, if the core logic implements multiple procedures or the procedure can be reasonably broken up into smaller steps, then refactoring the code into smaller steps will make it easier to maintain.

Code that is likely to be reused in other TTPs should be placed in a sub-TTP and imported where needed. It's much easier to maintain building blocks than to change the same (reimplemented) code in multiple places. Some good candidates for sub-TTPs include assessment and shaping operations, where you're likely to check if commonly used prerequisites are available, install commonly used tools, or tamper with security controls prior to the primary execution block.

```text
steps:
  - name: first_sub_ttp
    ttp: examples/sub-ttps/my-sub-ttps/ttp1.yaml
  - name: second_sub_ttp
    ttp: examples/sub-ttps/my-sub-ttps/ttp2.yaml
```

#### Cleanup

In addition to the implementation logic, each TTP must contain a `cleanup` block that reverts artifacts produced by the preceding blocks. In the event that none of your implementation blocks produce artifacts, the `cleanup` block should simply return a success log.

Example with implementation block artifacts. Here we see that we're reverting the changes made in the previous steps.
```text
steps:
  - name: disable-updates
    inline: |
      echo -e "===> Disabling automatic installation of security updates..."
      sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate.plist CriticalUpdateInstall -bool NO
      echo "[+] DONE!"

    cleanup:
      inline: |
        echo -e "===> Enabling automatic installation of security updates..."
        sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate.plist CriticalUpdateInstall -bool YES
        echo "[+] DONE!"
```

Example without implementation block artifacts. No changes were made to the target system and we report that in the success log.
```text
steps:
  - name: clipdump_cli
    inline: |
	  echo -e "===> Dumping clipboard to stdout..."
      pbpaste
      echo "[+] DONE!"
    cleanup:
      inline: |
        echo "No cleanup needed, as this TTP simply dumped clipboard contents to stdout."
```

