import socket
import sys

HOST = ""
PORT = port_here  # noqa: F821 — replaced at runtime by TTPForge sed
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    soc.bind((HOST, PORT))

except socket.error as message:
    print("Bind failed. Error Code : " + str(message[0]) + " Message " + message[1])
    sys.exit()

print("Listening on port " + str(PORT) + " ...")
soc.listen(9)
conn, address = soc.accept()
print("Connected with " + address[0] + ":" + str(address[1]))
