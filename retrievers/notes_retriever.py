
import pickle
import numpy as np
import requests
from config import EMBED_URL, EMBED_MODEL

NOTES_FILE = "notes.pkl"


def get_embedding(text):

    response = requests.post(
        EMBED_URL,
        json={
            "model": EMBED_MODEL,
            "prompt": text
        }
    )

    return np.array(response.json()["embedding"]).astype("float32")


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_from_notes(query, top_k=3):

    try:
        with open(NOTES_FILE, "rb") as f:
            notes = pickle.load(f)
    except:
        return []

    query_embedding = get_embedding(query)

    scored = []

    for note in notes:

        emb = get_embedding(note)

        score = cosine_similarity(query_embedding, emb)

        scored.append({
            "text": note,
            "source": "notes",
            "score": float(score)
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:top_k]

