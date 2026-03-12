import os
import sys
sys.path.append(os.path.abspath("pkt"))

from style_engine.style_prompt_builder import build_style_prompt

from retrieval.note_loader import load_notes
from retrieval.knowledge_graph_builder import build_knowledge_graph
from retrieval.faiss_manager import load_or_build_index
from retrieval.context_ranker import rank_context

from utils.embedder import get_embedding

from memory.memory_manager import load_conversation_memory
from memory.usage_tracker import load_usage_memory
from memory.save_memory import save_memory

from llm.ollama_client import ask_llm



LLM_URL = "http://localhost:11434/api/generate"

INDEX_FILE = "faiss.index"
NOTES_FILE = "notes.pkl"
MEMORY_FILE = "chat_memory.pkl"
USAGE_FILE = "usage_memory.pkl"


# ---------- Load Notes ----------
notes_lines = load_notes()


# ---------- TF-IDF ----------
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(notes_lines)


# ---------- Build Knowledge Graph ----------
G, keyword_frequency, domain_strength, top_keywords_per_chunk = build_knowledge_graph(notes_lines)

print(len(notes_lines))

# ---------- Assign Domain to Chunks ----------
from retrieval.domain_assigner import assign_domains_to_chunks

chunk_domains = assign_domains_to_chunks(top_keywords_per_chunk, domain_strength)



# ---------- Load / Build FAISS ----------
index = load_or_build_index(INDEX_FILE, NOTES_FILE, notes_lines, get_embedding)

print("PKT Assistant Ready (type 'exit' to quit)\n")

style_prompt = build_style_prompt()

# ---------- Load Memory ----------
conversation_history = load_conversation_memory(MEMORY_FILE)

# ---------- Load Usage Memory ----------
usage_memory = load_usage_memory(USAGE_FILE, domain_strength)


# ---------- Chat Loop ----------
while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input.strip():
        print("Please enter a question.\n")
        continue


    top_indices, similarity_score, confidence = rank_context(
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
    )
    best_index = top_indices[0]
    )

    print(f"\nSimilarity score: {similarity_score:.3f}")
    print(f"Confidence level: {confidence}")

    if similarity_score < 0.70:
        print("\nAI: Not found in my notes.")
        print("-" * 50)
        continue

    context = "\n\n".join([notes_lines[i] for i in top_indices])

    ai_answer = ask_llm(context, user_input, LLM_URL)

    print("\nAI:", ai_answer)
    print("-" * 50)

    conversation_history.append({
        "user": user_input,
        "ai": ai_answer
    })

    save_memory(conversation_history, usage_memory, MEMORY_FILE, USAGE_FILE)