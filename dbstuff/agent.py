#import chatolama
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent
from mongo import addTask, listTasks, searchTasks, completeTask, deleteTask

llm = ChatOllama(model="qwen3:8b", temperature=0) #you dont want the llm to be creativce when embedding and making to-do tasks

systemPrompt = """You are a to-do list assistant. Always use the tools to add, list, search, complete, or delete tasks, and base your replies on what the tools return rather than guessing or inventing tasks.
Keep replies short and plain: no emojis, no bold, no filler like "let me know if you need anything". Show tasks simply, one per line."""

#allows it to call the tools 
tools = [tool(addTask), tool(listTasks), tool(searchTasks), tool(completeTask), tool(deleteTask)]

#make agetn 
agent = create_agent(llm, tools, system_prompt=systemPrompt)

def chat(message):
    result = agent.invoke({"messages": [("user", message)]})
    return result["messages"][-1].content

if __name__ == "__main__":
    while True:
        userInput = input("")
        if userInput == "quit":
            break
        print(chat(userInput))