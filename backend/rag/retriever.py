import faiss
import pickle
import os
import numpy as np
from sentence_transformers import SentenceTransformer

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")

index_path = os.path.join(DATA_DIR, "vector_store.index")
doc_path = os.path.join(DATA_DIR, "documents.pkl")

index = None
documents = []

if os.path.exists(index_path) and os.path.exists(doc_path):
    index = faiss.read_index(index_path)

    with open(doc_path, "rb") as f:
        documents = pickle.load(f)
else:
    print("⚠️ FAISS index not found. Retrieval disabled.")

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_context(query, k=2):

    if index is None:
        return "No knowledge base loaded yet."

    # embed query
    query_embedding = model.encode([query])

    # search FAISS
    distances, indices = index.search(np.array(query_embedding), k)

    # get valid documents
    results = [documents[i] for i in indices[0] if i != -1]

    if not results:
        return "No relevant knowledge found."

    # combine context
    context = "\n\n".join(results)

    return context