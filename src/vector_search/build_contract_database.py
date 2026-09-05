import os
import json
import numpy as np
import faiss

from src.data_processing.document_parser import extract_text, clean_text
from src.clause_extraction.clause_extractor import extract_clauses
from src.clause_classification.clause_classifier import classify_clauses
from src.vector_search.embedding_generator import generate_embedding


# Your contract repository
CONTRACT_DIR = "data/contracts"

# Where the vector database will be stored
VECTOR_DB_DIR = "data/vector_database"

INDEX_PATH = os.path.join(
    VECTOR_DB_DIR,
    "contract_repository.index"
)

METADATA_PATH = os.path.join(
    VECTOR_DB_DIR,
    "contract_metadata.json"
)


def process_contract(pdf_path):
    """
    Process one PDF and return its classified clauses.
    """

    print(f"\nProcessing: {os.path.basename(pdf_path)}")

    # 1. Extract text
    raw_text = extract_text(pdf_path)

    # 2. Clean text
    cleaned_text = clean_text(raw_text)

    # 3. Extract clauses
    clauses = extract_clauses(cleaned_text)

    # 4. Classify clauses
    classified_clauses = classify_clauses(clauses)

    return classified_clauses


def build_database():

    if not os.path.exists(CONTRACT_DIR):
        raise FileNotFoundError(
            f"Contract directory not found: {CONTRACT_DIR}"
        )

    pdf_files = [
        file for file in os.listdir(CONTRACT_DIR)
        if file.lower().endswith(".pdf")
    ]

    if not pdf_files:
        raise ValueError(
            f"No PDF files found in {CONTRACT_DIR}"
        )

    print("=" * 70)
    print("BUILDING CONTRACT VECTOR DATABASE")
    print("=" * 70)

    print(f"\nContracts found: {len(pdf_files)}")

    embeddings = []
    metadata = []

    for pdf_file in pdf_files:

        pdf_path = os.path.join(
            CONTRACT_DIR,
            pdf_file
        )

        try:

            clauses = process_contract(pdf_path)

            print(
                f"Clauses extracted: {len(clauses)}"
            )

            for clause in clauses:

                # Get clause text
                text = clause.get("text", "")

                if not text.strip():
                    continue

                print(
                    f"  Embedding clause "
                    f"{clause.get('clause_number', 'N/A')}"
                )

                embedding = generate_embedding(text)

                embeddings.append(embedding)

                metadata.append({
                    "filename": pdf_file,
                    "clause_number": clause.get(
                        "clause_number"
                    ),
                    "title": clause.get(
                        "title"
                    ),
                    "text": text
                })

        except Exception as e:

            print(
                f"ERROR processing {pdf_file}: {e}"
            )

    if not embeddings:
        raise ValueError(
            "No clause embeddings were generated."
        )

    # Convert embeddings to NumPy
    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    # Get embedding dimension
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)

    # Add vectors
    index.add(embeddings)

    # Create database directory
    os.makedirs(
        VECTOR_DB_DIR,
        exist_ok=True
    )

    # Save FAISS index
    faiss.write_index(
        index,
        INDEX_PATH
    )

    # Save metadata
    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 70)
    print("CONTRACT VECTOR DATABASE CREATED")
    print("=" * 70)

    print(
        f"\nContracts processed : {len(pdf_files)}"
    )

    print(
        f"Clauses indexed     : {len(metadata)}"
    )

    print(
        f"Vector dimension    : {dimension}"
    )

    print(
        f"\nFAISS index:"
        f"\n{INDEX_PATH}"
    )

    print(
        f"\nMetadata:"
        f"\n{METADATA_PATH}"
    )

    print("\n" + "=" * 70)
    print("BUILD COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    build_database()