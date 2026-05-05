#Query Engine: Query engine is the brain of retrieval — decides how to fetch and answer:
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(docs)

# Basic query engine
query_engine = index.as_query_engine()
response = query_engine.query("What is AI?")

# With settings
query_engine = index.as_query_engine(
    similarity_top_k=5,          # fetch top 5 nodes
    response_mode="tree_summarize" # how to synthesize answer
)
#Response Modes
pythonresponse_mode="refine"
# generates answer from chunk 1
# refines answer with chunk 2
# refines again with chunk 3
# best quality, slower

response_mode="compact"
# fits as many chunks as possible into one prompt
# generates one answer
# faster

response_mode="tree_summarize"
# builds tree of summaries
# best for summarization tasks

response_mode="simple_summarize"
# simple and fast
# truncates if too long

#Sub Question Query Engine: Breaks complex question into sub questions:
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool

# Complex question:
# "Compare the revenue of Apple and Google in 2024"
#       ↓
# Sub question 1: "What was Apple's revenue in 2024?"
# Sub question 2: "What was Google's revenue in 2024?"
#       ↓
# Answers combined → final answer

tools = [
    QueryEngineTool.from_defaults(
        query_engine=apple_engine,
        name="apple_docs",
        description="Apple financial documents"
    ),
    QueryEngineTool.from_defaults(
        query_engine=google_engine,
        name="google_docs",
        description="Google financial documents"
    )
]

query_engine = SubQuestionQueryEngine.from_defaults(tools=tools)

response = query_engine.query(
    "Compare revenue of Apple and Google in 2024"
)