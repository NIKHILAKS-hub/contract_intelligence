import os
import json


# ============================================================
# LOAD CLASSIFIED CLAUSES
# ============================================================

def load_classified_clauses(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"\nClassified clauses file not found:\n{file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        clauses = json.load(file)

    if not isinstance(clauses, list):

        raise ValueError(
            "The JSON file must contain a list of clauses."
        )

    return clauses


# ============================================================
# RISK DETECTION FOR ONE CLAUSE
# ============================================================

def detect_risk(clause):

    title = clause.get(
        "title",
        ""
    ).lower()

    category = clause.get(
        "category",
        ""
    )

    text = clause.get(
        "text",
        ""
    ).lower()

    # --------------------------------------------------------
    # DEFAULT RESULT
    # --------------------------------------------------------

    risk = {
        "risk_detected": False,
        "risk_level": "LOW",
        "risk_score": 0,
        "risk_type": "No Significant Risk Detected",
        "reason": "No significant contractual risk identified."
    }

    # ========================================================
    # CAPITAL CONTRIBUTIONS
    # ========================================================

    if category == "Capital Contributions":

        if any(
            phrase in text
            for phrase in [
                "shall not be required",
                "not be required",
                "no capital contribution"
            ]
        ):

            risk = {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 50,
                "risk_type": "Funding Uncertainty",
                "reason": (
                    "The agreement does not require capital "
                    "contributions unless mutually agreed."
                )
            }


    # ========================================================
    # AUTHORITY & GOVERNANCE
    # ========================================================

    elif category == "Authority & Governance":

        if any(
            phrase in text
            for phrase in [
                "written consent",
                "approval of both",
                "consent or approval of both"
            ]
        ):

            risk = {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 50,
                "risk_type": "Joint Approval Requirement",
                "reason": (
                    "Certain actions require approval or "
                    "written consent from both Joint Venturers, "
                    "which may slow decision-making."
                )
            }


    # ========================================================
    # PROFIT & LOSS SHARING
    # ========================================================

    elif category == "Profit & Loss Sharing":

        if "50%" in text:

            risk = {
                "risk_detected": False,
                "risk_level": "LOW",
                "risk_score": 10,
                "risk_type": "Equal Profit/Loss Allocation",
                "reason": (
                    "Income, credits, losses and deductions "
                    "are allocated equally between the parties."
                )
            }


    # ========================================================
    # ACCOUNTING & RECORDS
    # ========================================================

    elif category == "Accounting & Records":

        if any(
            phrase in text
            for phrase in [
                "audited",
                "independent accountant",
                "books and records"
            ]
        ):

            risk = {
                "risk_detected": False,
                "risk_level": "LOW",
                "risk_score": 10,
                "risk_type": "Financial Record Controls",
                "reason": (
                    "The agreement provides for maintenance "
                    "of books and records and permits an "
                    "independent audit under specified conditions."
                )
            }


    # ========================================================
    # TERM & DURATION
    # ========================================================

    elif category == "Term & Duration":

        if any(
            phrase in text
            for phrase in [
                "effective until",
                "scheduled termination",
                "commence",
                "extended by written agreement"
            ]
        ):

            risk = {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 50,
                "risk_type": "Fixed Contract Term",
                "reason": (
                    "The agreement has a defined term and "
                    "requires a written agreement for extension."
                )
            }


    # ========================================================
    # DISTRIBUTIONS
    # ========================================================

    elif category == "Distributions":

        if any(
            phrase in text
            for phrase in [
                "only be made",
                "consent of both",
                "assets are in excess"
            ]
        ):

            risk = {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 40,
                "risk_type": "Distribution Restrictions",
                "reason": (
                    "Distributions are subject to conditions "
                    "and restrictions that may limit access "
                    "to Joint Venture funds."
                )
            }


    # ========================================================
    # TAX & LEGAL STRUCTURE
    # ========================================================

    elif category == "Tax & Legal Structure":

        if any(
            phrase in text
            for phrase in [
                "section 761",
                "subchapter k",
                "income tax purposes"
            ]
        ):

            risk = {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 50,
                "risk_type": "Tax Structure Complexity",
                "reason": (
                    "The agreement contains specific tax "
                    "elections and provisions under the "
                    "Internal Revenue Code."
                )
            }


    # ========================================================
    # TERMINATION & LIQUIDATION
    # ========================================================

    elif category == "Termination & Liquidation":

        if any(
            phrase in text
            for phrase in [
                "termination",
                "debt shall be paid",
                "assets",
                "liquidation"
            ]
        ):

            risk = {
                "risk_detected": True,
                "risk_level": "HIGH",
                "risk_score": 70,
                "risk_type": "Termination & Asset Distribution",
                "reason": (
                    "The clause contains provisions for "
                    "payment of debts and distribution of "
                    "Joint Venture assets following termination."
                )
            }


    # ========================================================
    # TRANSFER & ASSIGNMENT
    # ========================================================

    elif category == "Transfer & Assignment":

        if any(
            phrase in text
            for phrase in [
                "transfer",
                "sell",
                "pledge",
                "mortgage",
                "assignee"
            ]
        ):

            risk = {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 50,
                "risk_type": "Transfer Restrictions",
                "reason": (
                    "A Joint Venturer cannot freely transfer "
                    "or dispose of its interest without the "
                    "consent of the other Joint Venturer."
                )
            }


    # ========================================================
    # NOTICES
    # ========================================================

    elif category == "Notices":

        risk = {
            "risk_detected": False,
            "risk_level": "LOW",
            "risk_score": 5,
            "risk_type": "Notice Procedure",
            "reason": (
                "The agreement specifies acceptable methods "
                "for providing notice."
            )
        }


    # ========================================================
    # GOVERNING LAW
    # ========================================================

    elif category == "Governing Law":

        if "pennsylvania" in text:

            risk = {
                "risk_detected": True,
                "risk_level": "LOW",
                "risk_score": 20,
                "risk_type": "Jurisdiction",
                "reason": (
                    "The agreement is governed by the laws "
                    "of the Commonwealth of Pennsylvania."
                )
            }


    # ========================================================
    # BINDING EFFECT
    # ========================================================

    elif category == "Binding Effect":

        if "successors" in text:

            risk = {
                "risk_detected": False,
                "risk_level": "LOW",
                "risk_score": 5,
                "risk_type": "Binding Effect",
                "reason": (
                    "The agreement extends its binding effect "
                    "to specified successors and assigns."
                )
            }


    # ========================================================
    # EXECUTION & SIGNATURES
    # ========================================================

    elif category == "Execution & Signatures":

        risk = {
            "risk_detected": False,
            "risk_level": "LOW",
            "risk_score": 5,
            "risk_type": "Execution Formalities",
            "reason": (
                "The agreement permits execution in "
                "counterparts and provides signature fields."
            )
        }


    # ========================================================
    # BUSINESS SCOPE
    # ========================================================

    elif category == "Business Scope":

        risk = {
            "risk_detected": False,
            "risk_level": "LOW",
            "risk_score": 10,
            "risk_type": "Business Scope",
            "reason": (
                "The agreement defines the business activities "
                "and products covered by the Joint Venture."
            )
        }


    # ========================================================
    # OFFICE & LOCATION
    # ========================================================

    elif category == "Office & Location":

        risk = {
            "risk_detected": False,
            "risk_level": "LOW",
            "risk_score": 5,
            "risk_type": "Business Location",
            "reason": (
                "The agreement specifies the principal "
                "business location of the Joint Venture."
            )
        }


    # ========================================================
    # JOINT VENTURE IDENTITY
    # ========================================================

    elif category == "Joint Venture Identity":

        risk = {
            "risk_detected": False,
            "risk_level": "LOW",
            "risk_score": 5,
            "risk_type": "Contract Identification",
            "reason": (
                "The clause identifies the Joint Venture "
                "and its principal business location."
            )
        }


    return risk


# ============================================================
# ANALYZE ALL CLAUSES
# ============================================================

def analyze_clauses(clauses):

    results = []

    for clause in clauses:

        risk = detect_risk(
            clause
        )

        result = {

            "clause_number": clause.get(
                "clause_number",
                ""
            ),

            "title": clause.get(
                "title",
                ""
            ),

            "category": clause.get(
                "category",
                "Other"
            ),

            "risk_detected": risk[
                "risk_detected"
            ],

            "risk_level": risk[
                "risk_level"
            ],

            "risk_score": risk[
                "risk_score"
            ],

            "risk_type": risk[
                "risk_type"
            ],

            "reason": risk[
                "reason"
            ],

            "text": clause.get(
                "text",
                ""
            )
        }

        results.append(
            result
        )

    return results


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(
    results,
    output_path
):

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
            results,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(results):

    print("\n" + "=" * 80)
    print("CONTRACT RISK ANALYSIS")
    print("=" * 80)

    for result in results:

        print(
            f"\nClause {result['clause_number']}"
        )

        print(
            f"Title       : {result['title']}"
        )

        print(
            f"Category    : {result['category']}"
        )

        print(
            f"Risk        : {result['risk_detected']}"
        )

        print(
            f"Risk Level  : {result['risk_level']}"
        )

        print(
            f"Risk Score  : {result['risk_score']}"
        )

        print(
            f"Risk Type   : {result['risk_type']}"
        )

        print(
            f"Reason      : {result['reason']}"
        )

        print("-" * 80)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 80)
    print("CONTRACT RISK DETECTOR")
    print("=" * 80)

    file_path = input(
        "\nEnter the path of classified_clauses.json: "
    ).strip()

    try:

        # ----------------------------------------------------
        # LOAD
        # ----------------------------------------------------

        clauses = load_classified_clauses(
            file_path
        )

        print(
            f"\nLoaded {len(clauses)} classified clauses."
        )

        # ----------------------------------------------------
        # ANALYZE
        # ----------------------------------------------------

        results = analyze_clauses(
            clauses
        )

        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        display_results(
            results
        )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        output_path = os.path.join(
            "data",
            "contracts",
            "risk_analysis.json"
        )

        save_results(
            results,
            output_path
        )

        print(
            "\nRisk analysis saved to:"
        )

        print(
            output_path
        )

        print("\n" + "=" * 80)
        print("RISK DETECTION FINISHED")
        print("=" * 80)

    except Exception as e:

        print("\nERROR:")
        print(e)