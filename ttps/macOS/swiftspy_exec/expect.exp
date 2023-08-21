#!/usr/bin/expect

spawn /bin/bash

expect "*bash"

send -- "./swiftspy -keylog\r"

expect "*bash"

expect eof
