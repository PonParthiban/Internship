import chromadb
from chromadb.utils import embedding_functions

# create client
client = chromadb.Client()

# use sentence-transformers (no ONNX download issue)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# create collection
collection = client.create_collection(
    name="test",
    embedding_function=embedding_func
)

# add data
collection.add(
    documents=[
        "Flask is a web framework",
        "ChromaDB is a vector database",
        "LLM is used in AI"
    ],
    ids=["1", "2", "3"]
)

# query
results = collection.query(
    query_texts=["What is llm "],
    n_results=1
)

print(results)