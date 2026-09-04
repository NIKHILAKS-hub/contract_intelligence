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
# DEFAULT RISK
# ============================================================

def default_risk():

    return {
        "risk_detected": False,
        "risk_level": "LOW",
        "risk_score": 0,
        "risk_type": "No Significant Risk Detected",
        "reason": "No significant contractual risk identified."
    }


# ============================================================
# RISK DETECTION FOR ONE CLAUSE
# ============================================================

def detect_risk(clause):

    title = clause.get(
        "title",
        ""
    ).lower().strip()

    text = clause.get(
        "text",
        ""
    ).lower()

    category = clause.get(
        "category",
        ""
    )

    risk = default_risk()


    # ========================================================
    # 1. TERMINATION
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "termination",
            "liquidation",
            "termination and liquidation"
        ]
    ):

        return {
            "risk_detected": True,
            "risk_level": "HIGH",
            "risk_score": 70,
            "risk_type": "Termination & Asset Distribution",
            "reason": (
                "The clause contains provisions governing "
                "termination, payment of obligations, and "
                "distribution or liquidation of assets."
            )
        }


    # ========================================================
    # 2. RESTRICTIVE COVENANTS
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "restrictive covenant",
            "restrictive covenants",
            "non-compete",
            "non compete",
            "non-solicit",
            "non solicit"
        ]
    ):

        return {
            "risk_detected": True,
            "risk_level": "HIGH",
            "risk_score": 75,
            "risk_type": "Restrictive Covenants",
            "reason": (
                "The clause imposes restrictions on activities "
                "such as competition, solicitation, or other "
                "post-contract conduct."
            )
        }


    # ========================================================
    # 3. INDEMNIFICATION
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "indemnification",
            "indemnity",
            "indemnification and liability"
        ]
    ):

        return {
            "risk_detected": True,
            "risk_level": "HIGH",
            "risk_score": 70,
            "risk_type": "Indemnification Exposure",
            "reason": (
                "The clause contains indemnification obligations "
                "that may create financial exposure for a party."
            )
        }


    # ========================================================
    # 4. LIMITATION OF LIABILITY
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "limitation of liability",
            "limitation on liability",
            "liability"
        ]
    ):

        if any(
            keyword in text
            for keyword in [
                "liable",
                "liability",
                "damages",
                "consequential damages",
                "indirect damages"
            ]
        ):

            return {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 60,
                "risk_type": "Liability Exposure",
                "reason": (
                    "The clause contains provisions governing "
                    "liability or damages and may limit or "
                    "increase financial exposure."
                )
            }


    # ========================================================
    # 5. CONFIDENTIALITY
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "confidentiality",
            "confidential information",
            "non-disclosure",
            "nondisclosure"
        ]
    ):

        return {
            "risk_detected": True,
            "risk_level": "MEDIUM",
            "risk_score": 45,
            "risk_type": "Confidentiality Obligation",
            "reason": (
                "The clause creates obligations relating to "
                "the protection and disclosure of confidential "
                "information."
            )
        }


    # ========================================================
    # 6. INTELLECTUAL PROPERTY
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "intellectual property",
            "proprietary rights",
            "ownership of intellectual property",
            "copyright",
            "patent"
        ]
    ):

        return {
            "risk_detected": True,
            "risk_level": "MEDIUM",
            "risk_score": 55,
            "risk_type": "Intellectual Property Rights",
            "reason": (
                "The clause governs ownership, use, or rights "
                "associated with intellectual property."
            )
        }


    # ========================================================
    # 7. PAYMENT / COMPENSATION
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "payment",
            "compensation",
            "fees",
            "fee",
            "remuneration"
        ]
    ):

        return {
            "risk_detected": True,
            "risk_level": "MEDIUM",
            "risk_score": 45,
            "risk_type": "Payment Obligation",
            "reason": (
                "The clause establishes financial obligations "
                "or payment terms that may affect the parties."
            )
        }


    # ========================================================
    # 8. CAPITAL CONTRIBUTIONS
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

            return {
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
    # 9. AUTHORITY / GOVERNANCE
    # ========================================================

    if category == "Authority & Governance":

        if any(
            phrase in text
            for phrase in [
                "written consent",
                "approval of both",
                "consent or approval of both",
                "unanimous consent"
            ]
        ):

            return {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 50,
                "risk_type": "Joint Approval Requirement",
                "reason": (
                    "Certain actions require approval or "
                    "consent from multiple parties, which "
                    "may slow decision-making."
                )
            }


    # ========================================================
    # 10. PROFIT & LOSS
    # ========================================================

    if category == "Profit & Loss Sharing":

        if "50%" in text:

            return {
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
    # 11. ACCOUNTING
    # ========================================================

    if category == "Accounting & Records":

        if any(
            phrase in text
            for phrase in [
                "audited",
                "independent accountant",
                "books and records"
            ]
        ):

            return {
                "risk_detected": False,
                "risk_level": "LOW",
                "risk_score": 10,
                "risk_type": "Financial Record Controls",
                "reason": (
                    "The agreement provides for maintenance "
                    "of financial records and accounting controls."
                )
            }


    # ========================================================
    # 12. TERM / DURATION
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "term",
            "duration",
            "renewal"
        ]
    ):

        if any(
            phrase in text
            for phrase in [
                "effective until",
                "scheduled termination",
                "extended by written agreement",
                "automatic renewal",
                "renewal"
            ]
        ):

            return {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 50,
                "risk_type": "Contract Duration",
                "reason": (
                    "The clause establishes a defined contract "
                    "term or renewal condition."
                )
            }


    # ========================================================
    # 13. DISTRIBUTIONS
    # ========================================================

    if category == "Distributions":

        if any(
            phrase in text
            for phrase in [
                "only be made",
                "consent of both",
                "assets are in excess"
            ]
        ):

            return {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 40,
                "risk_type": "Distribution Restrictions",
                "reason": (
                    "Distributions are subject to conditions "
                    "or restrictions that may limit access "
                    "to funds."
                )
            }


    # ========================================================
    # 14. TAX
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "tax",
            "internal revenue",
            "tax election"
        ]
    ):

        return {
            "risk_detected": True,
            "risk_level": "MEDIUM",
            "risk_score": 50,
            "risk_type": "Tax Structure Complexity",
            "reason": (
                "The clause contains tax-related elections "
                "or obligations that may require specialized "
                "review."
            )
        }


    # ========================================================
    # 15. TRANSFER / ASSIGNMENT
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "transfer",
            "assignment",
            "sale or purchase",
            "interest of joint venturer"
        ]
    ):

        if any(
            phrase in text
            for phrase in [
                "transfer",
                "assign",
                "assignee",
                "pledge",
                "mortgage",
                "sell"
            ]
        ):

            return {
                "risk_detected": True,
                "risk_level": "MEDIUM",
                "risk_score": 50,
                "risk_type": "Transfer Restrictions",
                "reason": (
                    "The clause restricts the ability of a "
                    "party to transfer, assign, sell, or "
                    "otherwise dispose of its contractual interest."
                )
            }


    # ========================================================
    # 16. DISPUTE RESOLUTION
    # ========================================================

    if any(
        keyword in title
        for keyword in [
            "dispute",
            "dispute resolution",
            "arbitration",
            "mediation",
            "litigation"
        ]
    ):

        return {
            "risk_detected": True,
            "risk_level": "MEDIUM",
            "risk_score": 50,
            "risk_type": "Dispute Resolution",
            "reason": (
                "The clause establishes procedures or "
                "requirements for resolving contractual disputes."
            )
        }


    # ========================================================
    # 17. GOVERNING LAW
    # ========================================================

    if category == "Governing Law":

        return {
            "risk_detected": True,
            "risk_level": "LOW",
            "risk_score": 20,
            "risk_type": "Jurisdiction",
            "reason": (
                "The agreement specifies the applicable "
                "governing law or jurisdiction."
            )
        }


    # ========================================================
    # 18. NOTICES
    # ========================================================

    if category == "Notices":

        return {
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
    # 19. BINDING EFFECT
    # ========================================================

    if category == "Binding Effect":

        return {
            "risk_detected": False,
            "risk_level": "LOW",
            "risk_score": 5,
            "risk_type": "Binding Effect",
            "reason": (
                "The agreement specifies the parties or "
                "successors to whom the agreement is binding."
            )
        }


    # ========================================================
    # 20. EXECUTION
    # ========================================================

    if category == "Execution & Signatures":

        return {
            "risk_detected": False,
            "risk_level": "LOW",
            "risk_score": 5,
            "risk_type": "Execution Formalities",
            "reason": (
                "The agreement provides execution and "
                "signature formalities."
            )
        }


    # ========================================================
    # 21. DEFAULT BUSINESS SCOPE
    # ========================================================

    if category == "Business Scope":

        return {
            "risk_detected": False,
            "risk_level": "LOW",
            "risk_score": 10,
            "risk_type": "Business Scope",
            "reason": (
                "The agreement defines the business activities "
                "covered by the contract."
            )
        }


    # ========================================================
    # 22. DEFAULT OFFICE / LOCATION
    # ========================================================

    if category == "Office & Location":

        return {
            "risk_detected": False,
            "risk_level": "LOW",
            "risk_score": 5,
            "risk_type": "Business Location",
            "reason": (
                "The agreement specifies the business "
                "location or place of operations."
            )
        }


    # ========================================================
    # RETURN DEFAULT
    # ========================================================

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

        clauses = load_classified_clauses(
            file_path
        )

        print(
            f"\nLoaded {len(clauses)} classified clauses."
        )

        results = analyze_clauses(
            clauses
        )

        display_results(
            results
        )

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