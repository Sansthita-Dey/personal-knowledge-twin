from retrieval.query_expander import expand_query
from retrieval.context_ranker import rank_context
from retrieval.multi_source_retriever import retrieve_all_sources
from retrieval.context_builder import build_context


def run_query_pipeline(
    user_input,
    G,
    conversation_history,
    index,
    notes_lines,
    vectorizer,
    tfidf_matrix,
    get_embedding,
    chunk_domains,
    domain_strength,
    usage_memory,
    reinforce_memory,
    USE_EXTRA_SOURCES
):

    expanded_query = expand_query(user_input, G)

    top_indices, similarity_score, confidence = rank_context(
        expanded_query,
        conversation_history,
        index,
        notes_lines,
        vectorizer,
        tfidf_matrix,
        get_embedding,
        chunk_domains,
        domain_strength,
        usage_memory
    )

    top_indices = top_indices[:3]

    best_index = top_indices[0]
    best_domain = chunk_domains[best_index]

    reinforce_memory(usage_memory, best_domain)

    conversation_summary = ""

    if len(conversation_history) > 5:
        last_messages = conversation_history[-5:]
        summary_text = " ".join(msg["user"] for msg in last_messages)
        conversation_summary = f"Recent conversation topics: {summary_text}"

    notes_context = "\n\n".join(notes_lines[i][:250] for i in top_indices)

    if similarity_score > 0.80:

        context = conversation_summary + "\n\n" + notes_context
        reflection_source = "Notes"
        reflection_reason = "High semantic similarity"

    elif similarity_score > 0.60 and USE_EXTRA_SOURCES:

        extra_results = retrieve_all_sources(user_input)
        extra_context = build_context(extra_results)

        context = conversation_summary + "\n\n" + notes_context + "\n\n" + extra_context

        reflection_source = "Notes + External Sources"
        reflection_reason = "Medium similarity — expanded retrieval"

    else:
        return None

    source_details = []

    for idx in top_indices:
        source_details.append({
            "chunk": idx,
            "domain": chunk_domains[idx],
            "preview": notes_lines[idx][:120]
        })

    return {
        "context": context,
        "similarity": similarity_score,
        "confidence": confidence,
        "source_details": source_details,
        "reflection_source": reflection_source,
        "reflection_reason": reflection_reason
    }