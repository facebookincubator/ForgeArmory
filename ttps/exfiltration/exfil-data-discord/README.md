# Data Exfiltration via Discord

## Description
This TTP mimics an attacker exfiltrating data via a Discord bot from a compromised macOS system. It executes a specified command on the target system and sends the output to Discord using a Python script, provided a valid channel ID and bot token are configured.

## Arguments
- **command**: Command to execute on the target system and exfiltrate the output to Discord.

## Requirements
- macOS (darwin) platform.
- Python 3 must be installed.
- A valid Discord bot token and channel ID must be configured in the exfil-discord.py script.

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//exfiltration/exfil-data-discord/ttp.yaml --arg command="whoami"
```

## Steps
1. **Gather information**: Executes the specified command on the target system and captures the output as a variable.
2. **Send data to Discord**: Runs the exfil-discord.py Python script with the captured command output to send the data to a Discord channel via a bot.
