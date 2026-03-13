import faiss
import pickle
import numpy as np
from utils.embedder import get_embedding

INDEX_FILE = "code_index.faiss"
CHUNKS_FILE = "code_chunks.pkl"

index = faiss.read_index(INDEX_FILE)

with open(CHUNKS_FILE, "rb") as f:
    chunks = pickle.load(f)


def retrieve_from_code(query, top_k=2):

    query_embedding = get_embedding(query)
    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for i, idx in enumerate(indices[0]):
        results.append({
            "text": chunks[idx][:500],
            "source": "code",
            "score": float(distances[0][i])
        })

    return results