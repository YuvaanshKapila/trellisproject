from openai import OpenAI

aiClient = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def embed(text):
    response = aiClient.embeddings.create(model="all-minilm", input=text)
    return response.data[0].embedding

vector = embed("buy milk")
# print(len(vector))
# print(vector[:5])