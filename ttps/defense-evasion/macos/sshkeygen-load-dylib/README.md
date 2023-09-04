# Load dylib via ssh-keygen

![Community TTP - VVX7](https://img.shields.io/badge/Community_TTP-green)

Loads a custom dylib (which opens Calculator) via ssh-keygen.

## Arguments

- **cleanup**: When set to true, it will delete the compiled dylib.

## Pre-requisites

Ensure that `gcc` is installed and that you have permission to run it.

## Examples

Execute `ssh-keygen -D` to load a dylib. Once execution is complete,
this TTP will delete the generated `calc.dylib` file if cleanup is
set to true:

```bash
ttpforge run ttps/macOS/sshkeygen_load_dylib/sshkeygen_load_dylib.yaml
```

## Steps

1. **Setup**: Compile the dylib that is loaded by ssh-keygen.

1. **Load Dylib**: Execute `ssh-keygen -D` to load the dylib.

1. **Cleanup**: If the `cleanup` argument is set to `true`, delete the
   compiled dylib.
