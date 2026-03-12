import subprocess
import sys

if len(sys.argv) != 3:
    print("Usage: python3 attempt_ssh.py <username> <password>")
hostname = "localhost"
username = sys.argv[1]
password = sys.argv[2]

ssh_command = [
    "sshpass",
    "-p",
    password,
    "ssh",
    "-o",
    "NumberOfPasswordPrompts=1",
    "-o",
    "StrictHostKeyChecking=no",
    f"{username}@{hostname}",
    "whoami",
]

try:
    result = subprocess.run(ssh_command, capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print("SSH connection successful!")
        print(result.stdout)
    else:
        print("Authentication failed as expected.")
except Exception as e:
    print(f"SSH connection failed: {e}")
