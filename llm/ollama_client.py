
import requests
import json


def ask_llm(context, question, LLM_URL):

    full_prompt = f"""
You are an AI assistant answering questions from a knowledge base.

Response style:
{context.split("Style:")[-1] if "Style:" in context else "Provide a clear explanation."}

Follow this reasoning process:

1. Understand the user's question.
2. Identify the relevant concept from the provided context.
3. Provide an answer in the requested style.

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        LLM_URL,
        json={
            "model": "phi3",
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 80,
                "top_p": 0.9,
                "num_ctx": 2048,
                "keep_alive": "30m"
            }
        }
)

    full_answer = ""

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            token = data.get("response", "")
            full_answer += token

    print()

    return full_answer

