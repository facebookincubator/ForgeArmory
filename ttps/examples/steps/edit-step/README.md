# File Modification using `edit_file` Step

Discover how to make amendments to files leveraging the `edit_file` step,
a versatile tool for editing files through string matching or regular expressions.

---

## Running `edit-step.yaml` Demonstration

Execute the following command to illustrate the power of the `edit_file` step:

```bash
ttpforge run forgearmory//examples/steps/edit-step/edit-step.yaml
```

---

## Expected Output

```text
INFO    [*] Validating Steps
INFO    [+] Finished validating steps
INFO    [+] Running current TTP: edit_step_example
INFO    [+] Running current step: target-file-pre-edit
INFO    ========= Executing ==========
This is an example file.

The TTP will replace the string below:

REPLACE_ME

It will also delete the multi-line string below and replace
it with a comment:

result = await myclass.multi_line_function_call(
    param1,
    param2,
)

Lastly, it will comment out the subsequent lines using a C-Style /* ... */ comment.

another_multline_function_call(
    param1,
    param2,
)
INFO    ========= Done ==========
INFO    [+] Finished running step: target-file-pre-edit
INFO    [+] Running current step: edit-target-file
INFO    [+] Finished running step: edit-target-file
INFO    [+] Running current step: target-file-post-edit
INFO    ========= Executing ==========
This is an example file.

The TTP has replaced the string below with:

REPLACED_BY_EDIT

The multi-line string was deleted and replaced with a comment:

# replaced with comment

The following lines have been commented using a C-Style /* ... */ comment:

/*another_multline_function_call(
    param1,
    param2,
)*/
INFO    ========= Done ==========
INFO    [+] Finished running step: target-file-post-edit
INFO    [*] Completed TTP
INFO    [*] Starting Cleanup
INFO    ========= Executing ==========
INFO    ========= Done ==========
INFO    [*] Cleanup Complete
```
