import os
from dotenv import load_dotenv
from pymongo import MongoClient
#find the .env file
envPath = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(envPath)
#connect to the mongo cluster
client = MongoClient(os.environ["MONGO_URI"])

db = client["todo"]
tasks = db["tasks"]

tasks.insert_one({"text": "buy milk", "status": "open"})
#grab every task back and print it

for task in tasks.find():
    print(task)