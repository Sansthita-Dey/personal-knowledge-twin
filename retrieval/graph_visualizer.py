import matplotlib.pyplot as plt
import networkx as nx


def visualize_graph(G, degree_centrality):

    # Filter edges with weight >= 3
    filtered_edges = [(u, v) for u, v, d in G.edges(data=True) if d["weight"] >= 3]
    H = G.edge_subgraph(filtered_edges).copy()

    # Select top 30 nodes
    top_nodes = [node for node, _ in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:30]]
    H = H.subgraph(top_nodes)

    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(H, k=0.5, seed=42)

    node_sizes = [degree_centrality[node] * 4000 for node in H.nodes()]

    nx.draw_networkx_nodes(H, pos, node_size=node_sizes)
    nx.draw_networkx_edges(H, pos, alpha=0.4)
    nx.draw_networkx_labels(H, pos, font_size=9)

    plt.title("Core Knowledge Graph (Filtered & Weighted)")
    plt.axis("off")
    plt.tight_layout()

    plt.savefig("knowledge_graph_clean.png")
    plt.show()

    print("\n🖼 Clean graph saved as knowledge_graph_clean.png")