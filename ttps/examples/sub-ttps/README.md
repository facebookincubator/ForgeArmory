# Chaining Tactics with SubTTPs

Delve into the process of crafting a TTP with integrated SubTTPs. This technique
enables chaining multiple Tactics, Techniques, and Procedures for a streamlined
attack sequence.

---

## Running `sub-ttps.yaml` Demonstration

To visualize how SubTTPs function within a TTP, initiate the command below:

```bash
ttpforge run forgearmory//examples/sub-ttps/sub-ttps.yaml
```

---

## Expected Output

```text
INFO    [*] Validating Steps
INFO    [*] Validating Sub TTP: first_sub_ttp
INFO    [*] Finished validating Sub TTP
INFO    [*] Validating Sub TTP: second_sub_ttp
INFO    [*] Finished validating Sub TTP
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: sub_ttp_example
INFO    [+] Running current step: first_sub_ttp
INFO    [*] Executing Sub TTP: first_sub_ttp
INFO    [+] Running current step: step_one
INFO    ========= Executing ==========
hello
INFO    ========= Done ==========
INFO    [+] Finished running step: step_one
INFO    Finished execution of sub ttp file
INFO    [+] Finished running step: first_sub_ttp
INFO    [+] Running current step: second_sub_ttp
INFO    [*] Executing Sub TTP: second_sub_ttp
INFO    [+] Running current step: step_one
INFO    ========= Executing ==========
you said testing
INFO    ========= Done ==========
INFO    [+] Finished running step: step_one
INFO    Finished execution of sub ttp file
INFO    [+] Finished running step: second_sub_ttp
INFO    [*] Completed TTP
INFO    [*] Starting Cleanup
INFO    ========= Executing ==========
cleanup my_sub_ttp_2
INFO    ========= Done ==========
INFO    ========= Executing ==========
cleanup my_sub_ttp_1
INFO    ========= Done ==========
INFO    [*] Cleanup Complete
```
