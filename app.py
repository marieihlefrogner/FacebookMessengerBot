from flask import Flask, request
import os

from config import HUB_VERIFY_TOKEN
 
from events import messaging_events, process_message
from database import create_app

app = create_app()

@app.route('/', methods=['GET'])
def handle_verification():
    print("Handling Verification.")
    if request.args.get('hub.verify_token', '') == HUB_VERIFY_TOKEN:
        print("Verification successful!")
        return request.args.get('hub.challenge', '')
    else:
        print("Verification failed!")
        return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
    print("Handling Messages")
    payload = request.get_data()
    print("payload: " + str(payload))
    for sender, message in messaging_events(payload):
        print("Incoming from {}: {}".format(sender, message))

        def handle(sender, message):
            print("GEVENT: processing message from", sender)
            process_message(sender, message)
        
        Greenlet.spawn(handle, sender, message)
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0')