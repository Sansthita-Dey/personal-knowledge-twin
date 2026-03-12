import numpy as np
import faiss


def rank_context(
    user_input,
    conversation_history,
    index,
    notes_lines,
    vectorizer,
    tfidf_matrix,
    get_embedding,
    chunk_domains,
    domain_strength,
    usage_memory
):

    # ---------- Context Augmentation ----------
    augmented_query = user_input

    if len(user_input.split()) <= 4 and conversation_history:
        last_user_question = conversation_history[-1]["user"]
        augmented_query = last_user_question + " " + user_input

    query_embedding = get_embedding(augmented_query).reshape(1, -1)
    faiss.normalize_L2(query_embedding)

    # ---------- FAISS Search (Top 3) ----------
    similarities, indices = index.search(query_embedding, 3)

    top_indices = indices[0]              # indices of top 3 chunks
    raw_semantic_scores = similarities[0]
    semantic_scores = similarities[0].copy()

    # ---------- TF-IDF ----------
    query_tfidf = vectorizer.transform([augmented_query])
    tfidf_scores_all = (tfidf_matrix @ query_tfidf.T).toarray().flatten()
    tfidf_scores = tfidf_scores_all[top_indices]

    # ---------- Normalize ----------
    semantic_scores = (
        semantic_scores - semantic_scores.min()
    ) / (semantic_scores.max() - semantic_scores.min() + 1e-8)

    tfidf_scores = (
        tfidf_scores - tfidf_scores.min()
    ) / (tfidf_scores.max() - tfidf_scores.min() + 1e-8)

    # ---------- Domain Bias ----------
    domain_bias_scores = []

    max_strength = max(domain_strength.values()) + 1e-8

    for i in top_indices:
        domain = chunk_domains[i]
        bias = domain_strength.get(domain, 0) / max(max_strength, 1)
        domain_bias_scores.append(bias)

    domain_bias_scores = np.array(domain_bias_scores)

    # ---------- Final Score ----------
    final_scores = (
        0.6 * semantic_scores +
        0.25 * tfidf_scores +
        0.15 * domain_bias_scores
    )

    best_local = final_scores.argmax()
    best_index = top_indices[best_local]

    similarity_score = raw_semantic_scores[best_local]

    # ---------- Usage Memory ----------
    best_domain = chunk_domains[best_index]
    usage_memory["domain_counts"][best_domain] = (
        usage_memory["domain_counts"].get(best_domain, 0) + 1
    )

    # ---------- Confidence ----------
    if similarity_score >= 0.80:
        confidence = "High"
    elif similarity_score >= 0.65:
        confidence = "Medium"
    elif similarity_score >= 0.55:
        confidence = "Low"
    else:
        confidence = "Very Low"

    return top_indices, similarity_score, confidence