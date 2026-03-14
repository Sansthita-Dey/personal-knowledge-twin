from rag.retriever import retrieve_context
from llm.ollama_client import ask_llm


def run_rag_pipeline(query):

    context = retrieve_context(query)

    prompt = f"""
You are a helpful AI assistant.

Use the context to answer the question.

Context:
{context}

Question:
{query}

Answer clearly.
"""

    answer = ask_llm(prompt)

    return answer