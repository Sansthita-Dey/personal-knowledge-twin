import os
import pickle
import numpy as np
import faiss


def load_or_build_index(INDEX_FILE, NOTES_FILE, notes_lines, get_embedding):

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

    if index is None:
        print("Building FAISS index...\n")

        embeddings = [get_embedding(text) for text in notes_lines]
        embeddings_matrix = np.vstack(embeddings)

        faiss.normalize_L2(embeddings_matrix)

        dimension = embeddings_matrix.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings_matrix)

        faiss.write_index(index, INDEX_FILE)

        with open(NOTES_FILE, "wb") as f:
            pickle.dump(notes_lines, f)

    return index