import os
import requests
import numpy as np
import pickle
import faiss

LLM_URL = "http://localhost:11434/api/generate"
EMBED_URL = "http://localhost:11434/api/embeddings"

INDEX_FILE = "faiss.index"
NOTES_FILE = "notes.pkl"


# ---------- Load Notes ----------
from pypdf import PdfReader


def load_notes(folder="notes", chunk_size=500):
    documents = []

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)

        if not os.path.isfile(filepath):
            continue

        ext = filename.lower().split(".")[-1]

        text = ""

        # ---------- TXT ----------
        if ext == "txt":
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

        # ---------- Markdown ----------
        elif ext == "md":
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

        # ---------- Python Code ----------
        elif ext == "py":
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

        # ---------- PDF ----------
        elif ext == "pdf":
            reader = PdfReader(filepath)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        # ---------- Chunking ----------
        if text:
            text = text.replace("\n", " ").strip()

            for i in range(0, len(text), chunk_size):
                chunk = text[i:i + chunk_size]
                documents.append(chunk)

    return documents


# ---------- Get Embedding ----------
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


# ---------- Load Notes ----------
notes_lines = load_notes()


# ---------- Initialize / Load FAISS ----------
if os.path.exists(INDEX_FILE) and os.path.exists(NOTES_FILE):
    print("Loading FAISS index...\n")
    index = faiss.read_index(INDEX_FILE)

    with open(NOTES_FILE, "rb") as f:
        stored_notes = pickle.load(f)

    if stored_notes != notes_lines:
        print("Notes changed. Rebuilding index...\n")
        os.remove(INDEX_FILE)
        os.remove(NOTES_FILE)
        index = None
else:
    index = None


# ---------- Build Index If Needed ----------
if index is None:
    print("Building FAISS index...\n")

    embeddings = [get_embedding(text) for text in notes_lines]
    embeddings_matrix = np.vstack(embeddings)

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings_matrix)

    dimension = embeddings_matrix.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings_matrix)

    faiss.write_index(index, INDEX_FILE)

    with open(NOTES_FILE, "wb") as f:
        pickle.dump(notes_lines, f)

print("PKT Assistant Ready (type 'exit' to quit)\n")


# ---------- Chat Loop ----------
conversation_history = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input.strip():
        print("Please enter a question.\n")
        continue

    # ---------- Context Augmentation ----------
    augmented_query = user_input
    if len(user_input.split()) <= 4 and conversation_history:
        last_user_question = conversation_history[-1]["user"]
        augmented_query = last_user_question + " " + user_input

    query_embedding = get_embedding(augmented_query).reshape(1, -1)
    faiss.normalize_L2(query_embedding)

    # ---------- FAISS Search ----------
    similarities, indices = index.search(query_embedding, 3)
    similarity_score = similarities[0][0]

    # ---------- Confidence ----------
    if similarity_score >= 0.80:
        confidence = "High"
    elif similarity_score >= 0.65:
        confidence = "Medium"
    elif similarity_score >= 0.55:
        confidence = "Low"
    else:
        confidence = "Very Low"

    print(f"\nSimilarity score: {similarity_score:.3f}")
    print(f"Confidence level: {confidence}")

    # ---------- Simple Rejection ----------
    if similarity_score < 0.55:
        print("\nAI: Not found in my notes.")
        print("-" * 50)
        continue

    # ---------- Retrieve Context ----------
    top_matches = [notes_lines[i] for i in indices[0]]
    context = "\n".join(top_matches)

    # ---------- Memory ----------
    recent_memory = conversation_history[-4:]
    memory_text = ""
    for turn in recent_memory:
        memory_text += f"User: {turn['user']}\nAI: {turn['ai']}\n"

    full_prompt = f"""
You are a Personal Knowledge Twin.

You must ONLY use the NOTES below.
If the answer is not explicitly contained in NOTES, respond:
Not found in my notes.

Conversation:
{memory_text}

NOTES:
{context}

QUESTION:
{user_input}

Answer:
"""

    response = requests.post(
        LLM_URL,
        json={
            "model": "phi3",
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 100
            }
        }
    )

    result = response.json()
    ai_answer = result.get("response", "No response from model.")

    print("\nAI:", ai_answer)
    print("-" * 50)

    conversation_history.append({
        "user": user_input,
        "ai": ai_answer
    })