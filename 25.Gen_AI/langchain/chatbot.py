from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Model
llm = ChatOllama(model="phi3")

# Prompt (IMPORTANT: includes history)
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant.

Rules:
- Answer clearly and concisely
- Use simple language
- If unsure, say "I don't know"
- Avoid unnecessary details
"""),
    ("placeholder", "{history}"),
    ("human", "{question}")
])

# Chain
chain = prompt | llm

# Memory store
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Wrap with memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# Chat loop
while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = chain_with_memory.invoke(
        {"question": user_input},
        config={"configurable": {"session_id": "user1"}}
    )

    print("\nBot:", response.content)

"""
 User input
   ↓
Get history from store
   ↓
Add history to prompt
   ↓
LLM generates answer
   ↓
Save both messages back to store
"""