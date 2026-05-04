from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful teacher"),
    ("human", "Explain {topic} in 3 bullet points")
])

llm = ChatOllama(model="llama3")

parser = StrOutputParser()
#parser = JsonOutputParser()

chain = prompt | llm | parser #Prompt → LLM → Parser → Output

result = chain.invoke({"topic": "machine learning"})
print(result)

#Input → Prompt → Messages → LLM → Raw response → Parser → Clean output