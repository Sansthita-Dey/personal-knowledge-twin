import os
import pickle


def load_conversation_memory(MEMORY_FILE):

    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "rb") as f:
            conversation_history = pickle.load(f)

        print("Loaded previous conversation history.\n")

    else:
        conversation_history = []

    return conversation_history

def compress_conversation(conversation_history, ask_llm, LLM_URL):

    if len(conversation_history) <= 10:
        return conversation_history

    old_messages = conversation_history[:-10]

    summary_text = " ".join(
        msg["user"] + " " + msg["ai"]
        for msg in old_messages
    )

    summary_prompt = f"Summarize the key knowledge from this conversation:\n{summary_text}"

    summary = ask_llm("", summary_prompt, LLM_URL)

    return [
        {"user": "Conversation Summary", "ai": summary}
    ] + conversation_history[-10:]