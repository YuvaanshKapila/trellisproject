#import chatolama
from langchain_ollama import ChatOllama
llm = ChatOllama(model="qwen3:8b", temperature=0) #you dont want the llm to be creativce when embedding and making to-do tasks

response = llm.invoke("say hello in one short sentence")
print(response.content)
