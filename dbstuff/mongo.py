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

duplicateThreshold = 0.85
searchThreshold = 0.65

#function to add task, set to open by default and timestamp is the moment its created
def addTask(text: str):
    """Add a new task to the to-do list."""
    match = closestTask(text)
    if match and match["score"] >= duplicateThreshold:
        return "not added, duplicate of: " + match["text"]
    else:
        tasks.insert_one({
            "text": text,
            "status": "open",
            "createdAt": datetime.now(),
            "embedding": embed(text),
        })
        return "added: " + text

#grab every task back and print it
def listTasks():
    """List every task on the to-do list."""
    return "\n".join(task["text"] + " (" + task["status"] + ")" for task in tasks.find())

#find the task with this text and set its status to done
def completeTask(text: str):
    """Mark a task as done."""
    match = closestTask(text)
    tasks.update_one({"text": match["text"]}, {"$set": {"status": "done"}})
    return "marked done: " + match["text"]

#find the task with this text and remove it
def deleteTask(text: str):
    """Delete a task from the list."""
    match = closestTask(text)
    tasks.delete_one({"text": match["text"]})
    return "deleted: " + match["text"]

#search tasks by meaning, returns the closest matches with their score
def searchTasks(query: str):
    """Search the to-do list by meaning."""
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
    return "\n".join(task["text"] for task in results if task["score"] >= searchThreshold)

def closestTask(text):
    queryVector = embed(text)
    results = tasks.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": queryVector,
                "numCandidates": 50,
                "limit": 1,
            }
        },
        {
            "$project": {
                "text": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ])
    results = list(results)
    if results:
        return results[0]
    return None

# addTask("walk the dog")
# addTask("send the email")
# completeTask("walk the dog")
# deleteTask("send the email")
# addTask("buy bread")
# listTasks()  

# addTask("buy groceries")
# addTask("phone the dentist")
# searchTasks("something about food")
# addTask("grab some bread")   
# addTask("walk the dog")      

# tasks.delete_many({})     
# addTask("buy milk")
# addTask("walk the dog")
# addTask("buy bread")
# addTask("phone the dentist")
# listTasks()
