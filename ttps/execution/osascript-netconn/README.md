# Red Canary osascript netconn rule trigger

## Description
This TTP tests a Red Canary detector that flags on the osascript binary making network connections. It hosts a JXA file on a local Python 3 web server and uses osascript to fetch and inline-evaluate the script, causing osascript to make a network connection.

## Arguments
- **timeout**: Timeout for the web server which briefly hosts the JXA file, in seconds. Default: `10`.

## Requirements
- macOS (darwin) platform.
- Python 3 must be installed (used for the HTTP server).

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//execution/osascript-netconn/ttp.yaml --arg timeout=15
```

## Steps
1. **osascript_netconn**: Creates a /tmp/purpletest directory with a JXA file that runs the `id` command. Starts a Python 3 HTTP server on port 80 with the specified timeout. Then uses osascript with inline JavaScript to fetch and evaluate the JXA file from the local server using NSData and NSURL, causing osascript to make a network connection. During cleanup, it removes the /tmp/purpletest directory and output file.
