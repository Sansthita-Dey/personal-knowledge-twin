import os

def search_code(query, directory="."):

    results = []

    for root, dirs, files in os.walk(directory):

        for file in files:

            if file.endswith(".py"):

                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:

                        content = f.read()

                        if query.lower() in content.lower():
                            results.append(f"File: {file}\n{content}")

                except:
                    pass


    # If no results found
    if not results:
        return "No matching code found in project files."

    return "\n\n".join(results[:3])