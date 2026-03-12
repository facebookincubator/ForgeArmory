import datetime
import subprocess
import sys
import time

if len(sys.argv) < 3:
    print("Usage: python3 continuous_screenshots.py <capture_interval> <max_captures>")
    sys.exit(1)

captureInterval = int(sys.argv[1])
maxCaptures = int(sys.argv[2])

subprocess.run(["mkdir", "/tmp/captures"])

for i in range(maxCaptures):
    print(f"Capturing screenshot {i + 1}/{maxCaptures}")
    filename = f"/tmp/captures/screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    subprocess.run(["screencapture", "-x", filename])
    print(f"Screenshot saved to {filename}")
    time.sleep(captureInterval)
