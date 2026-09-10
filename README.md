# AI-Powered Contract Intelligence & Risk Scoring

An AI-assisted contract analysis system that extracts contract clauses, classifies them, performs semantic search, and identifies potential contractual risks.

## 📌 Project Overview

Contract Intelligence is an NLP-based application designed to automate the analysis of legal contracts.

The system accepts a contract PDF, extracts and cleans the text, identifies important clauses, classifies the clauses into relevant categories, assigns risk scores, and generates a risk assessment.

The project also includes semantic search using sentence embeddings and FAISS, a FastAPI REST API, and Docker support for deployment.

## 🎯 Objectives

* Extract text from contract PDF documents
* Clean and preprocess contract text
* Identify important contractual clauses
* Classify clauses into legal categories
* Detect potentially risky clauses
* Assign risk scores to clauses and contracts
* Perform semantic similarity search
* Provide an API for contract analysis
* Containerize the application using Docker

## 🏗️ System Architecture

```text
Contract PDF
     │
     ▼
PDF Text Extraction
     │
     ▼
Text Cleaning & Preprocessing
     │
     ▼
Clause Extraction
     │
     ▼
Clause Classification
     │
     ▼
Risk Detection & Scoring
     │
     ├──────────────► Risk Assessment Report
     │
     ▼
Sentence Embeddings
     │
     ▼
FAISS Vector Database
     │
     ▼
Semantic Search
     
FastAPI
     │
     ▼
REST API
     │
     ▼
Docker Container
```

## 📊 Dataset

The project uses the **CUAD (Contract Understanding Atticus Dataset)** for contract clause analysis and classification.

Dataset characteristics:

* 510 contracts
* 41 clause categories
* Contract-level train/validation/test split
* Approximately 13,823 valid annotated clause records after preprocessing

The processed dataset is stored as:

```text
data/processed/cuad_annotations.csv
```

## 🧠 NLP Pipeline

### 1. PDF Text Extraction

Contract PDFs are processed using PDF text extraction tools.

The extracted text is cleaned to remove unnecessary formatting and whitespace.

### 2. Clause Extraction

The system identifies individual contractual clauses from the cleaned contract text.

### 3. Clause Classification

Extracted clauses are classified into legal categories using NLP/transformer-based approaches.

### 4. Risk Detection

Each clause receives a risk score based on detected contractual risk factors.

Risk levels include:

```text
LOW
MEDIUM
HIGH
```

An overall contract risk score is also calculated.

## 🔎 Semantic Search

The project uses:

* Sentence Transformers
* `all-MiniLM-L6-v2`
* FAISS

The embedding dimension is:

```text
384
```

Contract clauses are converted into vector embeddings and stored in a FAISS index.

This allows semantically similar clauses to be retrieved even when the wording is different.

## 🚀 FastAPI

The project provides a REST API for contract analysis.

Main endpoints:

```text
GET /
GET /health
POST /analyze
```

The `/analyze` endpoint accepts a contract PDF and returns analysis results including:

* Filename
* Total clauses
* Risk score
* Risk level
* Risky clauses
* Clause classifications

Interactive API documentation is available through FastAPI/Swagger when the application is running.

## 🐳 Docker

The application can be containerized using Docker.

Build the image:

```powershell
docker build -t contract-intelligence-api .
```

Run the container:

```powershell
docker run -p 8000:8000 contract-intelligence-api
```

The API can then be accessed through:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## 📁 Project Structure

```text
contract_intelligence/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── embeddings/
│
├── models/
│
├── reports/
│
├── src/
│   ├── api/
│   │   └── main.py
│   │
│   ├── preprocessing/
│   │
│   ├── clause_extraction/
│   │
│   ├── classification/
│   │
│   ├── risk_detection/
│   │
│   ├── vector_search/
│   │
│   └── report_generation/
│
├── tests/
│
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Technologies Used

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Python                | Core programming language    |
| NLP                   | Contract text analysis       |
| CUAD                  | Contract clause dataset      |
| Transformers          | Clause classification        |
| Sentence Transformers | Text embeddings              |
| FAISS                 | Vector similarity search     |
| spaCy                 | NLP processing               |
| PyMuPDF               | PDF text extraction          |
| FastAPI               | REST API                     |
| Uvicorn               | API server                   |
| Docker                | Application containerization |
| Git/GitHub            | Version control              |

## 📈 Example Risk Analysis

Example output:

```text
CONTRACT RISK ASSESSMENT REPORT

Overall Risk Score: 27.19 / 100
Overall Risk Level: LOW

HIGH RISK CLAUSES: 1
MEDIUM RISK CLAUSES: 6
LOW RISK CLAUSES: 9
```

The system highlights high-risk clauses so that users can focus their attention on potentially problematic contractual provisions.

## 🧪 Testing

The API was tested using contract PDF files.

Example:

```text
Contract PDF
     ↓
Upload through API
     ↓
Text extraction
     ↓
Clause extraction
     ↓
Clause classification
     ↓
Risk scoring
     ↓
JSON response
```

The system successfully returned contract-level statistics and risky clauses through the FastAPI endpoint.

## 🔐 Limitations

* Risk scores are intended as AI-assisted indicators and not as legal advice.
* OCR may be required for scanned/image-only PDFs.
* Classification performance depends on training data and model quality.
* Legal interpretation can require review by a qualified legal professional.
* The current system is primarily designed as a prototype/research project.

## 🔮 Future Enhancements

* Fine-tune a legal-domain transformer such as Legal-BERT/RoBERTa on CUAD
* Improve OCR support for scanned contracts
* Add a web-based frontend
* Add authentication and authorization
* Add database storage for analyzed contracts
* Improve risk scoring using trained ML models
* Add explainable AI for risk predictions
* Deploy the API to a cloud platform
* Add monitoring and performance testing

## 👩‍💻 Author

**Nikhila K. S.**

Data Scientist | Machine Learning Enthusiast

Background in Electronics & Communication Engineering, Signal Processing, and operational decision-making.

## 📄 Disclaimer

This project is intended for educational, research, and demonstration purposes. It does not provide legal advice or replace professional legal review.
