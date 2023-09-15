# Specifying Targets for TTPs

Gain insights on how to define specific targets for a TTP, be it a cloud service,
an operating system, or a certain architecture.

---

## Running `cloud-target.yaml` Demonstration

To demonstrate the specification of a cloud target, execute:

```bash
ttpforge run forgearmory//examples/targets/cloud-target.yaml
```

---

## Expected Output (With Cloud Credentials)

```text
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

## Expected Output (Without Cloud Credentials)

```text
INFO    [*] Validating Steps
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: cloud
INFO    [+] Running current step: ensure-aws-creds-present
INFO    ========= Executing ==========
error: AWS_DEFAULT_REGION must be set.
ERROR   [*] Error executing TTP: exit status 1
INFO    [*] Completed TTP
INFO    [*] No Cleanup Steps Found
ERROR   failed to run command:
        failed to run TTP at /Users/$USER/.ttpforge/repos/forgearmory/ttps/
        examples/targets/cloud-target.yaml:
        exit status 1
```

---

## Running `os-and-arch-target.yaml` Demonstration

To visualize the mapping of operating systems and architectures to a TTP, execute:

```bash
ttpforge run forgearmory//examples/targets/os-and-arch-target.yaml
```

---

## Expected Output

```text
INFO    [*] Validating Steps
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: os-and-arch-target
INFO    [+] Running current step: friendly-message
INFO    ========= Executing ==========
You are running a TTP that works for the following operating systems: [linux macos]
and architectures: [x86_64 arm64].
It can be used for the following cloud providers
at the specified regions as well: [aws:us-west-1 gcp:us-west1-a azure:eastus].
INFO    ========= Done ==========
INFO    [+] Finished running step: friendly-message
INFO    [*] Completed TTP
INFO    [*] No Cleanup Steps Found
```
