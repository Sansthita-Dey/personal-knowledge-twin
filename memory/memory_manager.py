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