import os
import json
import re
import spacy

nlp = spacy.load("en_core_web_sm")

DATA_PATH = "pkt/data/raw_text"
OUTPUT_PATH = "pkt/style_engine/style_profile.json"

TECH_KEYWORDS = [
    "algorithm", "model", "architecture", "embedding",
    "optimization", "neural", "scaling", "complexity",
    "cloud", "system", "dataset", "analysis"
]

def load_all_text():
    full_text = ""
    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
                full_text += f.read() + " "
    return full_text

def avg_sentence_length(doc):
    lengths = [len(sent.text.split()) for sent in doc.sents]
    return sum(lengths) / len(lengths) if lengths else 0

def vocab_richness(text):
    words = text.split()
    return len(set(words)) / len(words) if words else 0

def emoji_count(text):
    emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    return len(emoji_pattern.findall(text))

def technical_density(text):
    words = text.lower().split()
    count = sum(1 for word in words if word in TECH_KEYWORDS)
    return count / len(words) if words else 0

def detect_format_style(text):
    bullet_count = text.count("- ") + text.count("•")
    return "bullet-heavy" if bullet_count > 10 else "paragraph-driven"

def build_style_profile():
    text = load_all_text()
    print("TEXT LENGTH:", len(text))

    doc = nlp(text)

    profile = {
        "avg_sentence_length": round(avg_sentence_length(doc), 2),
        "vocab_richness": round(vocab_richness(text), 3),
        "emoji_count": emoji_count(text),
        "technical_density": round(technical_density(text), 3),
        "format_preference": detect_format_style(text)
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4)

    print("\n🧠 STYLE PROFILE GENERATED:\n")
    for k, v in profile.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    build_style_profile()