conversation_history = []

def add_message(role, content):

    conversation_history.append({
        "role": role,
        "content": content
    })

    if len(conversation_history) > 10:
        conversation_history.pop(0)


def get_history():

    history = ""

    for msg in conversation_history:
        history += f"{msg['role']}: {msg['content']}\n"

    return history