# ForgeMunitions

[![License](https://img.shields.io/github/license/facebookincubator/ForgeMunitions?label=License&style=flat&color=blue&logo=github)](https://github.com/facebookincubator/ForgeMunitions/blob/main/LICENSE)
[![🚨 Semgrep Analysis](https://github.com/facebookincubator/ForgeMunitions/actions/workflows/semgrep.yaml/badge.svg)](https://github.com/facebookincubator/ForgeMunitions/actions/workflows/semgrep.yaml)
[![Renovate](https://github.com/facebookincubator/ForgeMunitions/actions/workflows/renovate.yaml/badge.svg)](https://github.com/facebookincubator/ForgeMunitions/actions/workflows/renovate.yaml)

This repo is comprised of utilities that I use across various go projects.

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
