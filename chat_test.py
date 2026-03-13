
import os
import sys
import time
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
from config import LLM_URL

from retrieval.query_expander import expand_query
from retrieval.multi_source_retriever import retrieve_all_sources
from retrieval.context_builder import build_context


INDEX_FILE = "faiss.index"
NOTES_FILE = "notes.pkl"
MEMORY_FILE = "chat_memory.pkl"
USAGE_FILE = "usage_memory.pkl"

# Toggle for multi-source retrieval
USE_EXTRA_SOURCES = False


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

    mode = input("Mode (student/interview/research/casual): ").lower()

    if mode == "student":
        personality_instruction = "Explain in simple terms suitable for a student."

    elif mode == "interview":
        personality_instruction = "Answer clearly and concisely like in a technical interview."

    elif mode == "research":
     personality_instruction = "Provide a detailed technical explanation."

    else:
        personality_instruction = "Answer in a casual conversational tone."
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input.strip():
        print("Please enter a question.\n")
        continue

    # Query expansion
    expanded_query = expand_query(user_input, G)

    # Context ranking
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

    # Limit to top 3 chunks (important for speed)
    top_indices = top_indices[:3]

    best_index = top_indices[0]
    best_domain = chunk_domains[best_index]

    from memory.usage_tracker import reinforce_memory
    reinforce_memory(usage_memory, best_domain)

    print(f"\nSimilarity score: {similarity_score:.3f}")
    print(f"Confidence level: {confidence}")

    # Determine source ranking
    source_rankings = ["Notes"]

    if similarity_score > 0.60 and similarity_score <= 0.80:
        source_rankings.append("External Sources")

    if conversation_history:
        source_rankings.append("Chat Memory")

    # Reflection info
    reflection_source = "Notes"
    reflection_reason = "Semantic similarity match"
    reflection_confidence = confidence

    


    # ---------- Build Notes Context ----------


    # Create a short summary of recent conversation
    conversation_summary = ""

    if len(conversation_history) > 5:
        last_messages = conversation_history[-5:]
        summary_text = " ".join([msg["user"] for msg in last_messages])
        conversation_summary = f"Recent conversation topics: {summary_text}"
        notes_context = "\n\n".join(notes_lines[i][:400] for i in top_indices)


    # ---------- Adaptive Retrieval ----------

    if similarity_score > 0.80:
         # High confidence → use notes only
        context = conversation_summary + "\n\n" + notes_context

    elif similarity_score > 0.60:
        # Medium confidence → expand with extra sources
        extra_results = retrieve_all_sources(user_input)
        extra_context = build_context(extra_results)
        context = conversation_summary + "\n\n" + notes_context + "\n\n" + extra_context
        reflection_source = "Notes + External Sources"
        reflection_reason = "Partial similarity, expanded retrieval"

    else:
    # Low confidence → not found
        print("\nAI: Not found in my notes.")
        print("-" * 50)
        continue

        

    # ---------- Ask LLM ----------
    print("Context length:", len(context))
    start_llm = time.time()

    ai_answer = ask_llm(context + "\n\nStyle: " + personality_instruction, user_input, LLM_URL)

    end_llm = time.time()
    print("LLM response time:", round(end_llm - start_llm, 2), "seconds")

    print("\nAI:", ai_answer)
    print("\nSource Ranking:")
for i, src in enumerate(source_rankings, 1):
    print(f"{i}. {src}")
    print("\nReflection:")
    print("Source:", reflection_source)
    print("Reason:", reflection_reason)
    print("Confidence:", reflection_confidence)
    print("-" * 50)


    # ---------- Save Conversation ----------
    conversation_history.append({
        "user": user_input,
        "ai": ai_answer
    })
    # Keep only last 10 interactions (Context Compression)
    conversation_history = conversation_history[-10:]

    save_memory(conversation_history, usage_memory, MEMORY_FILE, USAGE_FILE)

