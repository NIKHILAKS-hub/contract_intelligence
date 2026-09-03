import os
import json


# ============================================================
# LOAD CLAUSES
# ============================================================

def load_clauses(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"\nClause file not found:\n{file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        clauses = json.load(file)

    # Make sure JSON contains a list
    if not isinstance(clauses, list):

        raise ValueError(
            "The JSON file does not contain a list of clauses."
        )

    return clauses


# ============================================================
# CLASSIFY ONE CLAUSE
# ============================================================

def classify_clause(clause):

    # Make sure we received one dictionary
    if not isinstance(clause, dict):

        raise ValueError(
            "Each clause must be a dictionary."
        )

    title = clause.get(
        "title",
        ""
    ).lower().strip()

    text = clause.get(
        "text",
        ""
    ).lower()

    # ========================================================
    # TITLE-BASED CLASSIFICATION
    # ========================================================

    # Clause 1
    if "name of the joint venture" in title:

        return "Joint Venture Identity"

    # Clause 2
    if "scope of the joint venture" in title:

        return "Business Scope"

    # Clause 3
    if "capital contribution" in title:

        return "Capital Contributions"

    # Clause 4
    if "office" in title:

        return "Office & Location"

    # Clause 5
    if "powers and authority" in title:

        return "Authority & Governance"

    # Clause 6
    if "division of income and losses" in title:

        return "Profit & Loss Sharing"

    # Clause 7
    if "accounting" in title:

        return "Accounting & Records"

    # Clause 8
    if "term of" in title:

        return "Term & Duration"

    # Clause 9
    if "distribution" in title:

        return "Distributions"

    # Clause 10
    if "internal revenue code" in title:

        return "Tax & Legal Structure"

    # Clause 11
    if (
        "termination" in title
        and "liquidation" in title
    ):

        return "Termination & Liquidation"

    # Clause 12
    if (
        "sale or purchase" in title
        or "interest of joint venturer" in title
    ):

        return "Transfer & Assignment"

    # Clause 13
    if title == "notice" or "notice" in title:

        return "Notices"

    # Clause 14
    if "construction" in title:

        return "Governing Law"

    # Clause 15
    if "benefit" in title:

        return "Binding Effect"

    # Clause 16
    if "counterparts" in title:

        return "Execution & Signatures"


    # ========================================================
    # TEXT-BASED FALLBACK
    # ========================================================

    if any(
        keyword in text
        for keyword in [
            "capital contribution",
            "capital contributions"
        ]
    ):

        return "Capital Contributions"


    if any(
        keyword in text
        for keyword in [
            "books and records",
            "fiscal year",
            "accountant",
            "balance sheet",
            "accounting"
        ]
    ):

        return "Accounting & Records"


    if any(
        keyword in text
        for keyword in [
            "distribution",
            "distributed"
        ]
    ):

        return "Distributions"


    if any(
        keyword in text
        for keyword in [
            "termination",
            "liquidation"
        ]
    ):

        return "Termination & Liquidation"


    if any(
        keyword in text
        for keyword in [
            "transfer",
            "assign",
            "assignee",
            "pledge",
            "mortgage",
            "hypothecate"
        ]
    ):

        return "Transfer & Assignment"


    if any(
        keyword in text
        for keyword in [
            "notice",
            "hand delivered",
            "prepaid mail",
            "fax"
        ]
    ):

        return "Notices"


    if any(
        keyword in text
        for keyword in [
            "laws of",
            "interpreted and construed",
            "governing law"
        ]
    ):

        return "Governing Law"


    # ========================================================
    # DEFAULT
    # ========================================================

    return "Other"


# ============================================================
# CLASSIFY ALL CLAUSES
# ============================================================

def classify_clauses(clauses):

    classified_clauses = []

    for clause in clauses:

        # Classify ONE clause at a time
        category = classify_clause(
            clause
        )

        classified_clause = {

            "clause_number": clause.get(
                "clause_number",
                ""
            ),

            "title": clause.get(
                "title",
                ""
            ),

            "category": category,

            "text": clause.get(
                "text",
                ""
            )
        }

        classified_clauses.append(
            classified_clause
        )

    return classified_clauses


# ============================================================
# SAVE CLASSIFIED CLAUSES
# ============================================================

def save_classified_clauses(
    clauses,
    output_path
):

    # Create directory if necessary
    directory = os.path.dirname(
        output_path
    )

    if directory:

        os.makedirs(
            directory,
            exist_ok=True
        )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            clauses,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(clauses):

    print("\n" + "=" * 75)
    print("CLAUSE CLASSIFICATION RESULTS")
    print("=" * 75)

    for clause in clauses:

        print(
            f"\nClause {clause['clause_number']}"
        )

        print(
            f"Title    : {clause['title']}"
        )

        print(
            f"Category : {clause['category']}"
        )

        print("-" * 75)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 75)
    print("CONTRACT CLAUSE CLASSIFIER")
    print("=" * 75)

    file_path = input(
        "\nEnter the path of extracted_clauses.json: "
    ).strip()

    try:

        # ----------------------------------------------------
        # LOAD
        # ----------------------------------------------------

        clauses = load_clauses(
            file_path
        )

        print(
            f"\nLoaded {len(clauses)} clauses."
        )

        # ----------------------------------------------------
        # CLASSIFY
        # ----------------------------------------------------

        classified_clauses = classify_clauses(
            clauses
        )

        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        display_results(
            classified_clauses
        )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        output_path = os.path.join(
            "data",
            "contracts",
            "classified_clauses.json"
        )

        save_classified_clauses(
            classified_clauses,
            output_path
        )

        print(
            "\nClassified clauses saved to:"
        )

        print(
            output_path
        )

        print("\n" + "=" * 75)
        print("CLAUSE CLASSIFICATION FINISHED")
        print("=" * 75)

    except Exception as e:

        print("\nERROR:")
        print(e)