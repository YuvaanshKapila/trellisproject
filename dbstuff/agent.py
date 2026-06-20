#import chatolama
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent
from mongo import addTask, listTasks, searchTasks, completeTask, deleteTask

llm = ChatOllama(model="qwen3:8b", temperature=0) #you dont want the llm to be creativce when embedding and making to-do tasks

#allows it to call the tools 
tools = [tool(addTask), tool(listTasks), tool(searchTasks), tool(completeTask), tool(deleteTask)]

#make agetn 
agent = create_agent(llm, tools)

while True:
    userInput = input(" ")
    if userInput == "quit":
        break
    result = agent.invoke({"messages": [("user", userInput)]})
    print(result["messages"][-1].content)