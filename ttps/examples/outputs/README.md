# TTP Examples - Output

This TTP illustrates how to pass outputs between different steps.

## step-outputs.yaml

Run the TTP as follows:

```bash
ttpforge run examples/outputs/step-outputs.yaml
```

Expected output:

```text
this will be accessible in stdout
previous step output is this will be accessible in stdout
{"foo":"bar"}
bar
```
