#PDF → text → chunks → embeddings → Chroma → search → prompt → LLM
from pypdf import PdfReader
import chromadb
import requests
from chromadb.utils import embedding_functions
from chromadb.config import Settings

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.Client(
    Settings(persist_directory="./chroma_db")
)

collection = client.get_or_create_collection(
    name="pdf_data",
    embedding_function=embedding_func
)

text = load_pdf("file.pdf")

if not text.strip():
    print(" No text extracted from PDF")
    exit()

chunks = chunk_text(text)

if collection.count() == 0:
    collection.add(
        documents=chunks,
        ids=[str(i) for i in range(len(chunks))]
    )
    print(" PDF stored")
else:
    print(" Data already exists (skipped adding)")

def search(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results["documents"][0]

def ask_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",   # lighter model (better for your RAM)
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


while True:
    query = input("\nAsk (type 'exit'): ")

    if query.lower() == "exit":
        print("Goodbye ")
        break

    docs = search(query)

    if not docs:
        print("No relevant context found")
        continue

    print("\n Retrieved context:")
    for d in docs:
        print("-", d[:100], "...")

    context = "\n".join(docs)

    prompt = f"""
You are a helpful assistant.

Rules:
- Answer ONLY using the context
- If answer not found, say "I don't know"
- Keep answer short and clear

Context:
{context}

Question:
{query}

Answer:
"""
    try:
        answer = ask_llm(prompt)
        print("\n Answer:", answer)
    except Exception as e:
        print("\n Error:", e)