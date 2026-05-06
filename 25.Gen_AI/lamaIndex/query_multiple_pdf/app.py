from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

# STEP 1 — Configure HuggingFace
HF_TOKEN = "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"
MODEL_ID  = "meta-llama/Llama-3.1-8B-Instruct"  

# LLM — HuggingFace Inference API
Settings.llm = HuggingFaceInferenceAPI(
    model_name=MODEL_ID,
    token=HF_TOKEN,
    max_new_tokens=512,
    temperature=0.7,
)

# Embedding — runs locally for free
Settings.embed_model = HuggingFaceEmbedding(
    model_name="all-MiniLM-L6-v2"
)

# STEP 2 — Load Documents
docs = SimpleDirectoryReader(
    input_dir="./data",
    required_exts=[".pdf"] 
).load_data()

# STEP 3 — Smart Semantic Chunking
parser = SemanticSplitterNodeParser(
    embed_model=Settings.embed_model,       
    breakpoint_percentile_threshold=95
)
nodes = parser.get_nodes_from_documents(docs)
print(f"Created {len(nodes)} chunks")

# STEP 4 — Build Vector Index
index = VectorStoreIndex(nodes)
print("Index built successfully")


# STEP 5 — Query Engine
query_engine = index.as_query_engine(
    similarity_top_k=3,
    response_mode="compact"
)

# STEP 6 — Chat Loop
print("\nRAG ready! Ask questions about your documents.")
print("Type 'exit' to quit\n")

while True:
    question = input("\nAsk: ").strip()

    if not question:
        continue

    if question.lower() == "exit":
        print("Goodbye!")
        break

    try:
        response = query_engine.query(question)
        print("\nAnswer:", response)

        print("\nSources:")
        for node in response.source_nodes:
            file_name = node.metadata.get('file_name', 'Unknown')
            score = node.score if node.score else 0.0
            print(f"  - {file_name} (score: {score:.2f})")

    except Exception as e:
        print(f"\nError: {e}")