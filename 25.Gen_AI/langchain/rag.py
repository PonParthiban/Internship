from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#load data
loader = TextLoader("data.txt")
docs = loader.load()

#spliting into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

#creating embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

#store vector db
db = Chroma.from_documents(chunks, embeddings)

#this is search engine used to search
retriever = db.as_retriever()

#prompt
prompt = ChatPromptTemplate.from_template(
    """Answer ONLY from the context below:

{context}

Question: {question}
"""
)

#model
llm = ChatOllama(model="llama3")

#this is pipeline 
chain = (
    {"context": retriever, "question": lambda x: x}
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke("What is AI?"))