#VectorStoreIndex:Standard embedding based index — same as LangChain:
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()

response = query_engine.query("What is the refund policy?")
print(response)

#summary index:Creates a summary of entire document first, then searches:
from llama_index.core import SummaryIndex

index = SummaryIndex.from_documents(docs)
query_engine = index.as_query_engine()

# Good for: "summarize this document"
# Good for: questions needing full document context
response = query_engine.query("Summarize the main points")

#Knowledge Graph Index: Stores data as graph of entities and relationships:
from llama_index.core import KnowledgeGraphIndex

index = KnowledgeGraphIndex.from_documents(
    docs,
    max_triplets_per_chunk=5
)

# Automatically extracts:
# "Apple" → "founded by" → "Steve Jobs"
# "Steve Jobs" → "founded" → "Pixar"

query_engine = index.as_query_engine(
    include_text=True,
    response_mode="tree_summarize"
)

response = query_engine.query(
    "What companies did Apple's founder create?"
)

#Tree Index: Builds a tree structure from documents — good for long docs:
from llama_index.core import TreeIndex

index = TreeIndex.from_documents(docs)

# Builds:
#        Root Summary
#       /             \
#   Summary 1      Summary 2
#   /     \        /      \
# chunk1 chunk2  chunk3  chunk4

query_engine = index.as_query_engine()

#Keyword Table Index: Old school keyword based index:
from llama_index.core import KeywordTableIndex

index = KeywordTableIndex.from_documents(docs)

# Stores:
# "refund" → [chunk1, chunk3, chunk7]
# "policy" → [chunk1, chunk2]
# "return" → [chunk1, chunk4]

query_engine = index.as_query_engine()