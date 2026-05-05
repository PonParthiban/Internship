# PDF → text → chunks → embeddings → Chroma → search → prompt → HuggingFace API
from pypdf import PdfReader
import chromadb
import requests
from chromadb.utils import embedding_functions
from chromadb.config import Settings

# ============================================
# CONFIG — Put your HuggingFace token here
# ============================================
HF_TOKEN = "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"
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"  # Change model if needed
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# ============================================
# PDF LOADING
# ============================================
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# ============================================
# CHUNKING
# ============================================
def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

# ============================================
# CHROMA SETUP
# ============================================
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

# ============================================
# LOAD & STORE PDF
# ============================================
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

# ============================================
# SEARCH CHROMA
# ============================================
def search(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results["documents"][0]

# ============================================
# HUGGING FACE API  (replaces local Ollama)
# ============================================
def ask_llm(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "return_full_text": False   # Only return new generated text
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    # Handle model still loading
    if response.status_code == 503:
        print("Model is loading on HuggingFace servers, please wait 20 seconds...")
        import time
        time.sleep(20)
        response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"HF API Error {response.status_code}: {response.text}")

    result = response.json()

    # Response is a list for text-generation models
    if isinstance(result, list):
        return result[0].get("generated_text", "No response")
    
    # Some models return dict directly
    if isinstance(result, dict):
        return result.get("generated_text", str(result))

    return str(result)

# ============================================
# MAIN LOOP
# ============================================
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