from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, FunctionTool

# RAG as a tool
rag_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="company_docs",
    description="Search company documents"
)

# Custom function tool
def calculate(expression: str) -> str:
    """Calculate math expression"""
    return str(eval(expression))

calc_tool = FunctionTool.from_defaults(fn=calculate)

# Create agent
agent = ReActAgent.from_tools(
    tools=[rag_tool, calc_tool],
    llm=llm,
    verbose=True
)

response = agent.chat("What is our revenue and what is 20% of it?")
# Agent:
# Step 1 → searches docs for revenue → finds $1M
# Step 2 → calculates 20% of 1M → $200k
# Step 3 → combines and answers