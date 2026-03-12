def assign_domains_to_chunks(top_keywords_per_chunk, domain_keywords):

    chunk_domains = []

    for chunk_keywords in top_keywords_per_chunk:
        domain_scores = {}

        for domain, keywords in domain_keywords.items():

            # FIX: ensure keywords is iterable
            if not isinstance(keywords, (list, set, tuple)):
                continue

            overlap = sum(1 for word in chunk_keywords if word in keywords)
            domain_scores[domain] = overlap

        # fallback if dictionary is empty
        if not domain_scores:
            chunk_domains.append("general")
            continue

        best_domain = max(domain_scores, key=domain_scores.get)

        # fallback if no overlap found
        if domain_scores[best_domain] == 0:
            best_domain = "general"

        chunk_domains.append(best_domain)

    return chunk_domains