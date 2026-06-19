import os
from dotenv import load_dotenv
from pymongo import MongoClient

envPath = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(envPath)

client = MongoClient(os.environ["MONGO_URI"])

db = client["todo"]
tasks = db["tasks"]

tasks.insert_one({"text": "buy milk", "status": "open"})

for task in tasks.find():
    print(task)