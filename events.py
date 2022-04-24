import json
import shlex
import sys

import reddit
import facebook
import weather
import maps
import chat

def messaging_events(payload):
    data = json.loads(payload.decode('utf-8'))
    for event in data["entry"][0]["messaging"]:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"]
        else:
            yield event["sender"]["id"], "I can't echo this"


def process_message(recipient, text):
    print("message:", text)
    if "weather for" in text.lower():
        # check weather
        args = shlex.split(text)
        lat, lng = maps.get_location(args[1])

        if None not in [lat, lng]:
            w = weather.get_weather(lat, lng)
            facebook.send(recipient, "Weather for {} {}: \n---\n{}\n{}°C".format(args[2], args[3], w[0], w[1]))
        else:
            facebook.send(recipient, "I don't know where {} is.".format(args[2]))

    else:
        # check reddit
        found = False

        for sub in reddit.subreddits:
            if text.lower() == sub[2]:
                reddit.process_sub(sub[0], recipient)
                found = True

        if not found:
            facebook.send(recipient, " ")
            try:
                facebook.send(recipient, str(chat.get_answer(text)))
            except Exception as e:
                print(str(e))
                facebook.send(recipient, "Error")