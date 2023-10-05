# ForgeArmory

[![License](https://img.shields.io/github/license/facebookincubator/ForgeArmory?label=License&style=flat&color=blue&logo=github)](https://github.com/facebookincubator/ForgeArmory/blob/main/LICENSE)
[![🚨 Semgrep Analysis](https://github.com/facebookincubator/ForgeArmory/actions/workflows/semgrep.yaml/badge.svg)](https://github.com/facebookincubator/ForgeArmory/actions/workflows/semgrep.yaml)
[![Pre-Commit](https://github.com/facebookincubator/ForgeArmory/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/facebookincubator/ForgeArmory/actions/workflows/pre-commit.yaml)
[![Renovate](https://github.com/facebookincubator/ForgeArmory/actions/workflows/renovate.yaml/badge.svg)](https://github.com/facebookincubator/ForgeArmory/actions/workflows/renovate.yaml)

TTPForge is a cyber attack simulation platform. This project promotes a
Purple Team approach to cybersecurity with the following goals:

* To help blue teams accurately measure their detection and response capabilities
  through high-fidelity simulations of real attacker activity.
* To help red teams improve the ROI/actionability of their findings by packaging
  their attacks as automated, repeatable simulations.

TTPForge allows you to automate  attacker tactics, techniques, and procedures (TTPs)
using a powerful but easy-to-use YAML format. This repo 
contains our open-source catalog of TTPForge-powered TTPs - 
check out the links below to learn more: 

* [Install TTPForge](#installation)
* [TTPForge Design Philosophy](docs/foundations/design-philosophy.md)
* [Writing TTPs with TTPForge](docs/foundations/writing-ttps.md)
* [Our TTP Library](https://github.com/facebookincubator/ForgeArmory/tree/main/ttps)

## Installation

1. Get latest TTPForge release:

   ```bash
   bashutils_url="https://raw.githubusercontent.com/l50/dotfiles/main/bashutils"

   bashutils_path="/tmp/bashutils"

   if [[ ! -f "${bashutils_path}" ]]; then
      curl -s "${bashutils_url}" -o "${bashutils_path}"
   fi

   source "${bashutils_path}"

   fetchFromGithub "facebookincubator" "TTPForge" "latest" ttpforge
   ```

   At this point, the latest `ttpforge` release should be in
   `~/.local/bin/ttpforge` and subsequently, the `$USER`'s `$PATH`.

   If running in a stripped down system, you can add TTPForge to your `$PATH`
   with the following command:

   ```bash
   export PATH=$HOME/.local/bin:$PATH
   ```

1. Initialize TTPForge configuration

   This command will place a configuration file at the default location
   `~/.ttpforge/config.yaml` and download the
   [ForgeArmory](https://github.com/facebookincubator/ForgeArmory)
   TTPs repository:

   ```bash
   ttpforge init
   ```

TTPForge is now ready to use - check out our [tutorial](#tutorial) to
start exploring its capabilities.

## Tutorial

1. List available TTP repositories (should show `forgearmory`)

   ```bash
   ttpforge list repos
   ```

1. List available TTPs that you can run:

   ```bash
   ttpforge list ttps
   ```

1. Examine an example TTP:

   ```bash
   ttpforge show ttp forgearmory//examples/args/define-args.yaml
   ```

1. Run the specified example:

   ```bash
   ttpforge run \
     forgearmory//examples/args/define-args.yaml \
     --arg a_message="hello" \
     --arg a_number=1337
   ```

1. Next, check out the Armory's collection of [TTPs](https://github.com/facebookincubator/ForgeArmory/tree/main/ttps) and learn to [write your own TTPs](docs/foundations/writing-ttps.md) 

---

## Dependencies

- [Install asdf](https://asdf-vm.com/):

  ```bash
  git clone https://github.com/asdf-vm/asdf.git ~/.asdf
  ```

- Install and use asdf plugins to manage go, python, and ruby for this project:

  ```bash
  source .asdf
  ```

  Alternatively, you can pick and choose which plugins to install:

  ```bash
  # Employ asdf for this project's python:
  source .asdf python
  ```

- [Install pre-commit](https://pre-commit.com/):

  ```bash
  python3 -m pip install --upgrade pip
  python3 -m pip install pre-commit
  ```

- [Install Mage](https://magefile.org/):

  ```bash
  go install github.com/magefile/mage@latest
  ```

---

## For Contributors and Developers

1. [Fork this project](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

1. Install dependencies:

   ```bash
   mage installDeps
   ```

1. Update and run pre-commit hooks locally:

   ```bash
   mage runPreCommit
   ```

---

## Create New Release

This requires the [GitHub CLI](https://github.com/cli/cli#installation)
and [gh-changelog GitHub CLI extension](https://github.com/chelnak/gh-changelog).

Install changelog extension:

```bash
gh extension install chelnak/gh-changelog
```

Generate changelog:

```bash
NEXT_VERSION=v1.1.3
gh changelog new --next-version "${NEXT_VERSION}"
```

Create release:

```bash
gh release create "${NEXT_VERSION}" -F CHANGELOG.md
```
