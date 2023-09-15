# Passing Outputs Between TTP Steps

Discover the methodology to efficiently pass outputs from one TTP step
to the subsequent steps, ensuring seamless data flow within a procedure.

---

## Running `step-outputs.yaml` Demonstration

To observe the interplay of outputs between different TTP steps, execute:

```bash
ttpforge run forgearmory//examples/outputs/step-outputs.yaml
```

---

## Expected Output

```text
INFO    [*] Validating Steps
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: step_outputs_example
INFO    [+] Running current step: raw_output
INFO    ========= Executing ==========
this will be accessible in stdout
INFO    ========= Done ==========
INFO    [+] Finished running step: raw_output
INFO    [+] Running current step: access_raw_output
INFO    ========= Executing ==========
previous step output is this will be accessible in stdout
INFO    ========= Done ==========
INFO    [+] Finished running step: access_raw_output
INFO    [+] Running current step: with_json_output
INFO    ========= Executing ==========
{"foo":"bar"}
INFO    ========= Done ==========
INFO    [+] Finished running step: with_json_output
INFO    [+] Running current step: print_json
INFO    ========= Executing ==========
bar
INFO    ========= Done ==========
INFO    [+] Finished running step: print_json
INFO    [*] Completed TTP
INFO    [*] No Cleanup Steps Found
```
