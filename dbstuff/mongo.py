import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from embeddings import embed

#find the .env file
envPath = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(envPath)
#connect to the mongo cluster
client = MongoClient(os.environ["MONGO_URI"])
#creates db and collection 
db = client["todo"]
tasks = db["tasks"]
#function to add task, set to open by default and timestamp is the moment its created
def addTask(text):
    tasks.insert_one({
        "text": text,
        "status": "open",
        "createdAt": datetime.now(),
        "embedding": embed(text),
    })

#grab every task back and print it
def listTasks():
    for task in tasks.find():
        print(task)

#find the task with this text and set its status to done
def completeTask(text):
    tasks.update_one({"text": text}, {"$set": {"status": "done"}})

#find the task with this text and remove it
def deleteTask(text):
    tasks.delete_one({"text": text})

def searchTasks(query):
    queryVector = embed(query)
    results = tasks.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": queryVector,
                "numCandidates": 50,
                "limit": 5,
            }
        },
        {
            "$project": {
                "text": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ])
    for task in results:
        print(round(task["score"], 2), task["text"])
        
# addTask("walk the dog")
# addTask("send the email")
# completeTask("walk the dog")
# deleteTask("send the email")
# addTask("buy bread")
# listTasks()  