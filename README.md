# SentinelAI

**Intelligent Threat Analysis Platform**

## Overview

**SentinelAI is a full-stack intelligent threat detection system designed to identify phishing URLs and scam content in documents using custom-trained machine learning models.**

## Why SentinelAI?

- Ownership of ML inference
- Avoids black-box API dependency
- Architected for extensibility
- Focus on explainability

## Architecture

```bash
User → Frontend (React)
     → Backend API (Flask)
        → URL ML Model
        → Text ML Model
        → Optional LLM Explainer
```

## Core Features

1. Phishing URL detection (custom ML)
2. Scam document detection (NLP)
3. Confidence scoring
4. Explainable predictions
5. Modular model pipeline

## Tech Stack 

**Frontend** - React, MUI
**Backend** - Flask
**ML**: Scikit-learn, HuggingFace Transformers
**Models**: RandomForest / DistilBERT
**LLM**: Gemini (optional explanation)