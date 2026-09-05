from sentence_transformers import SentenceTransformer


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    """
    Convert text into a numerical vector.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    embedding = model.encode(text)

    return embedding


if __name__ == "__main__":

    sample_text = """
    This agreement may be terminated by either party upon thirty days
    written notice to the other party.
    """

    embedding = generate_embedding(sample_text)

    print("=" * 70)
    print("DOCUMENT EMBEDDING TEST")
    print("=" * 70)

    print("\nOriginal text:")
    print(sample_text)

    print("\nEmbedding shape:")
    print(embedding.shape)

    print("\nFirst 10 embedding values:")
    print(embedding[:10])

    print("\nEmbedding generation successful!")