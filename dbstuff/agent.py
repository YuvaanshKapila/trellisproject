#import chatolama
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent
from mongo import addTask, listTasks, searchTasks, completeTask, deleteTask

llm = ChatOllama(model="qwen3:8b", temperature=0) #you dont want the llm to be creativce when embedding and making to-do tasks

systemPrompt = """You are a to-do list assistant. Use the tools to add, list, search, complete, or delete tasks, and base your answers on what the tools return.
You can answer questions about the tasks, like how many there are or summarizing them, using the list the tool gives back.
If the message is not a task action, reply normally without calling a tool.
By default keep replies short and plain, one task per line, but if the user asks for a count, a summary, or a format like a table, give that instead. No emojis, no filler."""
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