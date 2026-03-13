
import faiss
import pickle
import numpy as np
import requests
from config import EMBED_URL, EMBED_MODEL

# Load FAISS index and embeddings once
index = faiss.read_index("faiss.index")

with open("embeddings.pkl", "rb") as f:
    data = pickle.load(f)

texts = data["notes"]
embeddings = np.array(data["embeddings"]).astype("float32")


def get_embedding(text):
    response = requests.post(
        EMBED_URL,
        json={
            "model": EMBED_MODEL,
            "prompt": text
        }
    )

    return np.array(response.json()["embedding"]).astype("float32")


def retrieve_from_pdf(query, top_k=5):

    query_embedding = get_embedding(query)
    query_embedding = np.expand_dims(query_embedding, axis=0)

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for i, idx in enumerate(indices[0]):

        results.append({
            "text": texts[idx],
            "source": "pdf",
            "score": float(distances[0][i])
        })

    return results

