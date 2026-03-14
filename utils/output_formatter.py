def print_sources(source_rankings, source_details):
    
    print("\nSource Ranking:")

    for i, src in enumerate(source_rankings, 1):
        print(f"{i}. {src}")

    print("\nSource Details:")

    for s in source_details:
        print(f"Chunk {s['chunk']} | Domain: {s['domain']}")
        print("Preview:", s["preview"])
        print()

def print_reflection(source, reason, confidence):

    print("Reflection:")
    print("Source:", source)
    print("Reason:", reason)
    print("Confidence:", confidence)
    print("-" * 50)