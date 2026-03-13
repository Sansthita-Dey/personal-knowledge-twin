import pickle
import faiss
import numpy as np
from utils.embedder import get_embedding

CHAT_FILE = "chat_memory.pkl"
INDEX_FILE = "chat_index.faiss"
CHUNKS_FILE = "chat_chunks.pkl"


with open(CHAT_FILE, "rb") as f:
    chats = pickle.load(f)

texts = []

for item in chats:
    text = item["user"] + " " + item["ai"]
    texts.append(text)

print(f"Embedding {len(texts)} chat messages...")

embeddings = []

for text in texts:
    emb = get_embedding(text)
    embeddings.append(emb)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, INDEX_FILE)

with open(CHUNKS_FILE, "wb") as f:
    pickle.dump(texts, f)

print("Chat index built successfully.")