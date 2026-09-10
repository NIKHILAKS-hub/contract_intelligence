# src/vector_search/semantic_search.py

import os
import json
import faiss
import numpy as np

from src.vector_search.embedding_generator import generate_embedding


VECTOR_DB_DIR = "data/vector_database"

INDEX_PATH = os.path.join(
    VECTOR_DB_DIR,
    "contract_repository.index"
)

METADATA_PATH = os.path.join(
    VECTOR_DB_DIR,
    "contract_metadata.json"
)


def load_vector_database():

    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(
            f"FAISS index not found: {INDEX_PATH}"
        )

    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_PATH}"
        )

    index = faiss.read_index(INDEX_PATH)

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        metadata = json.load(file)

    return index, metadata


def search_clauses(query, top_k=3):

    if not query or not query.strip():
        raise ValueError(
            "Search query cannot be empty."
        )

    index, metadata = load_vector_database()

    query_embedding = generate_embedding(query)

    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

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
            "filename": clause.get("filename"),
            "clause_number": clause.get("clause_number"),
            "title": clause.get("title"),
            "text": clause.get("text"),
            "distance": float(distance)
        })

    return results


def search_uploaded_clauses(
    clauses,
    query,
    top_k=3
):

    if not clauses:
        raise ValueError(
            "No clauses available for semantic search."
        )

    if not query or not query.strip():
        raise ValueError(
            "Search query cannot be empty."
        )

    valid_clauses = []

    for clause in clauses:

        text = clause.get("text", "")

        if text and text.strip():
            valid_clauses.append(clause)

    if not valid_clauses:
        raise ValueError(
            "No valid clause text found."
        )

    embeddings = []

    for clause in valid_clauses:

        embedding = generate_embedding(
            clause["text"]
        )

        embeddings.append(embedding)

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    query_embedding = generate_embedding(
        query
    )

    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    top_k = min(
        top_k,
        index.ntotal
    )

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

        clause = valid_clauses[
            index_position
        ]

        results.append({
            "clause_number": clause.get(
                "clause_number"
            ),
            "title": clause.get(
                "title"
            ),
            "text": clause.get(
                "text"
            ),
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

    for i, result in enumerate(
        results,
        start=1
    ):

        print(f"\nResult {i}")
        print("-" * 70)

        print(
            f"File          : "
            f"{result['filename']}"
        )

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