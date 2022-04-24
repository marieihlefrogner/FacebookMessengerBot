import requests
import json

from config import FB_PAT

quick_replies_list = [{
    "content_type":"text",
    "title":"Meme",
    "payload":"meme",
},
{
    "content_type":"text",
    "title":"Motivation",
    "payload":"motivation",
},
{
    "content_type":"text",
    "title":"ShowerThought",
    "payload":"shower",
},
{
    "content_type":"text",
    "title":"Joke",
    "payload":"Joke",
}
]

def send(recipient, text, do_qr=True, image=False):
    qr_list = []
    if do_qr:
        qr_list = quick_replies_list
    
    if image:
        return requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": FB_PAT},
            data=json.dumps({
                "recipient": {"id": recipient},
                "message": {"attachment": {
                              "type": "image",
                              "payload": {
                                "url": text
                              }},
                              "quick_replies":qr_list}
            }),
            headers={'Content-type': 'application/json'})

    return requests.post("https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": FB_PAT},
            data=json.dumps({
                "recipient": {"id": recipient},
                "message": {"text": text,
                            "quick_replies":qr_list}
            }),
            headers={'Content-type': 'application/json'})