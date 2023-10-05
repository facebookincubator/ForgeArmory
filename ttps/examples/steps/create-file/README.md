# The `create_file:` Step

This step type will edit the contents of a specified existing 
target file. Reach for this step in a situation where you 
might use `sed`. Example use cases include:

* Adding a malicious `/etc/sudoers` entry.
* Commenting out authorization checks in critical server-side code.

## Example Usage

Usage of the `create_file:` step is demonstrated in the below TTP:

https://github.com/facebookincubator/TTPForge/blob/main/ttps/examples/steps/create-file/create-file-example.yaml

## Run This Example

Run this example as follows:

```bash
ttpforge run forgearmory//examples/steps/create-file/create-file-example.yaml
```