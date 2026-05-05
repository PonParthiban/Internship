from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Model
llm = ChatOllama(model="phi3")

# Prompt
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

# Chain with output parser added
chain = prompt | llm | StrOutputParser()

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
print("Chatbot ready! Type 'exit' to quit.")

while True:
    user_input = input("\nYou: ")

    # Handle empty input
    if not user_input.strip():
        print("Please type something!")
        continue

    # Handle exit
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    # Handle errors
    try:
        response = chain_with_memory.invoke(
            {"question": user_input},
            config={"configurable": {"session_id": "user1"}}
        )
        print("\nBot:", response)   # ← no .content needed now

    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure Ollama is running!")

"""User input
   ↓
Get history from store
   ↓
Add history to prompt
   ↓
LLM generates answer
   ↓
Save both messages back to store"""