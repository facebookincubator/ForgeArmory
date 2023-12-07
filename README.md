# ForgeArmory

[![License](https://img.shields.io/github/license/facebookincubator/ForgeArmory?label=License&style=flat&color=blue&logo=github)](https://github.com/facebookincubator/ForgeArmory/blob/main/LICENSE)
[![🚨 Semgrep Analysis](https://github.com/facebookincubator/ForgeArmory/actions/workflows/semgrep.yaml/badge.svg)](https://github.com/facebookincubator/ForgeArmory/actions/workflows/semgrep.yaml)
[![Pre-Commit](https://github.com/facebookincubator/ForgeArmory/actions/workflows/pre-commit.yaml/badge.svg)](https://github.com/facebookincubator/ForgeArmory/actions/workflows/pre-commit.yaml)

ForgeArmory is a repository of attacker Tactics, Techniques, and Procedures
(TTPs) that you can download and run with Meta's
[TTPForge](https://github.com/facebookincubator/TTPForge) attack simulation
engine. Our catalog presently focuses on macOS and Cloud TTPs.

## Setup

To get started,
[install TTPForge](https://github.com/facebookincubator/TTPForge/blob/main/README.md#installation)
and then browse the ForgeArmory
[TTP catalog](https://github.com/facebookincubator/ForgeArmory/tree/main/ttps)
to find cyberattacks to simulate.

## Adding New TTPs

You can add new TTPs to ForgeArmory by
[forking](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this
repository and adding your TTP YAML files to the appropriate directories in the
[catalog](https://github.com/facebookincubator/ForgeArmory/tree/main/ttps).
Check out the
[TTPForge documentation](https://github.com/facebookincubator/TTPForge/blob/main/docs/foundations/README.md)
to learn the syntax for writing TTPs and all of TTPForge's attack simulation
features.

## Submitting Pull Requests

Once your TTPs are ready, feel free to send us a pull request :)

Our automation will run various linters/checks against new pull requests.
Several of the linters in this project may be used as pre-commit hooks if
desired - you can install and setup pre-commit according to the
[official instructions](https://pre-commit.com/).

For quick ad hoc runs, you may wish to run pre-commit in a virtual environment:

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install pre-commit
pre-commit run --all-files
```
