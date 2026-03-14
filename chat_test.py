import os
import sys
import time

sys.path.append(os.path.abspath("pkt"))

from style_engine.style_prompt_builder import build_style_prompt

from retrieval.note_loader import load_notes
from retrieval.knowledge_graph_builder import build_knowledge_graph
from retrieval.faiss_manager import load_or_build_index
from retrieval.domain_assigner import assign_domains_to_chunks
from retrieval.query_engine import run_query_pipeline

from utils.embedder import get_embedding
from utils.personality import get_personality_instruction
from utils.output_formatter import print_sources, print_reflection

from memory.memory_manager import load_conversation_memory, compress_conversation
from memory.usage_tracker import load_usage_memory, reinforce_memory
from memory.save_memory import save_memory

from llm.ollama_client import ask_llm
from config import LLM_URL

from sklearn.feature_extraction.text import TfidfVectorizer

from agent.tool_router import choose_tool
from tools.code_search import search_code
from tools.python_runner import run_python
from tools.web_search import search_web

INDEX_FILE = "faiss.index"
NOTES_FILE = "notes.pkl"
MEMORY_FILE = "chat_memory.pkl"
USAGE_FILE = "usage_memory.pkl"

# Toggle extra retrieval sources
USE_EXTRA_SOURCES = True


# ---------- Load Notes ----------
notes_lines = load_notes()


# ---------- TF-IDF ----------
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(notes_lines)


# ---------- Build Knowledge Graph ----------
G, keyword_frequency, domain_strength, top_keywords_per_chunk = build_knowledge_graph(notes_lines)

print("Loaded chunks:", len(notes_lines))


# ---------- Assign Domains ----------
chunk_domains = assign_domains_to_chunks(top_keywords_per_chunk, domain_strength)


# ---------- Load / Build FAISS ----------
index = load_or_build_index(INDEX_FILE, NOTES_FILE, notes_lines, get_embedding)

print("PKT Assistant Ready (type 'exit' to quit)\n")


# ---------- Style Prompt ----------
style_prompt = build_style_prompt()


# ---------- Load Memory ----------
conversation_history = load_conversation_memory(MEMORY_FILE)


# ---------- Load Usage Memory ----------
usage_memory = load_usage_memory(USAGE_FILE, domain_strength)


# ===============================
# CHAT LOOP
# ===============================

while True:

    mode = input("Mode (student/interview/research/casual): ").lower()

    personality_instruction = get_personality_instruction(mode)

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input.strip():
        print("Please enter a question.\n")
        continue


    # ---------- Tool Router ----------
    tool = choose_tool(user_input)


    # ---------- Run Tool If Needed ----------
    if tool == "code":

        context = search_code(user_input)

        result = {
            "context": context,
            "source_details": [
                {
                    "chunk": "tool",
                    "domain": "code",
                    "preview": "Code search tool result"
                }
            ],
            "reflection_source": "Code Tool",
            "reflection_reason": "Code search tool used",
            "confidence": "High",
            "similarity": 1.0
        }

    elif tool == "python":

        context = run_python(user_input)

        result = {
            "context": context,
            "source_details": [
                {
                    "chunk": "tool",
                    "domain": "python",
                    "preview": "Python execution tool"
                }
            ],
            "reflection_source": "Python Tool",
            "reflection_reason": "Python code executed",
            "confidence": "High",
            "similarity": 1.0
        }

    elif tool == "web":

        context = search_web(user_input)

        result = {
            "context": context,
            "source_details": [
                {
                    "chunk": "tool",
                    "domain": "web",
                    "preview": "Web search tool"
                }
            ],
            "reflection_source": "Web Tool",
            "reflection_reason": "Web tool used",
            "confidence": "Medium",
            "similarity": 1.0
        }

    else:

        # ---------- Run Retrieval Pipeline ----------
        result = run_query_pipeline(
            user_input,
            G,
            conversation_history,
            index,
            notes_lines,
            vectorizer,
            tfidf_matrix,
            get_embedding,
            chunk_domains,
            domain_strength,
            usage_memory,
            reinforce_memory,
            USE_EXTRA_SOURCES
        )


    if result is None:
        print("\nAI: Not found in my notes.")
        print("-" * 50)
        continue

    context = result["context"]

    # Limit context size for faster LLM response
    context = context[:3000]

    source_details = result["source_details"]

    reflection_source = result["reflection_source"]
    reflection_reason = result["reflection_reason"]
    reflection_confidence = result["confidence"]


    # ---------- Source Ranking ----------
    source_rankings = ["Notes"]

    if result["similarity"] > 0.60 and USE_EXTRA_SOURCES:
        source_rankings.append("External Sources")

    if conversation_history:
        source_rankings.append("Chat Memory")


    # ---------- Debug Info ----------
    print(f"\nSimilarity score: {result['similarity']:.3f}")
    print(f"Confidence level: {result['confidence']}")

    print("Context length:", len(context))


    # ---------- Ask LLM ----------
    start_llm = time.time()

# Skip LLM if tool already answered
    if result["reflection_source"] in ["Python Tool", "Code Tool", "Web Tool"]:

      ai_answer = context
      end_llm = time.time()

    else:

        ai_answer = ask_llm(
        context + "\n\nStyle: " + personality_instruction,
        user_input,
        LLM_URL
    )

    end_llm = time.time()

    print("LLM response time:", round(end_llm - start_llm, 2), "seconds")

    print("\nAI:", ai_answer)


    # ---------- Output ----------
    print_sources(source_rankings, source_details)

    print_reflection(
        reflection_source,
        reflection_reason,
        reflection_confidence
    )


    # ---------- Save Conversation ----------
    conversation_history.append({
        "user": user_input,
        "ai": ai_answer
    })


    # ---------- Context Compression ----------
    conversation_history = compress_conversation(
        conversation_history,
        ask_llm,
        LLM_URL
    )


    # ---------- Save Memory ----------
    save_memory(
        conversation_history,
        usage_memory,
        MEMORY_FILE,
        USAGE_FILE
    )