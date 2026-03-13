import json

PROFILE_PATH = "pkt/style_engine/style_profile.json"


def build_style_prompt():

    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        profile = json.load(f)

    avg_len = profile["avg_sentence_length"]
    tech_density = profile["technical_density"]
    format_pref = profile["format_preference"]
    vocab = profile["vocab_richness"]

    instructions = []

    # Sentence style
    if avg_len > 18:
        instructions.append("Use detailed explanations with longer sentences.")
    else:
        instructions.append("Keep explanations concise and clear.")

    # Technical tone
    if tech_density > 0.15:
        instructions.append("Use technical terminology and precise definitions.")

    # Vocabulary richness
    if vocab > 0.4:
        instructions.append("Use varied vocabulary while keeping explanations clear.")

    # Formatting preference
    if format_pref == "bullet-heavy":
        instructions.append("Prefer bullet points when listing concepts or steps.")
    else:
        instructions.append("Explain concepts in paragraph form.")

    prompt = f"""
You are the Personal Knowledge Twin of Sansthita.

Your goal is to answer questions using the same writing style found in the user's notes.

Style Guidelines:
{" ".join(instructions)}

Always explain concepts clearly, using examples when useful.
"""

    return prompt


if __name__ == "__main__":
    print(build_style_prompt())