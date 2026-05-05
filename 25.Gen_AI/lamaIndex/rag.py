from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings



# Step 1 — Configure models globally
Settings.llm = Ollama(model="phi3")
Settings.embed_model = OllamaEmbedding(model="nomic-embed-text")

# Step 2 — Load documents
docs = SimpleDirectoryReader("./data").load_data()

# Step 3 — Smart chunking
parser = SemanticSplitterNodeParser(
    embed_model=Settings.embed_model
)
nodes = parser.get_nodes_from_documents(docs)

# Step 4 — Build index
index = VectorStoreIndex(nodes)

# Step 5 — Query engine
query_engine = index.as_query_engine(
    similarity_top_k=3,
    response_mode="compact"
)



# Step 6 — Chat loop
while True:
    question = input("\nAsk: ")
    if question == "exit":
        break
    response = query_engine.query(question)
    print("\nAnswer:", response)
    print("\nSources:")
    for node in response.source_nodes:
        print(f"  - {node.metadata['file_name']} (score: {node.score:.2f})")