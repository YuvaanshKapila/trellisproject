#imports and connection from middleman open ai to llama
import time
import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

#ollama list, just shows all the models that will be benchmarked
models = [
    "qwen3:8b",
    "qwen3:14b",
    "llama3.1:8b",
    "llama3.2:3b",
    "artcx001/Ministral-8B-Instruct-2410:Q4_K_M",
]

#univeersal system prompt for all the models, gives them the same instructions and tools to use
systemPrompt = (
    "You are a to-do assistant. Use a tool to add, search, complete, or list "
    "tasks. If the user is only chatting, reply without a tool."
)

#takes a tools anme and description and returns the tool format needed for the api
def makeTool(name, description):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {"type": "object", "properties": {}},
        },
    }

#lists the tools/calls the function can use , calls makeTool 4 times to build the four tools needed for the task, addTask, searchTasks, completeTask, listTasks
tools = [
    makeTool("addTask", "Add a new task to the list."),
    makeTool("searchTasks", "Search existing tasks by keyword."),
    makeTool("completeTask", "Mark a task as done."),
    makeTool("listTasks", "List all current tasks."),
]

#Each item is a pair: the prompt on the left, and the tool that should fire on the right. None means the right answer is to call no tool at all.
testCases = [
    ("add buy milk", "addTask"),
    ("remind me to call mum", "addTask"),
    ("add pick up dry cleaning", "addTask"),
    ("what do I have about groceries?", "searchTasks"),
    ("find my work tasks", "searchTasks"),
    ("mark the milk task as done", "completeTask"),
    ("I finished the dry cleaning one", "completeTask"),
    ("show me everything on my list", "listTasks"),
    ("what is on my to-do list", "listTasks"),
    ("hello there", None),
    ("thanks, that is helpful", None),
    ("what can you do?", None),
]

#This is one round trip to one model. It sends the system prompt, the user's prompt, and the tools menu, with temperature 0 so the answer is as consistent as possible.
def ask(model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": prompt},
        ],
        tools=tools,
        temperature=0,
    )
    calls = response.choices[0].message.tool_calls  #see if the model decided to call a tool. If it did, return its name. If not (plain chat), return None.
    if calls:
        return calls[0].function.name
    return None

#runs the whole benchmark for each model, one at a time, scoring each test case and timing the run
results = []
runs = 3

for model in models:
    print(model)
    ask(model, "hi")
    score = 0
    start = time.time()
    for prompt, expected in testCases:
        for r in range(runs):                      #run each prompt a few times to smooth out randomness
            choice = ask(model, prompt)
            if choice == expected:
                score += 1
            print("  ", "ok" if choice == expected else "XX", prompt, "->", choice)
    accuracy = round(score / (len(testCases) * runs) * 100, 1)  
    seconds = round(time.time() - start, 1)
    print("  ", model, accuracy, "%", seconds, "s")
    results.append({"model": model, "accuracy": accuracy, "seconds": seconds})

#save all the results to a file so you have them after the terminal closes
with open("results.json", "w") as file:
    json.dump(results, file, indent=2)