# TTP Examples - Targets

This TTP illustrates how to specify targets for a TTP.

---

## cloud-target.yaml

If you want to execute the example we provide to specify a cloud target,
you can run the following command:

```bash
ttpforge run forgearmory//examples/targets/cloud-target.yaml
```

Expected output if cloud credentials are set:

```bash
INFO    [*] Validating Steps
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: cloud
INFO    [+] Running current step: ensure-aws-creds-present
INFO    ========= Executing ==========
You have AWS credentials set, well done!
INFO    ========= Done ==========
INFO    [+] Finished running step: ensure-aws-creds-present
INFO    [*] Completed TTP
INFO    [*] No Cleanup Steps Found
```

Expected output if cloud credentials are not set:

```bash
INFO    [*] Validating Steps
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: cloud
INFO    [+] Running current step: ensure-aws-creds-present
INFO    ========= Executing ==========
error: AWS credentials are not set, exiting.
ERROR   [*] Error executing TTP: exit status 1
INFO    [*] Completed TTP
INFO    [*] No Cleanup Steps Found
ERROR   failed to run command:
        failed to run TTP at /Users/$USER/.ttpforge/repos/forgearmory/
        ttps/examples/targets/cloud-target.yaml: exit status 1
```

---

## os-and-arch-target.yaml

If you want to execute the example we provide that shows how to map
operating systems and/or architecture to a TTP,
you can run the following command:

```bash
ttpforge run forgearmory//examples/targets/os-and-arch-target.yaml
```

Expected output:

```text
```
