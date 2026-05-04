import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import requests

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.Client(
    Settings(persist_directory="./chroma_db")
)

collection = client.get_or_create_collection(
    name="notes",
    embedding_function=embedding_func
)

with open("notes.txt") as f:
    docs = f.readlines()

# clean data
docs = [d.strip() for d in docs if d.strip()]

if collection.count() == 0:
    collection.add(
        documents=docs,
        ids=[str(i) for i in range(len(docs))]
    )
    print("Stored notes ")
else:
    print("Notes already exist ")


def search_notes(query):
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
    query = input("\nAsk (type 'exit'): ")

    if query.lower() == "exit":
        print("Goodbye ")
        break

    docs = search_notes(query)

    # debug: show retrieved docs
    print("\n Retrieved context:")
    for d in docs:
        print("-", d)

    # safety check
    if not docs:
        print("No relevant context found")
        continue

    # build prompt
    context = "\n".join(docs)

    prompt = f"""
You are a helpful assistant.

Answer ONLY using the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}
"""

    try:
        answer = ask_llm(prompt)
        print("\n Answer:", answer)
    except Exception as e:
        print("\n Error:", e)