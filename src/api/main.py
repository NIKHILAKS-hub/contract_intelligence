# src/api/main.py

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

import os
import shutil
import tempfile


from src.data_processing.document_parser import (
    extract_text,
    clean_text
)

from src.clause_extraction.clause_extractor import (
    extract_clauses
)

from src.clause_classification.clause_classifier import (
    classify_clauses
)

from src.risk_analysis.risk_detector import (
    analyze_clauses
)

from src.risk_analysis.overall_risk_score import (
    create_overall_report
)

from src.vector_search.semantic_search import (
    search_clauses,
    search_uploaded_clauses
)


app = FastAPI(
    title="Contract Intelligence API",
    description=(
        "AI-assisted contract clause classification, "
        "semantic search, and risk analysis API"
    ),
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Contract Intelligence API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.get("/semantic-search")
def semantic_search(
    query: str,
    top_k: int = 3
):

    try:

        if not query or not query.strip():

            raise HTTPException(
                status_code=400,
                detail="Search query cannot be empty."
            )

        if top_k < 1:

            raise HTTPException(
                status_code=400,
                detail="top_k must be at least 1."
            )

        results = search_clauses(
            query=query,
            top_k=top_k
        )

        return {
            "query": query,
            "top_k": top_k,
            "search_type": "contract_repository",
            "results": results
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/analyze")
async def analyze_contract(
    file: UploadFile = File(...),
    query: str = "",
    top_k: int = 3
):

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

    if top_k < 1:

        raise HTTPException(
            status_code=400,
            detail="top_k must be at least 1."
        )

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file
            )

            temp_path = temp_file.name


        # ====================================================
        # TEXT EXTRACTION
        # ====================================================

        raw_text = extract_text(
            temp_path
        )

        cleaned_text = clean_text(
            raw_text
        )


        # ====================================================
        # CLAUSE EXTRACTION
        # ====================================================

        clauses = extract_clauses(
            cleaned_text
        )


        # ====================================================
        # CLAUSE CLASSIFICATION
        # ====================================================

        classified_clauses = classify_clauses(
            clauses
        )


        # ====================================================
        # RISK ANALYSIS
        # ====================================================

        risk_analysis = analyze_clauses(
            classified_clauses
        )


        # ====================================================
        # OVERALL RISK
        # ====================================================

        overall_report = create_overall_report(
            risk_analysis
        )


        # ====================================================
        # SEMANTIC SEARCH ON UPLOADED PDF
        # ====================================================

        semantic_results = []

        if query and query.strip():

            semantic_results = search_uploaded_clauses(
                classified_clauses,
                query,
                top_k
            )


        # ====================================================
        # RESPONSE
        # ====================================================

        return {

            "filename": file.filename,

            "analysis": {

                "total_clauses":
                    len(classified_clauses),

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
            },

            "semantic_search": {

                "query": query,

                "top_k": top_k,

                "search_type":
                    "uploaded_contract",

                "results":
                    semantic_results
            }
        }


    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    finally:

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            os.remove(
                temp_path
            )