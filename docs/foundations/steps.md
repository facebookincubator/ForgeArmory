# Steps

Relying on interpreter scripts for attack simulation will often provide defenders with logs/telemetry
that differs from what they would observer in real cyber threat situations. For instance,
an attacker who is maliciously editing a configuration file is unlikely to
do so by running a shell command such as:

```
sed -ie 's/benign/malicious/' sabotaged.cfg
```

The code above will generate a varienty of indicators of compromise (IOCs) that would be visible
to defenders: 

1. Shell History Logs 
1. Process Execution Logs

In reality, an attacker would likely simply edit the file with an existing editor program (such as VS Code)
or modify it directly from their C2 implant with no shell involved. Raw file modification telemetry
would likely be necessary to detect this malicious action, and the attack simulation should reflect
that reality. 

TTPForge solves this problem by providing a wide range of native YAML-based steps from 
which attack chains can be constructed. These steps (downloading files, editing files, etc.) are
natively built into the TTPForge engine itself and do not produce unrealistic shell history telemetry.

Note that the logs associated with execution of `ttpforge` itself from an interactive shell might be considered undesirable telemetry in certain situations - should this be the case, one can consider
obfuscating `ttpforge` by renaming the binary or employing purpose-built obfuscation tools such as
[garble](https://github.com/burrowers/garble).

Each of TTPForge's step types is described below.

# Create File Step

This step will create a file the specified contents 
on disk. Example use cases include:

* Writing a malicious `crontab` file to establish persistence.
* Dropping a malicious PHP webshell in `/var/www/html`.

Usage of the `create_file:` step is demonstrated below:

https://github.com/facebookincubator/TTPForge/blob/main/ttps/examples/steps/create-file/create-file-example.yaml

Run this example as follows:

```bash
ttpforge run forgearmory//examples/steps/edit-file/edit-file-example.yaml
```

[create_file](../../ttps/examples/steps/create-file/README.md)
[edit_file](../../ttps/examples/steps/edit-file/README.md)

COMING SOON

`file:`
`inline:`
`fetch_uri:`
`ttp:`