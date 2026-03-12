import pickle


def save_memory(conversation_history, usage_memory, MEMORY_FILE, USAGE_FILE):

    with open(MEMORY_FILE, "wb") as f:
        pickle.dump(conversation_history, f)

    with open(USAGE_FILE, "wb") as f:
        pickle.dump(usage_memory, f)