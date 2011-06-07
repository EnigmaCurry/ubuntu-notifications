import threading
import logging
import flask
from flask import Flask, jsonify, request, abort, make_response

from dbus_client import get_notify

logging.basicConfig()
logger = logging.getLogger("simple_notification.indicator")
app = Flask("Simple Notifications")
notify = None

@app.route("/message", methods=['GET','POST'])
def new_message():
    response = {}
    summary = response['summary'] = request.form["summary"]
    message = response['message'] = request.form["message"]
    category = response['category'] = request.form["category"]

    notify("Summary","This is the statmessage","Ryan")

    return jsonify(response)

class FlaskApp(threading.Thread):
    def __init__(self):
        global notify
        notify = get_notify()
        threading.Thread.__init__(self)
    def run(self):
        logger.warn("flask app staring...")
        app.run()
