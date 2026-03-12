import faiss
import numpy as np


def process_query(user_input, conversation_history, index, notes_lines, vectorizer, tfidf_matrix, get_embedding):

    augmented_query = user_input

    # Context augmentation
    if len(user_input.split()) <= 4 and conversation_history:
        last_user_question = conversation_history[-1]["user"]
        augmented_query = last_user_question + " " + user_input

    query_embedding = get_embedding(augmented_query).reshape(1, -1)
    faiss.normalize_L2(query_embedding)

    similarities, indices = index.search(query_embedding, len(notes_lines))

    raw_semantic_scores = similarities[0]
    semantic_scores = similarities[0].copy()

    query_tfidf = vectorizer.transform([augmented_query])
    tfidf_scores = (tfidf_matrix @ query_tfidf.T).toarray().flatten()

    semantic_scores = (semantic_scores - semantic_scores.min()) / (semantic_scores.max() - semantic_scores.min() + 1e-8)
    tfidf_scores = (tfidf_scores - tfidf_scores.min()) / (tfidf_scores.max() - tfidf_scores.min() + 1e-8)

    return augmented_query, indices, semantic_scores, tfidf_scores, raw_semantic_scores