# pip Package Installer

## Description
A helper TTP designed to install Python libraries needed for other TTPs. It first verifies that pip is installed (attempting to install it via `ensurepip` if missing), then installs the specified Python packages.

## Arguments
- **modules**: Space-delimited list of Python libraries to install (required, type: string)
- **proxy**: Optional proxy address for pip install and git clone (leave empty for direct connection). Defaults to `""`.

## Requirements
- Python 3 must be available.
- Network access to PyPI or a configured package repository.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//utils/pip-install/ttp.yaml --arg modules="requests pandas numpy"
```

## Steps
1. **pip_check**: Checks if pip is installed. If not, attempts to install it using `ensurepip --upgrade`. Exits with an error if pip cannot be installed.
2. **install**: Installs the specified Python packages using `pip install` with the provided module list.
