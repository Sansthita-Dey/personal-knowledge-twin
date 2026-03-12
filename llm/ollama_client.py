import requests


def ask_llm(context, question, LLM_URL):

    full_prompt = f"""
You are a strict extraction system.

Extract ONLY information from NOTES that answers the QUESTION.
If not clearly present, respond exactly:
Not found in my notes.

NOTES:
{context}

QUESTION:
{question}

Answer:
"""

    response = requests.post(
        LLM_URL,
        json={
            "model": "phi3:latest",
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": 90
            }
        }
    )

    result = response.json()

    return result.get("response", "No response from model.")