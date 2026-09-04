from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import shutil
import tempfile

# Import existing project functions
from src.data_processing.document_parser import extract_text, clean_text
from src.clause_extraction.clause_extractor import extract_clauses
from src.clause_classification.clause_classifier import classify_clauses
from src.risk_analysis.risk_detector import analyze_clauses
from src.risk_analysis.overall_risk_score import create_overall_report


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Contract Intelligence API",
    description="AI-assisted contract clause classification and risk analysis API",
    version="1.0.0"
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Contract Intelligence API is running",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ============================================================
# CONTRACT ANALYSIS ENDPOINT
# ============================================================

@app.post("/analyze")
async def analyze_contract(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # CHECK FILE TYPE
    # --------------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file provided."
        )

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    temp_path = None

    try:

        # ----------------------------------------------------
        # SAVE UPLOADED PDF TEMPORARILY
        # ----------------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file
            )

            temp_path = temp_file.name

        # ----------------------------------------------------
        # STEP 1: EXTRACT TEXT
        # ----------------------------------------------------

        raw_text = extract_text(
            temp_path
        )

        cleaned_text = clean_text(
            raw_text
        )

        # ----------------------------------------------------
        # STEP 2: EXTRACT CLAUSES
        # ----------------------------------------------------

        clauses = extract_clauses(
            cleaned_text
        )

        # ----------------------------------------------------
        # STEP 3: CLASSIFY CLAUSES
        # ----------------------------------------------------

        classified_clauses = classify_clauses(
            clauses
        )

        # ----------------------------------------------------
        # STEP 4: DETECT RISKS
        # ----------------------------------------------------

        risk_analysis = analyze_clauses(
            classified_clauses
        )

        # ----------------------------------------------------
        # STEP 5: CALCULATE OVERALL RISK
        # ----------------------------------------------------

        overall_report = create_overall_report(
            risk_analysis
        )

        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {

            "filename": file.filename,

            "total_clauses": len(
                classified_clauses
            ),

            "overall_risk_score":
                overall_report[
                    "overall_risk_score"
                ],

            "overall_risk_level":
                overall_report[
                    "overall_risk_level"
                ],

            "high_risk_clauses":
                overall_report[
                    "high_risk_clauses"
                ],

            "medium_risk_clauses":
                overall_report[
                    "medium_risk_clauses"
                ],

            "low_risk_clauses":
                overall_report[
                    "low_risk_clauses"
                ],

            "risk_clauses":
                overall_report[
                    "risk_clauses"
                ]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        # ----------------------------------------------------
        # DELETE TEMPORARY FILE
        # ----------------------------------------------------

        if temp_path and os.path.exists(
            temp_path
        ):

            os.remove(
                temp_path
            )