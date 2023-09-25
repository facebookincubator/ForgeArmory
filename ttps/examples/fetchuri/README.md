# Using the FetchURI Step in TTPs

Discover how to effectively employ the `FetchURI` step in TTPs to fetch content
from a specific URI and store it in a file.

---

## Running `fetchuri-example.yaml` Demonstration

To observe the functionality of the `FetchURI` step in action, execute:

```bash
ttpforge run forgearmory//examples/fetchuri/fetchuri.yaml
```

---

## Expected Output

```text
INFO    [*] Validating Steps
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: fetchuri_step_example
INFO    [+] Running current step: fetch-google-and-store-in-file
INFO    ========= Executing ==========
INFO    ========= Result ==========
INFO    [+] Finished running step: fetch-google-and-store-in-file
INFO    [*] Completed TTP
INFO    [*] Beginning Cleanup
INFO    ========= Executing ==========
INFO    ========= Result ==========
INFO    [*] Finished Cleanup
```
