# Ignore Errors in a TTP step

Understand the process of ignoring errors in a specific TTP step.

---

## Running `ignore-errors.yaml` Demonstration

To see the `ignore_errors` functionality in action, execute:

```bash
ttpforge run forgearmory//examples/ignore-errors/ignore-errors.yaml
```

This will illustrate how to create a step that allows the TTP to continue,
even if an error occurs within a previous step.

By setting the `ignore_errors: true` on a step, subsequent steps in the
TTP can continue executing even if there's an error in the current step.

---

## Expected Output

```text
INFO    [*] Validating Steps
INFO    executor set via extension      {"exec": "sh"}
INFO    [*] Validating Sub TTP: subttp-step-with-error
INFO    [*] Finished validating Sub TTP
INFO    [*] Validating Sub TTP: second_sub_ttp
INFO    [*] Finished validating Sub TTP
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: ignore-errorsure
INFO    [+] Running current step: basic-step-expected-to-fail
INFO    ========= Executing ==========
this will fail
ERROR   {error 26 0  exit status 1}
WARN    Error ignored due to 'ignore_errors' parameter
INFO    [+] Finished running step: basic-step-expected-to-fail
INFO    [+] Running current step: basic-step-post-error
INFO    ========= Executing ==========
We still reach this step despite there being an error
in the previous inline step.
INFO    ========= Result ==========
INFO    [+] Finished running step: basic-step-post-error
INFO    [+] Running current step: file-step-expected-to-fail
INFO    ========= Executing ==========
ERROR   bad exit of process     {"stdout": "", "stderr": "", "exit code": 1}
ERROR   {error 26 0  exit status 1}
WARN    Error ignored due to 'ignore_errors' parameter
INFO    [+] Finished running step: file-step-expected-to-fail
INFO    [+] Running current step: file-step-post-error
INFO    ========= Executing ==========
We still reach this step despite there being an error
in the previous file step.
INFO    ========= Result ==========
INFO    [+] Finished running step: file-step-post-error
INFO    [+] Running current step: edit-step-expected-to-fail
INFO    ========= Executing ==========
WARN    Error ignored due to 'ignore_errors' parameter{error 26 0
pattern 'I_DONT_EXIST_IN_THE_FILE' from edit #1 was not found in file ignore-errors-edit-example.txt}
WARN    Error ignored due to 'ignore_errors' parameter{error 26 0  pattern
'(?ms:^result = await myclass\.multi_line_function_call\(.*?\)$)' from edit #2 was not found in file ignore-errors-edit-example.txt}
WARN    Error ignored due to 'ignore_errors' parameter{error 26 0  pattern
'(?P<fn_call>(?ms:^another_multline_function_call\(.*?\)$))' from edit #3 was not found in file ignore-errors-edit-example.txt}
INFO    ========= Result ==========
INFO    [+] Finished running step: edit-step-expected-to-fail
INFO    [+] Running current step: edit-step-post-error
INFO    ========= Executing ==========
We still reach this step despite there being an error
in the previous edit step.
INFO    ========= Result ==========
INFO    [+] Finished running step: edit-step-post-error
INFO    [+] Running current step: subttp-step-with-error
INFO    [*] Executing Sub TTP: subttp-step-with-error
INFO    [+] Running current step: step_one
INFO    ========= Executing ==========
we are about to fail
ERROR   {error 26 0  exit status 1}
WARN    Error ignored due to 'ignore_errors' parametererrorexit status 1
INFO    [+] Finished running step: step_one
INFO    ========= Result ==========
INFO    [+] Finished running step: subttp-step-with-error
INFO    [+] Running current step: second_sub_ttp
INFO    [*] Executing Sub TTP: second_sub_ttp
INFO    [+] Running current step: step_one
INFO    ========= Executing ==========
you said testing
INFO    ========= Result ==========
INFO    [+] Finished running step: step_one
INFO    ========= Result ==========
INFO    [+] Finished running step: second_sub_ttp
INFO    [+] Running current step: subttp-step-post-error
INFO    ========= Executing ==========
We still reach this step despite there being an error
in one of the subttp steps.
INFO    ========= Result ==========
INFO    [+] Finished running step: subttp-step-post-error
INFO    [+] Running current step: fetchURI-step-no-error
INFO    ========= Executing ==========
INFO    ========= Result ==========
INFO    [+] Finished running step: fetchURI-step-no-error
INFO    [+] Running current step: fetchURI-step-with-error
INFO    ========= Executing ==========
ERROR   {error 26 0  Get "http://not-a-real-siteabc123456.com": dial tcp: lookup not-a-real-siteabc123456.com: no such host}
WARN    Error ignored due to 'ignore_errors' parameter
INFO    [+] Finished running step: fetchURI-step-with-error
INFO    [+] Running current step: fetchuri-step-post-error
INFO    ========= Executing ==========
We still reach this step despite there being an error
in the fetchuri step.
INFO    ========= Result ==========
INFO    [+] Finished running step: fetchuri-step-post-error
INFO    [*] Completed TTP
INFO    [*] Beginning Cleanup
INFO    ========= Executing ==========
INFO    ========= Result ==========
INFO    ========= Executing ==========
cleanup my_sub_ttp_2
INFO    ========= Result ==========
INFO    ========= Executing ==========
cleanup my_sub_ttp_1
INFO    ========= Result ==========
INFO    ========= Executing ==========
INFO    ========= Result ==========
INFO    [*] Finished Cleanup
```
