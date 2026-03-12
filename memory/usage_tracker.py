import os
import pickle


def load_usage_memory(USAGE_FILE, domain_keywords):

    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "rb") as f:
            usage_memory = pickle.load(f)

    else:
        usage_memory = {
            "domain_counts": {domain: 0 for domain in domain_keywords}
        }

    return usage_memory