# File Creation and Cleanup using `test-cleanup` Step

Discover how to create and subsequently clean up files leveraging the
`test-cleanup` step. This example showcases the capability to create a
directory and remove it in the cleanup step.

---

## Running `cleanup-step.yaml` Demonstration

Execute the following command to illustrate the functionality of
the `test-cleanup` step:

```bash
ttpforge run forgearmory//examples/steps/cleanup-step/cleanup-step.yaml
```

---

## Expected Output

```text
INFO    [*] Validating Steps
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: test-cleanup
INFO    [+] Running current step: step_one
INFO    ========= Executing ==========
# Directory "testDir" is created here
INFO    ========= Done ==========
INFO    [+] Finished running step: step_one
INFO    [*] Completed TTP
INFO    [*] Starting Cleanup
INFO    ========= Executing ==========
# Directory "testDir" is removed here
INFO    ========= Done ==========
INFO    [*] Cleanup Complete
```
