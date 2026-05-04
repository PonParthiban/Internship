from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Model
llm = ChatOllama(model="phi3")

# Prompt with system message
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer concisely and clearly."),
    ("human", "{question}")
])

# Chain
chain = prompt | llm

# Chat loop
while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = chain.invoke({"question": user_input})

    print("\nBot:", response.content)