#Loader → Splitter → Embeddings → VectorStore → Retriever → Prompt → LLM → Output
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

#Load PDF
loader = PyPDFLoader("file.pdf")
docs = loader.load()

#Split into chunks (better than your manual chunking)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_documents(docs)

#Embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

#Vector DB
db = Chroma.from_documents(chunks, embeddings)

#Retriever
retriever = db.as_retriever(search_kwargs={"k": 3})

#Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant.

Rules:
- Answer ONLY from the context
- If answer not found, say "I don't know"
- Be concise and accurate
"""),
    ("placeholder", "{history}"),
    ("human", "Context:\n{context}\n\nQuestion: {question}")
])

#Model
llm = ChatOllama(model="phi3")

#Chain 
chain = (
    {
        "context": lambda x: retriever.invoke(x["question"]),
        "question": lambda x: x["question"]
    }
    | prompt
    | llm
    | StrOutputParser()
)

#memory
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

#Chat loop
while True:
    query = input("\nAsk (type 'exit'): ")

    if query.lower() == "exit":
        print("Goodbye")
        break

    try:
        answer = chain_with_memory.invoke(
    {"question": query},
    config={"configurable": {"session_id": "user1"}}
     )
        print("\nAnswer:", answer)
    except Exception as e:
        print("\nError:", e)