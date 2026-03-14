def search_pdf(query, vector_store, k=5):

    results = vector_store.similarity_search(query, k=k)

    context = []

    for doc in results:
        context.append(doc.page_content)

    return "\n\n".join(context)