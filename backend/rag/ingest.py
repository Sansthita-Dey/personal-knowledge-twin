import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# project directories
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
KNOWLEDGE_DIR = os.path.join(ROOT_DIR, "knowledge")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)


# -----------------------------
# Load PDFs
# -----------------------------
def load_pdfs(folder):

    texts = []

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            path = os.path.join(folder, file)
            reader = PdfReader(path)

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    texts.append(text)

    return texts


# -----------------------------
# Chunk text
# -----------------------------
def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


# -----------------------------
# Build document list
# -----------------------------
raw_texts = load_pdfs(KNOWLEDGE_DIR)

documents = []

for text in raw_texts:
    documents.extend(chunk_text(text))


if len(documents) == 0:
    print("⚠️ No documents found in knowledge folder.")
    exit()


# -----------------------------
# Create embeddings
# -----------------------------
embeddings = model.encode(documents)


# -----------------------------
# Create FAISS index
# -----------------------------
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


# -----------------------------
# Save FAISS + documents
# -----------------------------
index_path = os.path.join(DATA_DIR, "vector_store.index")
doc_path = os.path.join(DATA_DIR, "documents.pkl")

faiss.write_index(index, index_path)

with open(doc_path, "wb") as f:
    pickle.dump(documents, f)


print("Knowledge base built successfully.")
print(f"Indexed {len(documents)} chunks.")