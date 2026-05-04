#Loader → Splitter → Embeddings → VectorStore → Retriever → Prompt → LLM → Output
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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
prompt = ChatPromptTemplate.from_template(
    """You are a helpful assistant.

Rules:
- Answer ONLY using the context
- If answer not found, say "I don't know"
- Keep answer short and clear

Context:
{context}

Question:
{question}
"""
)

#Model
llm = ChatOllama(model="phi3")

#Chain (THIS replaces your whole logic)
chain = (
    {"context": retriever, "question": lambda x: x}
    | prompt
    | llm
    | StrOutputParser()
)

#Chat loop
while True:
    query = input("\nAsk (type 'exit'): ")

    if query.lower() == "exit":
        print("Goodbye")
        break

    try:
        answer = chain.invoke(query)
        print("\nAnswer:", answer)
    except Exception as e:
        print("\nError:", e)