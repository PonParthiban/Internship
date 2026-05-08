import json
from datetime import datetime
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.prompts import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from dotenv import load_dotenv
import os


# STEP 1 — Configure HuggingFace
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found! Add it to .env file")

MODEL_ID  = "meta-llama/Llama-3.1-8B-Instruct"  

Settings.llm = HuggingFaceInferenceAPI(
    model_name=MODEL_ID,
    token=HF_TOKEN,
    max_new_tokens=512,
    temperature=0.7,
)

"""Settings.embed_model = HuggingFaceEmbedding(
    model_name="all-MiniLM-L6-v2"
)"""

Settings.embed_model = HuggingFaceEmbedding(
    model_name="all-mpnet-base-v2"  # stronger
)


# STEP 2 — Load Documents
docs = SimpleDirectoryReader(
    input_dir="./data",
    required_exts=[".pdf"] 
).load_data()

# STEP 3 — Smart Semantic Chunking
parser = SemanticSplitterNodeParser(
    embed_model=Settings.embed_model,       
    breakpoint_percentile_threshold=85 #Lower threshold = smaller, more focused chunks = better matching.
)
nodes = parser.get_nodes_from_documents(docs)
print(f"Created {len(nodes)} chunks")

# STEP 4 — Build Vector Index
index = VectorStoreIndex(nodes)
print("Index built successfully")

# STEP 5 — PROMPT
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

# STEP 6 — Query Engine
query_engine = index.as_query_engine(
    similarity_top_k=3,
    response_mode="compact",
    text_qa_template=qa_prompt_template 
)

# STEP 7 — LOGGING SETUP (Silent - No Printing)
class RAGLogger:
    """Logs all RAG interactions silently"""
    
    def __init__(self, log_file="rag_logs.json"):
        self.log_file = log_file
        self.logs = []
    
    def log_query(self, question, retrieved_chunks, model_answer):
        """Log a single query and response (silent)"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": question,
            "retrieved_information": {
                "total_chunks": len(retrieved_chunks),
                "chunks": [
                    {
                        "file": chunk.metadata.get('file_name', 'Unknown'),
                        "content": chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text,
                        "similarity_score": float(chunk.score) if chunk.score else 0.0
                    }
                    for chunk in retrieved_chunks
                ]
            },
            "model_response": str(model_answer),
            "response_length": len(str(model_answer))
        }
        
        self.logs.append(log_entry)
        self.save_logs()  # Save silently
    
    def save_logs(self):
        """Save logs to JSON file (no print)"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)

# Initialize logger
logger = RAGLogger("rag_logs.json")

# STEP 8 — Chat Loop (Only prints answer and sources, not logs)
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
        # Query the RAG system
        response = query_engine.query(question)
        
        # Log silently (no print)
        logger.log_query(
            question=question,
            retrieved_chunks=response.source_nodes,
            model_answer=response
        )
        
        # Only print the answer
        print("\nAnswer:", response)

        # Print sources
        print("\nSources:")
        for node in response.source_nodes:
            file_name = node.metadata.get('file_name', 'Unknown')
            score = node.score if node.score else 0.0
            print(f"  - {file_name} (score: {score:.2f})")

    except Exception as e:
        print(f"\nError: {e}")
        
        # Log errors silently too
        error_log = {
            "timestamp": datetime.now().isoformat(),
            "query": question,
            "error": str(e)
        }
        logger.logs.append(error_log)
        logger.save_logs()