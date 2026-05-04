def generate_prompt(question, context):
    return f"""
You are a helpful assistant.

Rules:
- Answer only using the context
- If answer not found, say "I don't know"
- Keep answer short and clear

Context:
{context}

Question:
{question}

Answer:
"""