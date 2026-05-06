# PDF → text → chunks → embeddings → Chroma → search → prompt → HuggingFace API
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os


load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found! Add it to .env file")


hf_client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3", 
    token=HF_TOKEN
)

# PDF LOADING
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


# CHUNKING
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

# CHROMA SETUP
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

chroma_client = chromadb.Client(
    Settings(persist_directory="./chroma_db")
)

collection = chroma_client.get_or_create_collection(
    name="pdf_data",
    embedding_function=embedding_func
)

# LOAD & STORE PDF
text = load_pdf("file.pdf")

if not text.strip():
    print("No text extracted from PDF")
    exit()

chunks = chunk_text(text)

if collection.count() == 0:
    collection.add(
        documents=chunks,
        ids=[str(i) for i in range(len(chunks))]
    )
    print("PDF stored in ChromaDB")
else:
    print("Data already exists (skipped adding)")

# SEARCH CHROMA
def search(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results["documents"][0]

# ASK LLM
def ask_llm(prompt):
    response = hf_client.text_generation(
        prompt,                     # ✅ passes actual prompt not hardcoded text
        max_new_tokens=512,
        temperature=0.7,
        repetition_penalty=1.1
    )
    return response

# MAIN LOOP
while True:
    query = input("\nAsk (type 'exit'): ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    docs = search(query)

    if not docs:
        print("No relevant context found")
        continue

    print("\nRetrieved context:")
    for d in docs:
        print("-", d[:100], "...")

    context = "\n".join(docs)

    prompt = f"""You are a helpful assistant.

Rules:
- Answer ONLY using the context below
- If answer not found, say "I don't know"
- Keep answer short and clear

Context:
{context}

Question:
{query}

Answer:"""

    try:
        answer = ask_llm(prompt)
        print("\nAnswer:", answer)
    except Exception as e:
        print("\nError:", e)