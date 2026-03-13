def expand_query(query, graph, max_neighbors=3):

    query = query.lower()
    expanded_terms = set()

    for node in graph.nodes:

        if node in query:

            neighbors = list(graph.neighbors(node))[:max_neighbors]

            for n in neighbors:
                expanded_terms.add(n)

    expanded_query = query + " " + " ".join(expanded_terms)

    return expanded_query