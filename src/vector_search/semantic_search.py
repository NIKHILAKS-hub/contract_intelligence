import os
import json
import faiss
import numpy as np

from embedding_generator import generate_embedding


VECTOR_DB_DIR = "data/vector_database"

INDEX_PATH = os.path.join(
    VECTOR_DB_DIR,
    "contract_clauses.index"
)

METADATA_PATH = os.path.join(
    VECTOR_DB_DIR,
    "clause_metadata.json"
)


def load_vector_database():
    """
    Load the FAISS index and clause metadata.
    """

    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(
            f"FAISS index not found: {INDEX_PATH}"
        )

    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_PATH}"
        )

    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return index, metadata


def search_clauses(query, top_k=3):
    """
    Search the vector database using semantic similarity.
    """

    index, metadata = load_vector_database()

    # Convert search query into an embedding
    query_embedding = generate_embedding(query)

    # FAISS expects a 2D float32 array
    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    # Don't request more results than available
    top_k = min(top_k, index.ntotal)

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_position in zip(
        distances[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        clause = metadata[index_position]

        results.append({
            "clause_number": clause["clause_number"],
            "title": clause["title"],
            "text": clause["text"],
            "distance": float(distance)
        })

    return results


if __name__ == "__main__":

    print("=" * 70)
    print("CONTRACT SEMANTIC SEARCH")
    print("=" * 70)

    query = input(
        "\nEnter your search query: "
    )

    results = search_clauses(
        query,
        top_k=3
    )

    print("\n" + "=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("-" * 70)

        print(
            f"Clause Number : "
            f"{result['clause_number']}"
        )

        print(
            f"Title         : "
            f"{result['title']}"
        )

        print(
            f"Distance      : "
            f"{result['distance']:.4f}"
        )

        print(
            f"\nClause Text:\n"
            f"{result['text']}"
        )

    print("\n" + "=" * 70)
    print("SEMANTIC SEARCH COMPLETED")
    print("=" * 70)