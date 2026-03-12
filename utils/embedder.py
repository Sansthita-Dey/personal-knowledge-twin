import requests
import numpy as np

EMBED_URL = "http://localhost:11434/api/embeddings"


def get_embedding(text):

    response = requests.post(
        EMBED_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    data = response.json()

    if "embedding" not in data or not data["embedding"]:
        raise ValueError("Embedding API returned empty vector.")

    return np.array(data["embedding"]).astype("float32")