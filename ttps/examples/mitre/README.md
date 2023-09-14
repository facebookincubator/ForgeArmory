# TTP Examples - MITRE ATT&CK Mapping

## mitre.yaml

If you want to execute the example we provide that shows how to map
a TTP to MITRE ATT&CK, you can run the following command:

```bash
ttpforge run forgearmory//examples/targets/mitre-target.yaml
```

Expected output:

```text
INFO    [*] Validating Steps
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: mitre-target
INFO    [+] Running current step: friendly-message
INFO    ========= Executing ==========
You are running a TTP that is mapped to MITRE ATT&CK
INFO    ========= Done ==========
INFO    [+] Finished running step: friendly-message
INFO    [*] Completed TTP
INFO    [*] No Cleanup Steps Found
```
