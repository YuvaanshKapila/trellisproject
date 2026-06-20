import os
import discord
import requests
from dotenv import load_dotenv

#loads env
envPath = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(envPath)

#lets the bot read what people type
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
#ignore the bots own messages so it doesnt reply to itself
    if message.author == client.user:
        return
    #send the text to the agent api, reply with the answer
    response = requests.post("http://localhost:8000/chat", json={"message": message.content})
    await message.channel.send(response.json()["reply"])
    
client.run(os.environ["DISCORD_TOKEN"])