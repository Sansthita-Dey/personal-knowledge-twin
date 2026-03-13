import faiss
import pickle
import numpy as np
from utils.embedder import get_embedding

INDEX_FILE = "chat_index.faiss"
CHUNKS_FILE = "chat_chunks.pkl"

# Load index once
index = faiss.read_index(INDEX_FILE)

# Load stored chat chunks
with open(CHUNKS_FILE, "rb") as f:
    chunks = pickle.load(f)


def retrieve_from_chat(query, top_k=3):

    query_embedding = get_embedding(query)
    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for i, idx in enumerate(indices[0]):
        results.append({
            "text": chunks[idx],
            "source": "chat",
            "score": float(distances[0][i])
        })

    return results