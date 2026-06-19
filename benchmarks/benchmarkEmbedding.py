#imports and connection from middleman open ai to llama
import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

#ollama list, just shows all the embedding models that will be benchmarked, small to large
models = [
    "all-minilm",
    "nomic-embed-text",
    "mxbai-embed-large",
    "qwen3-embedding:0.6b",
    "qwen3-embedding:4b",
]

#Each item is a pair of tasks, True means they are really the same task (a duplicate) and False means they are different
testCases = [
    ("buy milk", "grab milk", True),
    ("call mum", "phone my mother", True),
    ("pick up dry cleaning", "get the dry cleaning", True),
    ("finish the report", "complete the report", True),
    ("book a dentist appointment", "schedule a dentist visit", True),
    ("buy milk", "call mum", False),
    ("finish the report", "walk the dog", False),
    ("book flights to Rome", "do the laundry", False),
    ("buy milk", "buy a car", False),
    ("email John about the budget", "email Sarah about lunch", False),
]

#the cutoff, if two tasks score this similar or higher we count them as a duplicate
threshold = 0.7

#takes one piece of text and turns it into its vector, the list of numbers that holds its meaning
def embed(model, text):
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding

#takes two vectors and works out how close they are in meaning, 0 is different and 1 is identical
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    sizeA = sum(x * x for x in a) ** 0.5
    sizeB = sum(y * y for y in b) ** 0.5
    return dot / (sizeA * sizeB)

#runs the whole benchmark for each model, scoring how well it tells duplicates from different tasks
results = []
for model in models:
    print(model)
    embed(model, "hi")  
    score = 0
    dupeSims = []
    nonDupeSims = []
    for textA, textB, expected in testCases:
        sim = cosine(embed(model, textA), embed(model, textB))
        predicted = sim >= threshold
        if predicted == expected:
            score += 1
        if expected:
            dupeSims.append(sim)
        else:
            nonDupeSims.append(sim)
        print("  ", "ok" if predicted == expected else "XX", round(sim, 2), textA, "/", textB)
    accuracy = round(score / len(testCases) * 100, 1)
    avgDupe = round(sum(dupeSims) / len(dupeSims), 2)
    avgNonDupe = round(sum(nonDupeSims) / len(nonDupeSims), 2)
    print("  ", model, accuracy, "% | dupes avg", avgDupe, "| non dupes avg", avgNonDupe)
    results.append({"model": model, "accuracy": accuracy, "dupeAvg": avgDupe, "nonDupeAvg": avgNonDupe})

with open("results2.json", "w") as file:
    json.dump(results, file, indent=2)