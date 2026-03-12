# Cronjob Persistence

## Description
This TTP creates a simple cron job that drops a text file to the `/tmp` directory and appends to this file each time the cron job is triggered (every minute). This simulates an attacker establishing persistence through scheduled task creation.

## Arguments
- **timeout**: Timeout value to set before cleanup begins. Default: `1200`

## Requirements
- Linux operating system
- Superuser (root) privileges

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/create-cronjob/ttp.yaml --arg timeout=600
```

## Steps
1. **cronjob**: Create a cron job under the root user that writes to `/tmp/purplecrontest.out` every minute, then sleep for the specified timeout. On cleanup, the cron job entry is removed and `/tmp/purplecrontest.out` is deleted.
