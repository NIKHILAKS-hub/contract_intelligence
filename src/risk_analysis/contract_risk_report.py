import os
import json
from datetime import datetime


# ============================================================
# LOAD JSON FILE
# ============================================================

def load_json(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"\nFile not found:\n{file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# GENERATE REPORT
# ============================================================

def generate_report(
    overall_report,
    risk_analysis
):

    lines = []

    lines.append("=" * 80)
    lines.append("CONTRACT RISK ASSESSMENT REPORT")
    lines.append("=" * 80)

    lines.append("")
    lines.append(
        f"Report Generated : "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    lines.append("")

    # --------------------------------------------------------
    # OVERALL SUMMARY
    # --------------------------------------------------------

    lines.append("-" * 80)
    lines.append("OVERALL RISK SUMMARY")
    lines.append("-" * 80)

    lines.append(
        f"Total Clauses       : "
        f"{overall_report['total_clauses']}"
    )

    lines.append(
        f"Overall Risk Score  : "
        f"{overall_report['overall_risk_score']} / 100"
    )

    lines.append(
        f"Overall Risk Level  : "
        f"{overall_report['overall_risk_level']}"
    )

    lines.append(
        f"High Risk Clauses   : "
        f"{overall_report['high_risk_clauses']}"
    )

    lines.append(
        f"Medium Risk Clauses : "
        f"{overall_report['medium_risk_clauses']}"
    )

    lines.append(
        f"Low Risk Clauses    : "
        f"{overall_report['low_risk_clauses']}"
    )

    # --------------------------------------------------------
    # HIGH RISK
    # --------------------------------------------------------

    high_risk = [
        clause
        for clause in risk_analysis
        if clause.get("risk_level") == "HIGH"
    ]

    lines.append("")
    lines.append("-" * 80)
    lines.append("HIGH RISK CLAUSES")
    lines.append("-" * 80)

    if high_risk:

        for clause in high_risk:

            lines.append("")
            lines.append(
                f"Clause {clause['clause_number']}: "
                f"{clause['title']}"
            )

            lines.append(
                f"Risk Score : "
                f"{clause['risk_score']} / 100"
            )

            lines.append(
                f"Risk Type  : "
                f"{clause['risk_type']}"
            )

            lines.append(
                f"Reason     : "
                f"{clause['reason']}"
            )

    else:

        lines.append("No high-risk clauses detected.")

    # --------------------------------------------------------
    # MEDIUM RISK
    # --------------------------------------------------------

    medium_risk = [
        clause
        for clause in risk_analysis
        if clause.get("risk_level") == "MEDIUM"
    ]

    lines.append("")
    lines.append("-" * 80)
    lines.append("MEDIUM RISK CLAUSES")
    lines.append("-" * 80)

    if medium_risk:

        for clause in medium_risk:

            lines.append("")
            lines.append(
                f"Clause {clause['clause_number']}: "
                f"{clause['title']}"
            )

            lines.append(
                f"Risk Score : "
                f"{clause['risk_score']} / 100"
            )

            lines.append(
                f"Risk Type  : "
                f"{clause['risk_type']}"
            )

            lines.append(
                f"Reason     : "
                f"{clause['reason']}"
            )

    else:

        lines.append("No medium-risk clauses detected.")

    # --------------------------------------------------------
    # LOW RISK
    # --------------------------------------------------------

    low_risk = [
        clause
        for clause in risk_analysis
        if clause.get("risk_level") == "LOW"
    ]

    lines.append("")
    lines.append("-" * 80)
    lines.append("LOW RISK CLAUSES")
    lines.append("-" * 80)

    if low_risk:

        for clause in low_risk:

            lines.append("")

            lines.append(
                f"Clause {clause['clause_number']}: "
                f"{clause['title']}"
            )

            lines.append(
                f"Risk Score : "
                f"{clause['risk_score']} / 100"
            )

            lines.append(
                f"Risk Type  : "
                f"{clause['risk_type']}"
            )

    # --------------------------------------------------------
    # KEY RISK FINDINGS
    # --------------------------------------------------------

    lines.append("")
    lines.append("-" * 80)
    lines.append("KEY RISK FINDINGS")
    lines.append("-" * 80)

    if high_risk:

        highest = max(
            high_risk,
            key=lambda x: x["risk_score"]
        )

        lines.append("")
        lines.append(
            f"1. Highest Risk Clause: "
            f"Clause {highest['clause_number']} - "
            f"{highest['title']}"
        )

        lines.append(
            f"   Risk Score: "
            f"{highest['risk_score']} / 100"
        )

        lines.append(
            f"   Risk Type: "
            f"{highest['risk_type']}"
        )

    if medium_risk:

        lines.append("")
        lines.append(
            f"2. Medium-risk clauses identified: "
            f"{len(medium_risk)}"
        )

        lines.append(
            "   These clauses should be reviewed "
            "for potential contractual impact."
        )

    lines.append("")
    lines.append(
        "3. Overall Assessment: "
        f"The contract has been classified as "
        f"{overall_report['overall_risk_level']} risk "
        f"with an overall score of "
        f"{overall_report['overall_risk_score']} / 100."
    )

    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    lines.append("")
    lines.append("-" * 80)
    lines.append("DISCLAIMER")
    lines.append("-" * 80)

    lines.append("")
    lines.append(
        "This report is generated using a rule-based "
        "contract risk analysis system."
    )

    lines.append(
        "The risk scores are automated assessments and "
        "should not be considered legal advice."
    )

    lines.append(
        "Contracts should be reviewed by a qualified "
        "legal professional before making legal or "
        "business decisions."
    )

    lines.append("")
    lines.append("=" * 80)
    lines.append("END OF CONTRACT RISK REPORT")
    lines.append("=" * 80)

    return "\n".join(lines)


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(
    report_text,
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

        file.write(report_text)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 80)
    print("CONTRACT RISK REPORT GENERATOR")
    print("=" * 80)

    overall_path = input(
        "\nEnter the path of overall_risk_score.json: "
    ).strip()

    risk_path = input(
        "\nEnter the path of risk_analysis.json: "
    ).strip()

    try:

        # Load files
        overall_report = load_json(
            overall_path
        )

        risk_analysis = load_json(
            risk_path
        )

        print(
            "\nFiles loaded successfully."
        )

        # Generate report
        report_text = generate_report(
            overall_report,
            risk_analysis
        )

        # Display report
        print("\n")
        print(report_text)

        # Save report
        output_path = os.path.join(
            "data",
            "contracts",
            "contract_risk_report.txt"
        )

        save_report(
            report_text,
            output_path
        )

        print(
            "\n\nReport saved to:"
        )

        print(
            output_path
        )

        print("\n" + "=" * 80)
        print("REPORT GENERATION FINISHED")
        print("=" * 80)

    except Exception as e:

        print("\nERROR:")
        print(e)