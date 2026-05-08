from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.prompts import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

# STEP 1 — Configure HuggingFace
HF_TOKEN = "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"
MODEL_ID  = "meta-llama/Llama-3.1-8B-Instruct"  

Settings.llm = HuggingFaceInferenceAPI(
    model_name=MODEL_ID,
    token=HF_TOKEN,
    max_new_tokens=512,
    temperature=0.7,
)

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

# STEP 5 — CREATE CUSTOM PROMPT ✅
qa_prompt_template = PromptTemplate("""
You are a helpful AI assistant answering questions based on documents.

Context information is below:
---------------------
{context_str}
---------------------

Based ONLY on the context above, answer the following question:
{query_str}

If the answer is not in the context, say "I don't know" instead of making up information.
Provide a clear and concise answer.
""")

# STEP 6 — Query Engine with Custom Prompt
query_engine = index.as_query_engine(
    similarity_top_k=3,
    response_mode="compact",
    text_qa_template=qa_prompt_template  # ← add custom prompt here
)

# STEP 7 — Chat Loop
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