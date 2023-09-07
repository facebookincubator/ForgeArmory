# TTP Development

This document introduces concepts to help developers
create their own TTPs for use in TTPForge.

## TTP Anatomy

ForgeArmory TTPs are designed to be consumed by [TTPForge](https://github.com/facebookincubator/TTPForge),
which provides an interface to execute TTPs across various targets and mediums.
Each ForgeArmory TTP consists of metadata and optional argument declarations.
The steps define the TTP implementation logic.

### Metadata

TTP metadata must include the name of the TTP and a description of that TTP's
behavior. MITRE ATT&CK IDs are optional but recommended. If the TTP cannot be
mapped to MITRE ATT&CK then the `mitre` mapping and its child mappings should be
omitted.

An example of TTP metadata is shown below.

```yaml
---
name: Leverage mdfind to search for aws credentials on disk.
description: |
  This TTP runs a search using mdfind to search for AKIA strings in files,
  which would likely indicate that the file is an aws key.
mitre:
  tactics:
    - TA0006 Credential Access
  techniques:
    - T1552 Unsecured Credentials
  subtechniques:
    - "T1552.001 Unsecured Credentials: Credentials In Files"
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
      set -e

      echo "hi! You passed the message: {{ .Args.a_message }}"
      echo "You passed the number: {{ .Args.a_number }}"
      echo "has_a_default has the value: '{{ .Args.has_a_default }}'"
```

### Steps

Steps are uniquely named blocks of implementation logic which are executed in
sequence. Steps help developers organize and manage the complexity of TTPs.

In general, steps will fall into one of the following high-level categories;

- Assessment
- Shaping
- Execution
- Cleanup

Additionally, TTPs may be daisy-chained enabling developers to create complex
sequences of TTPs. In doing so, each daisy-chained TTP is represented in the
parent TTP as a sub-TTP. We'll see an example of this shortly and some
recommendations on developing sub-TTPs as common building blocks.

#### Assessment

It is often necessary for a TTP to test execution requirements, such as whether
a necessary environment variable is set, and bail out of the TTP if it is not.
In this example, if the `AWS_DEFAULT_REGION` environment variable is not set,
the TTP returns exit code 1 and no further blocks are executed.

```yaml
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

When creating assessment type blocks, it's preferable to place each test in its
own block rather than a single block that tests all prerequisites. This approach
will make your TTPs much easier to maintain as they become more complex.

#### Shaping

It is often necessary for a TTP to install dependencies, stage files, or shape
the target environment prior to executing the core TTP logic. As with assessment
type blocks, when creating shaping type blocks, it's preferable to place each
action in its own block.

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

The execution blocks contain the core TTP logic. A single execution block may
be sufficient for simple TTPs such as atomics, which contain a single procedure.
For complex TTPs, the core logic should be broken up across multiple steps or
sub-TTPs. In general, if the core logic implements multiple procedures or the
procedure can be reasonably divided, refactoring into smaller steps will enhance
maintainability.

Code likely to be reused in other TTPs should be placed in a sub-TTP and imported
where needed. It's easier to maintain building blocks than to modify the same
(reimplemented) code in multiple places. Good candidates for sub-TTPs include
assessment and shaping operations. Here, you might check for commonly used
prerequisites, install frequent tools, or tamper with security controls before
the primary execution block.

```yaml
steps:
  - name: first_sub_ttp
    ttp: examples/sub-ttps/my-sub-ttps/ttp1.yaml
  - name: second_sub_ttp
    ttp: examples/sub-ttps/my-sub-ttps/ttp2.yaml
```

#### Cleanup

In addition to the implementation logic, each TTP must contain a `cleanup` block
to revert artifacts from the preceding blocks. If no implementation blocks produce
artifacts, the `cleanup` block should just return a success log.

Example with implementation block artifacts: Here, we revert changes made in
previous steps.

```yaml
steps:
  - name: disable-updates
    inline: |
      set -e

      echo -e "===> Disabling automatic installation of security updates..."
      sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate.plist CriticalUpdateInstall -bool NO
      echo "[+] DONE!"

    cleanup:
      inline: |
        set -e

        echo -e "===> Enabling automatic installation of security updates..."
        sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate.plist CriticalUpdateInstall -bool YES
        echo "[+] DONE!"
```
