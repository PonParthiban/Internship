from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful teacher"),
    ("human", "Explain {topic} in simple terms")
])

llm = ChatOllama(model="llama3")

chain = prompt | llm #Prompt → LLM → Output

response = chain.invoke({"topic": "machine learning"})
print(response.content)