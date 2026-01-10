# 🔐 SentinelAI

**Intelligent Threat Analysis Platform**

## 1. Problem Statement

**Phishing URLs and scam content remain one of the most common attack vectors for fraud, identity theft, and malware distribution.**

### Most existing tools rely on:

- Black-box APIs
- Heavily rule-based systems
- Limited explainability

This makes them hard to trust, extend, or adapt to evolving threats.

## 2. Objective

**Build a production-style, end-to-end threat analysis system that**:

- Uses custom-trained machine learning models
- Supports URL and document scam detection
- Provides confidence scores and explanations
- Is modular, extensible, and architected like a real product
- Goal is skill demonstration, not monetization or public launch.

## 3. Non-Goals (VERY IMPORTANT)

**SentinelAI will NOT:**

- Train or fine-tune large language models
- Compete with commercial security products
- Rely entirely on third-party AI APIs
- Optimize for large-scale traffic or billing

## 4. Core Design Principles

**Model Ownership**
- All core detections must use in-house trained models

**Explainability over Hype**
- LLMs only assist explanations, not decisions

**Production Thinking**
- Clean APIs, validation, metrics

**Extensibility**
- Models can be swapped without frontend changes

## 5. System Architecture

```bash
User
 │
 ▼
Frontend (React)
 │
 ▼
Backend API (Flask)
 ├── URL Phishing Classifier (Custom ML)
 ├── Text Scam Classifier (DistilBERT)
 ├── Confidence & Risk Scoring
 └── Optional LLM Explanation Layer
 ```

## 6. Functional Scope

### 6.1 URL Threat Detection

**Input**: URL string

**Detection via**:
- Lexical feature extraction
- Supervised ML classifier

**Output**:
- Classification (safe / phishing)
- Confidence score
- Risk indicators

### 6.2 File & Text Threat Detection

**Supported formats**:
- PDF
- TXT

**Steps**:
- Text extraction
- NLP preprocessing
- Transformer-based classification

**Output**:
- Scam / Legit
- Confidence score
- Highlighted suspicious patterns

### 6.3 Explainability Layer (Optional)

**Uses LLM for**:
- Natural language explanation
- Risk interpretation

**Not involved in classification decision**

## 7. Tech Stack

- **Frontend** - React + Vite + Material UI + Axios

- **Backend** - 
> Flask + REST APIs + Model inference pipeline 
> Machine Learning +Scikit-learn
> HuggingFace Transformers
>Joblib / Torch model persistence
>AI (Explanation Only)
>Gemini LLM (pluggable)

