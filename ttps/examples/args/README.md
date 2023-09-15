# Defining Arguments for TTPs

Delve into the process of specifying arguments for a TTP. Proper argument
definition ensures flexible and dynamic Tactics, Techniques, and Procedures.

---

## Running `define-args.yaml` Demonstration

To witness the definition and usage of arguments within a TTP, execute:

```bash
ttpforge run forgearmory//examples/args/define-args.yaml \
  --arg a_message=foo \
  --arg a_number=1337
```

---

## Expected Output

```text
INFO    [*] Validating Steps
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: define_args
INFO    [+] Running current step: print_args
INFO    ========= Executing ==========
hi! You passed the message: foo
You passed the number: 1337
has_a_default has the value: 'this is the default value'
INFO    ========= Done ==========
INFO    [+] Finished running step: print_args
INFO    [*] Completed TTP
INFO    [*] No Cleanup Steps Found
```
