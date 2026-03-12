# Install flask: "pip install flask" or "apt install flask"
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/<path:subpath>", methods=["GET", "POST"])
def handle_request(*args, **kwargs):
    return ""


# Change port number as appropriate
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
