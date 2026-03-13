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


def reinforce_memory(usage_memory, domain):

    if "reinforcement" not in usage_memory:
        usage_memory["reinforcement"] = {}

    usage_memory["reinforcement"][domain] = \
        usage_memory["reinforcement"].get(domain, 0) + 1


def prune_memory(usage_memory, threshold=2):

    if "reinforcement" not in usage_memory:
        return

    pruned = {}

    for domain, count in usage_memory["reinforcement"].items():
        if count >= threshold:
            pruned[domain] = count

    usage_memory["reinforcement"] = pruned