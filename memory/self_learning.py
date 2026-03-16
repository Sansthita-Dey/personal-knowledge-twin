def update_memory_importance(query, usage_memory):

    query = query.lower()

    for domain in usage_memory:

        if domain in query:

            usage_memory[domain] += 1

    return usage_memory