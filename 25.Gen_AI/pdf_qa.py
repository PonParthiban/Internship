from pypdf import PdfReader
import chromadb,requests
from chromadb.utils import embedding_functions

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text

def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.Client()
collection = client.create_collection(
    name="pdf_data",
    embedding_function=embedding_func
)

# load + chunk
text = load_pdf("file.pdf")
chunks = chunk_text(text)

collection.add(
    documents=chunks,
    ids=[str(i) for i in range(len(chunks))]
)

print("PDF stored ")

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
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

while True:
    query = input("\nAsk: ")

    docs = search(query)

    context = "\n".join(docs)

    prompt = f"""
Answer using only the context below.

Context:
{context}

Question:
{query}
"""

    answer = ask_llm(prompt)

    print("\nAnswer:", answer)