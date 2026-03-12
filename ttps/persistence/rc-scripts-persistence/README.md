# RC Scripts Persistence

## Description
This TTP appends a line to the bottom of the `/etc/rc.local` file for persistence. It sets up the rc-local service to execute on boot, which writes to a file at `/tmp/rcpersist.txt` each time the persistence mechanism is triggered. This simulates an attacker using boot initialization scripts for persistence.

## Arguments
- **timeout**: Timeout in seconds before cleanup begins. Default: `120`

## Requirements
- Linux operating system
- Superuser (root) privileges

## Example(s)
You can run this TTP with the following command:
```bash
ttpforge run forgearmory//persistence/rc-scripts-persistence/ttp.yaml --arg timeout=300
```

## Steps
1. **append_to_rclocal**: Append a command to `/etc/rc.local` that writes text to `/tmp/rcpersist.txt` each time the rc persistence is executed. On cleanup, the appended line is removed from `/etc/rc.local`.
2. **set_up_persistence**: Set the executable bit on `/etc/rc.local`, enable and start the rc-local service. On cleanup, the TTP sleeps for the specified timeout, then disables and stops the rc-local service, removes the executable bit from `/etc/rc.local`, and deletes `/tmp/rcpersist.txt`.
