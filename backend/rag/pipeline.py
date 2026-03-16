from rag.retriever import retrieve_context
from llm.ollama_client import ask_llm


def run_rag_pipeline(query, mode="student"):

    context = retrieve_context(query)

    if not context:
        context = "No relevant knowledge found."

    context = context[:1000]

    mode_instruction = {
        "student": "Explain clearly with simple examples.",
        "research": "Provide a detailed and technical explanation.",
        "interview": "Answer concisely like in a technical interview.",
        "casual": "Answer in a friendly conversational tone."
    }

    style = mode_instruction.get(mode, mode_instruction["student"])

    prompt = f"""
You are a helpful AI assistant.

Style:
{style}

Use the context to answer the question.

Context:
{context}

Question:
{query}

Answer clearly.
"""

    answer = ask_llm(prompt)

    return {
        "answer": answer,
        "sources": ["knowledge_base"],
        "confidence": "medium",
        "reason": "Answer generated using retrieved context."
    }