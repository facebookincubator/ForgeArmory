# Setup Python Virtual Environment

## Description
Creates a Python virtual environment with specified package(s) installed.
Outputs the venv path to PYTHON_VENV for use by subsequent steps or parent TTPs.

Supports PyPI packages and git repos (prefix with git+) in the same list:
  packages: "impacket,git+https://github.com/Hackndo/pyGPOAbuse.git,requests"

## Arguments
- **packages**: Package(s) to install (comma-separated). Use git+https:// prefix for git repos. No default (required).
- **venv_path**: Path where the virtual environment will be created. Defaults to `/tmp/python_venv`.
- **clone_path**: Path where git repositories will be cloned. Defaults to `/tmp/git_repos`.
- **proxy**: Optional proxy address for pip install and git clone (leave empty for direct connection). Defaults to `""`.

## Requirements
- **Platforms:** Linux, macOS

## Example(s)
```bash
ttpforge run forgearmory//ttps/utils/setup-python-venv/ttp.yaml \
  --arg packages=impacket
```

```bash
ttpforge run forgearmory//ttps/utils/setup-python-venv/ttp.yaml \
  --arg packages="impacket,git+https://github.com/Hackndo/pyGPOAbuse.git,requests" \
  --arg venv_path=/tmp/my_venv
```

## Steps
1. **create_venv**: Create Python virtual environment. Outputs the venv path to PYTHON_VENV. Cleanup removes the virtual environment directory.
2. **install_packages**: Install packages, cloning git repos as needed. Handles both PyPI packages and git repositories. Cleanup removes the clone directory.
