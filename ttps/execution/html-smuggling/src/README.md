## Description

This project simulates an HTML smuggling attack, a technique where malicious content (such as an executable file) is delivered through a browser using JavaScript and HTML without being detected by network security tools. The attack involves three files:

1. `index.html` - This HTML page loads a malicious JavaScript file from a remote attacker's server (C2).
2. `loader.js` - Hosted on the attacker's C2 server, this JavaScript file creates and downloads a malicious executable (`attachment.exe`) on the victim's machine.
3. `attachment.c` - A C program compiled into `attachment.exe`, which, when executed, writes and runs a Python script to gather sensitive information from the victim's system.

## Attack Flow

1. **Initial Delivery (`index.html`)**:
    - The victim opens `index.html`, which uses obfuscated JavaScript to dynamically load a malicious JavaScript file (`loader.js`) hosted on the attacker's C2 server.
    - The script tag is created and appended to the HTML document dynamically to bypass simple static content filtering.

2. **Malicious Payload (`loader.js`)**:
    - Once the victim's browser loads `loader.js` from the attacker's C2 server, the script decodes and reconstructs a base64-encoded executable (`attachment.exe`).
    - This executable is then automatically downloaded to the victim's machine using JavaScript's Blob and File APIs.

3. **Executable Payload (`attachment.exe`)**:
    - The `attachment.c` file is compiled into `attachment.exe`, which is delivered to the victim's system through `loader.js`.
    - Upon execution, `attachment.exe` attempts to find Python on the system, writes a Python script that gathers system information, and then executes the script.
    - The Python script collects data such as the current directory contents, environment variables, and the logged-in user, and saves this data to a file named `gathered.txt` on the victim's machine.

## Files

### `index.html`

- **Purpose**: This HTML file is used to load the malicious `loader.js` script from the attacker's C2 server.
- **How it works**: It creates a script element dynamically and assigns its source to the attacker's `loader.js`. This obfuscation helps bypass basic detection.

### `loader.js`

- **Purpose**: This JavaScript file is hosted on the attacker's C2 server. It constructs a malicious executable (`attachment.exe`) from a base64-encoded string and triggers a download on the victim's machine.
- **How it works**:
  - `to_blob` function converts the base64-encoded binary into a Blob, which simulates a file download in the victim's browser.
  - `trigger` creates a link element, attaches the Blob, and forces the browser to download the file (`attachment.exe`).

### `attachment.c`

- **Purpose**: This is the C source code that, when compiled to `attachment.exe`, creates and runs a Python script to gather sensitive information from the victim's machine.
- **How it works**:
  - It looks for Python in the system's PATH.
  - It writes a Python script to the user's home directory, which collects system information like files in the current directory, environment variables, and the logged-in user.
  - The information is saved to a file called `gathered.txt` on the victim's machine.

## How the Attack Works

1. **User Interaction**: The victim is tricked into opening the `index.html` page (e.g., via a phishing email or malicious link).
2. **HTML Smuggling**: The `index.html` loads the `loader.js` script, which reconstructs and downloads a malicious executable (`attachment.exe`) to the victim's machine.
3. **Execution of the Malicious Payload**: The victim is lured into executing `attachment.exe`, which writes and executes a Python script to gather system data.

## MITRE ATT&CK Mapping

- **T1027**: Obfuscated Files or Information (obfuscating the script element in `index.html`).
- **T1059.006**: Command and Scripting Interpreter: Python (the executable runs a Python script to gather system information).

## Additional Information

- Ensure you have appropriate permission before testing or simulating this attack.
- The `attachment.c` should be compiled to `attachment.exe` before deploying the simulation.
- The `loader.js` script needs to be hosted on a C2 server that the victim can access. Replace `<C2>` in `index.html` with the actual URL of your C2 server.
