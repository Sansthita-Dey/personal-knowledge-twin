from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


def cluster_topics(chunks, n_clusters=8):

    vectorizer = TfidfVectorizer(stop_words="english")

    X = vectorizer.fit_transform(chunks)

    model = KMeans(n_clusters=n_clusters, random_state=42)

    labels = model.fit_predict(X)

    clusters = {}

    for i, label in enumerate(labels):

        clusters.setdefault(label, []).append(chunks[i])

    return clusters