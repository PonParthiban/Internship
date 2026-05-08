from llama_index.core.agent import ReActAgent
from llama_index.core.memory import ChatMemoryBuffer

# Create memory system
memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
# Create agent with memory
agent = ReActAgent.from_tools(
    tools=[vector_tool, summary_tool],
    memory=memory,
    verbose=True,
    system_prompt="""
    You are a helpful assistant with access to company documents.
    Remember context from previous conversations.
    Break down complex questions into steps.
    """
)
# Multi-turn conversation
response1 = agent.chat("What are our main products?")
response2 = agent.chat("How do they compare to competitors?")
