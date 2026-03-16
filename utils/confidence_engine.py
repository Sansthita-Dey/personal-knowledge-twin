def compute_confidence(similarity, context_length):

    score = similarity

    if context_length > 1000:
        score += 0.05

    if score > 0.85:
        return "High"

    elif score > 0.65:
        return "Medium"

    return "Low"