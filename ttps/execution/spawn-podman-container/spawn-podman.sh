#!/usr/bin/expect -f

set timeout -1

spawn podman run --network=host -it ubuntu:20.04 /bin/bash

expect "*#"

send -- "cat /etc/*-release\r"

expect "This string will not be found"

expect eof
