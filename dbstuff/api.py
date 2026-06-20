from fastapi import FastAPI
from pydantic import BaseModel
from agent import chat
from fastapi.responses import FileResponse
import os
import requests

app = FastAPI()

#makes the request into json wiht a field called message
class Message(BaseModel):
    message: str

@app.get("/")
def home():
    return FileResponse("index.html")

#since data is being sent a post reqeust is required
@app.post("/chat")
def chatEndpoint(msg: Message):
    return {"reply": chat(msg.message)}

@app.get("/slack/oauth")
def slackOauth(code: str):
    result = requests.post("https://slack.com/api/oauth.v2.access", data={
        "client_id": os.environ["SLACK_CLIENT_ID"],
        "client_secret": os.environ["SLACK_CLIENT_SECRET"],
        "code": code,
        "redirect_uri": os.environ["SLACK_REDIRECT_URI"],
    })
    return result.json()