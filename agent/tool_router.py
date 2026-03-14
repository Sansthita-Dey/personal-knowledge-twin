def choose_tool(query):

    q = query.lower()

    if "calculate" in q or "python" in q:
        return "python"

    elif "code" in q or "function" in q or "bug" in q:
        return "code"

    elif "web" in q or "internet" in q:
        return "web"

    else:
        return "pdf"