from flask import Flask, jsonify, request, abort, make_response
app = Flask("Simple Notifications")

from notify import Message, app_indicator
print "ASDF"

@app.route("/message", methods=['GET','POST'])
def new_message():
    response = {}
    summary = response['summary'] = request.form["summary"]
    message = response['message'] = request.form["message"]
    category = response['category'] = request.form["category"]

    msg = Message("Summary","This is the statmessage","Ryan")
    #Message(summary, message, category)

    return jsonify(response)

if __name__ == "__main__":
    app.run()
