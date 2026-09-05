import os
import json
import numpy as np
import faiss

from embedding_generator import generate_embedding


# Folder where the vector database will be stored
VECTOR_DB_DIR = "data/vector_database"

INDEX_PATH = os.path.join(VECTOR_DB_DIR, "contract_clauses.index")
METADATA_PATH = os.path.join(VECTOR_DB_DIR, "clause_metadata.json")


def create_vector_database(clauses):
    """
    Generate embeddings for contract clauses
    and store them in a FAISS vector database.
    """

    if not clauses:
        raise ValueError("No clauses provided.")

    embeddings = []
    metadata = []

    print("\nGenerating embeddings...")

    for i, clause in enumerate(clauses):

        # Support different possible clause formats
        if isinstance(clause, dict):
            text = clause.get("text", "")
            clause_number = clause.get("clause_number", str(i + 1))
            title = clause.get("title", f"Clause {i + 1}")
        else:
            text = str(clause)
            clause_number = str(i + 1)
            title = f"Clause {i + 1}"

        if not text.strip():
            continue

        print(f"Embedding clause {clause_number}...")

        embedding = generate_embedding(text)

        embeddings.append(embedding)

        metadata.append({
            "clause_number": clause_number,
            "title": title,
            "text": text
        })

    if not embeddings:
        raise ValueError("No valid clause text found.")

    # Convert embeddings to NumPy array
    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS index
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    # Add embeddings to the index
    index.add(embeddings)

    # Create directory
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, INDEX_PATH)

    # Save clause metadata
    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 70)
    print("VECTOR DATABASE CREATED")
    print("=" * 70)

    print(f"\nNumber of clauses : {len(metadata)}")
    print(f"Vector dimension   : {dimension}")
    print(f"FAISS index        : {INDEX_PATH}")
    print(f"Metadata file      : {METADATA_PATH}")

    return index, metadata


if __name__ == "__main__":

    # Simple test clauses
    test_clauses = [
        {
            "clause_number": "1",
            "title": "Termination",
            "text": """
            Either party may terminate this agreement upon thirty days
            written notice to the other party.
            """
        },
        {
            "clause_number": "2",
            "title": "Confidentiality",
            "text": """
            The parties shall maintain the confidentiality of all
            proprietary and confidential information.
            """
        },
        {
            "clause_number": "3",
            "title": "Payment",
            "text": """
            The consultant shall receive payment for services provided
            under this agreement.
            """
        }
    ]

    create_vector_database(test_clauses)