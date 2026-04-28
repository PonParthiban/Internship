import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from openai import OpenAI

# -------------------------
# 1. Setup embedding model
# -------------------------
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# -------------------------
# 2. Persistent DB (IMPORTANT)
# -------------------------
client = chromadb.Client(
    Settings(persist_directory="./chroma_db")
)

collection = client.get_or_create_collection(
    name="notes",
    embedding_function=embedding_func
)

# -------------------------
# 3. Load and clean notes
# -------------------------
with open("notes.txt") as f:
    docs = f.readlines()

docs = [d.strip() for d in docs if d.strip()]

# -------------------------
# 4. Add data (avoid duplicates)
# -------------------------
if collection.count() == 0:
    collection.add(
        documents=docs,
        ids=[str(i) for i in range(len(docs))]
    )
    print("Stored notes ✅")
else:
    print("Notes already exist ✅")

# -------------------------
# 5. Search function
# -------------------------
def search_notes(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results["documents"][0]

# -------------------------
# 6. LLM setup
# -------------------------
client_llm = OpenAI()
client_llm = OpenAI(api_key="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")
def ask_llm(question, context_docs):
    context = "\n".join(context_docs)

    prompt = f"""
You are a helpful assistant.

Answer ONLY using the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""

    response = client_llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# -------------------------
# 7. Main loop
# -------------------------
while True:
    query = input("\nAsk (type 'exit'): ")

    if query.lower() == "exit":
        print("Goodbye 👋")
        break

    docs = search_notes(query)

    print("\n🔍 Retrieved context:")
    for d in docs:
        print("-", d)

    try:
        answer = ask_llm(query, docs)
        print("\n🤖 Answer:", answer)
    except Exception as e:
        print("\n❌ Error:", e)