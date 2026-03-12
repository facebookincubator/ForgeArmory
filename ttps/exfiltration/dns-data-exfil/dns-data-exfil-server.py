import os

from dnslib import DNSHeader, DNSRecord, QTYPE, RR
from dnslib.server import DNSServer


class ExfilDNSHandler:
    def __init__(self):
        self.subdomains = []

    def resolve(self, query, handler):
        # Log the incoming query
        print(f"Received query for: {query.q.qname} ({query.q.qtype})")

        # Prepare a response
        response = query.reply()

        if query.q.qtype == QTYPE.A:
            ip = "192.168.1.1"
            response.add_answer(*RR.fromZone(f"{query.q.qname} 60 A {ip}"))
        elif query.q.qtype == QTYPE.TXT:
            response.add_answer(
                *RR.fromZone(f"{query.q.qname} 60 TXT Response: TXT Record")
            )

        if query.q.qname == "end":
            data = "".join(self.subdomains)
            with open("output.txt", "w") as file:
                file.write(data)
            print("Data written to output.txt")

            os._exit(0)

        self.subdomains.append(str(query.q.qname).split(".")[0])

        return response


handler = ExfilDNSHandler()
server = DNSServer(handler, port=53, address="0.0.0.0")


print("Starting DNS server...")
server.start()

print("Stopping DNS server...")
server.stop()
