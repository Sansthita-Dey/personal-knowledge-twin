from retrievers.pdf_retriever import retrieve_from_pdf
from retrievers.chat_retriever import retrieve_from_chat
from retrievers.notes_retriever import retrieve_from_notes
from retrievers.code_retriever import retrieve_from_code


def retrieve_all_sources(query):

    results = []

    try:
        pdf_results = retrieve_from_pdf(query)
        results.extend(pdf_results)
    except:
        pass

    try:
        chat_results = retrieve_from_chat(query)
        results.extend(chat_results)
    except:
        pass

    try:
        notes_results = retrieve_from_notes(query)
        results.extend(notes_results)
    except:
        pass

    try:
        code_results = retrieve_from_code(query)
        results.extend(code_results)
    except:
        pass

    # sort by score
    results.sort(key=lambda x: x["score"], reverse=True)

    return results