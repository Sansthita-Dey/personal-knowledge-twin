def build_context(results, max_chunks=5):

    context = ""

    for r in results[:max_chunks]:

        source = r.get("source", "unknown")
        text = r.get("text", "")

        context += f"[SOURCE: {source}]\n"
        context += text
        context += "\n\n"

    return context