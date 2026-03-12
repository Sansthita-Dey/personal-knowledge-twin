from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from collections import Counter
import networkx as nx
import itertools
import pickle


def build_knowledge_graph(notes_lines):

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(notes_lines)

    feature_names = np.array(vectorizer.get_feature_names_out())

    # ---------- Extract Keywords ----------
    top_keywords_per_chunk = []

    for row in tfidf_matrix:
        row_array = row.toarray().flatten()
        top_indices = row_array.argsort()[-10:]
        top_keywords = feature_names[top_indices]
        top_keywords_per_chunk.append(top_keywords)

    # ---------- Keyword Frequency ----------
    all_keywords = [word for chunk in top_keywords_per_chunk for word in chunk]
    keyword_frequency = Counter(all_keywords)

    dominant_keywords = keyword_frequency.most_common(20)

    print("\n🧠 Top Dominant Keywords:")
    for word, freq in dominant_keywords:
        print(f"{word}: {freq}")

    # ---------- Domain Strength ----------
    domain_keywords = {
        "DBMS": ["database", "dbms", "normalization", "sql", "transaction", "relation"],
        "OS": ["process", "thread", "allocation", "deadlock", "scheduling", "memory", "time"],
        "AI_ML": ["learning", "model", "neural", "dataset", "training", "classification"],
        "Cloud": ["cloud", "virtualization", "scaling", "aws", "azure", "gcp"]
    }

    domain_strength = {}

    for domain, keywords in domain_keywords.items():
        score = sum(keyword_frequency.get(word, 0) for word in keywords)
        domain_strength[domain] = score

    print("\n📊 Domain Strength Scores:")
    for domain, score in domain_strength.items():
        print(f"{domain}: {score}")

    # ---------- Knowledge Graph ----------
    G = nx.Graph()

    for chunk_keywords in top_keywords_per_chunk:
        for w1, w2 in itertools.combinations(chunk_keywords, 2):
            if G.has_edge(w1, w2):
                G[w1][w2]["weight"] += 1
            else:
                G.add_edge(w1, w2, weight=1)

    print("\n🧠 Knowledge Graph Built")
    print("Total Nodes:", G.number_of_nodes())
    print("Total Edges:", G.number_of_edges())

    # ---------- Centrality ----------
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    top_between = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]

    print("\n🔥 Top Degree Central Concepts:")
    for node, score in top_degree:
        print(f"{node}: {score:.4f}")

    print("\n🔥 Top Betweenness Central Concepts:")
    for node, score in top_between:
        print(f"{node}: {score:.4f}")

    # ---------- Save Graph ----------
    with open("knowledge_graph.gpickle", "wb") as f:
        pickle.dump(G, f)

    print("\n💾 Graph saved as knowledge_graph.gpickle")

    return G, keyword_frequency, domain_strength, top_keywords_per_chunk