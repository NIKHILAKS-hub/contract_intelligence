import os
import json


# ============================================================
# LOAD RISK ANALYSIS
# ============================================================

def load_risk_analysis(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"\nRisk analysis file not found:\n{file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        results = json.load(file)

    if not isinstance(results, list):

        raise ValueError(
            "The JSON file must contain a list."
        )

    return results


# ============================================================
# CALCULATE OVERALL RISK SCORE
# ============================================================

def calculate_overall_score(results):

    if not results:
        return 0

    total_score = sum(
        result.get("risk_score", 0)
        for result in results
    )

    maximum_possible_score = len(results) * 100

    overall_score = (
        total_score / maximum_possible_score
    ) * 100

    return round(overall_score, 2)


# ============================================================
# DETERMINE OVERALL RISK LEVEL
# ============================================================

def determine_risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


# ============================================================
# FIND HIGH-RISK CLAUSES
# ============================================================

def get_high_risk_clauses(results):

    high_risk = []

    for result in results:

        if result.get("risk_detected") is True:

            high_risk.append({
                "clause_number": result.get(
                    "clause_number"
                ),
                "title": result.get(
                    "title"
                ),
                "risk_level": result.get(
                    "risk_level"
                ),
                "risk_score": result.get(
                    "risk_score"
                ),
                "risk_type": result.get(
                    "risk_type"
                )
            })

    # Sort highest risk first
    high_risk.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    return high_risk


# ============================================================
# CREATE OVERALL REPORT
# ============================================================

def create_overall_report(results):

    overall_score = calculate_overall_score(
        results
    )

    overall_level = determine_risk_level(
        overall_score
    )

    risk_clauses = get_high_risk_clauses(
        results
    )

    high_count = sum(
        1
        for result in results
        if result.get("risk_level") == "HIGH"
    )

    medium_count = sum(
        1
        for result in results
        if result.get("risk_level") == "MEDIUM"
    )

    low_count = sum(
        1
        for result in results
        if result.get("risk_level") == "LOW"
    )

    report = {

        "total_clauses": len(results),

        "overall_risk_score": overall_score,

        "overall_risk_level": overall_level,

        "high_risk_clauses": high_count,

        "medium_risk_clauses": medium_count,

        "low_risk_clauses": low_count,

        "risk_clauses": risk_clauses
    }

    return report


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(
    report,
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
            report,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# DISPLAY REPORT
# ============================================================

def display_report(report):

    print("\n" + "=" * 80)
    print("OVERALL CONTRACT RISK SCORE")
    print("=" * 80)

    print(
        f"\nTotal Clauses       : "
        f"{report['total_clauses']}"
    )

    print(
        f"Overall Risk Score  : "
        f"{report['overall_risk_score']}/100"
    )

    print(
        f"Overall Risk Level  : "
        f"{report['overall_risk_level']}"
    )

    print(
        f"\nHIGH Risk Clauses   : "
        f"{report['high_risk_clauses']}"
    )

    print(
        f"MEDIUM Risk Clauses : "
        f"{report['medium_risk_clauses']}"
    )

    print(
        f"LOW Risk Clauses    : "
        f"{report['low_risk_clauses']}"
    )

    print("\n" + "-" * 80)
    print("RISK CLAUSES")
    print("-" * 80)

    for clause in report["risk_clauses"]:

        print(
            f"\nClause {clause['clause_number']}"
        )

        print(
            f"Title      : "
            f"{clause['title']}"
        )

        print(
            f"Risk Level : "
            f"{clause['risk_level']}"
        )

        print(
            f"Risk Score : "
            f"{clause['risk_score']}"
        )

        print(
            f"Risk Type  : "
            f"{clause['risk_type']}"
        )

    print("\n" + "=" * 80)
    print("OVERALL RISK SCORING FINISHED")
    print("=" * 80)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 80)
    print("CONTRACT OVERALL RISK SCORING")
    print("=" * 80)

    file_path = input(
        "\nEnter the path of risk_analysis.json: "
    ).strip()

    try:

        results = load_risk_analysis(
            file_path
        )

        print(
            f"\nLoaded {len(results)} risk analysis records."
        )

        report = create_overall_report(
            results
        )

        display_report(
            report
        )

        output_path = os.path.join(
            "data",
            "contracts",
            "overall_risk_score.json"
        )

        save_report(
            report,
            output_path
        )

        print(
            "\nOverall risk report saved to:"
        )

        print(
            output_path
        )

    except Exception as e:

        print("\nERROR:")
        print(e)