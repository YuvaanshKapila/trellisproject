import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

envPath = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(envPath)

app = App(token=os.environ["SLACK_BOT_TOKEN"])

#when mentioned in a channel
@app.event("app_mention")
def handleMention(event, say):
    #strip the @bot part off the front
    text = event["text"].split(">", 1)[-1].strip()
    response = requests.post("http://localhost:8000/chat", json={"message": text})
    say(response.json()["reply"])

#when direct messaged
@app.event("message")
def handleMessage(event, say):
    #ignore the bots own messages so it doesnt loop
    if event.get("bot_id"):
        return
    response = requests.post("http://localhost:8000/chat", json={"message": event.get("text", "")})
    say(response.json()["reply"])

SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()