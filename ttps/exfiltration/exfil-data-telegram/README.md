# Data Exfiltration via Telegram

## Description
This TTP mimics an attacker exfiltrating data via a Telegram bot from a compromised macOS system. It executes a specified command on the target system and sends the output to Telegram using a Python script, provided a valid chat ID and bot token are configured.

## Arguments
- **command**: Command to execute on the target system and exfiltrate the output to Telegram.

## Requirements
- macOS (darwin) platform.
- Python 3 must be installed.
- A valid Telegram bot token and chat ID must be configured in the exfil-telegram.py script.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//exfiltration/exfil-data-telegram/ttp.yaml --arg command="whoami"
```

## Steps
1. **Gather information**: Executes the specified command on the target system and captures the output as a variable.
2. **Send data to Telegram**: Runs the exfil-telegram.py Python script with the captured command output to send the data to a Telegram chat via a bot.
