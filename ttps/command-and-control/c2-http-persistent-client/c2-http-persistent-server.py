# Install flask: "pip install flask" or "apt install flask"

import os
import time

import flask

app = flask.Flask(__name__)


@app.route("/")
def stream():
    def response_gen():
        try:
            while True:
                yield "data: Hello World\n\n"
                time.sleep(5)
        except GeneratorExit:
            os._exit(0)

    return flask.Response(response_gen(), mimetype="text/event-stream")


# Change port number as appropriate for the client
app.run(threaded=False, host="0.0.0.0", port=80)
