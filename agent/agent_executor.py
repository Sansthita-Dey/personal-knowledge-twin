from tools.pdf_search import search_pdf
from tools.code_search import search_code
from tools.python_runner import run_python
from tools.web_search import search_web
from agent.tool_router import choose_tool


def run_agent(query, vector_store):

    tool = choose_tool(query)

    if tool == "pdf":

        context = search_pdf(query, vector_store)

    elif tool == "code":

        context = search_code(query)

    elif tool == "python":

        context = run_python(query)

    elif tool == "web":

        context = search_web(query)

    else:

        context = ""

    return context