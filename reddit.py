import praw
import requests

from config import REDDIT_CLIENT, REDDIT_SECRET

import facebook
from database import register_event, get_db_user

reddit = praw.Reddit(client_id=REDDIT_CLIENT, client_secret=REDDIT_SECRET, user_agent='my user agent')

IMAGE = 0
TITLE = 1
INNER = 2

#   (SUBREDDIT, RET_TYPE, alias)
subreddits = [
    ("Showerthoughts", TITLE, "showerthought"),
    ("Jokes", INNER, "joke"),
    ("GetMotivated", IMAGE, "motivation"),
    ("Memes", IMAGE, "meme")
]

def process_sub(subreddit_name, recipient, limit=None):
    db_user = get_db_user(recipient)

    for sub in subreddits:
        if sub[0] == subreddit_name:
            if sub[1] == IMAGE:
                message = "http://imgur.com/WeyNGtQ.jpg"
                for submission in reddit.subreddit(subreddit_name).hot(limit=limit):
                    if (submission.link_flair_css_class == 'image') or ((submission.is_self != True) and ((".jpg" in submission.url) or (".png" in submission.url))):
                        if register_event(db_user, submission.id, submission.url):
                            message = submission.url
                            break

                r = facebook.send(recipient, message, image=True)
            elif sub[1] == TITLE:
                for submission in reddit.subreddit(subreddit_name).hot(limit=limit):
                    if submission.is_self:
                        if register_event(db_user, submission.id, submission.title):
                            message = submission.title
                            break

                r = facebook.send(recipient, message)
            elif sub[1] == INNER:
                for submission in reddit.subreddit(subreddit_name).hot(limit=limit):
                    if ((submission.is_self == True) and (submission.link_flair_text is None)):
                        if register_event(db_user, submission.id, submission.title):
                            title = submission.title
                            inner = submission.selftext
                            break

                r = facebook.send(recipient, title + "\n---\n" + inner)

    if r.status_code != requests.codes.ok:
        print(r.text)
