def get_personality_instruction(mode):

    if mode == "student":
        return "Explain in simple terms suitable for a student."

    elif mode == "interview":
        return "Answer clearly and concisely like in a technical interview."

    elif mode == "research":
        return "Provide a detailed technical explanation."

    else:
        return "Answer in a casual conversational tone."