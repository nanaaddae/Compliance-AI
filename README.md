# ComplianceAI — AI-Powered Policy & Compliance Checker

A full-stack web application that allows companies to upload internal policy documents and let employees query them using natural language. Built with FastAPI, React, and a full RAG (Retrieval Augmented Generation) pipeline.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green) ![React](https://img.shields.io/badge/React-18-blue) ![License](https://img.shields.io/badge/license-MIT-green)

---

## What It Does

Employees can ask questions like *"Can I expense a client dinner?"* or *"What is the hotel limit for New York?"* and get accurate, sourced answers drawn strictly from uploaded company policy PDFs — no hallucination, no guessing.

Every query is logged for compliance auditing, and access is controlled by role so employees, compliance officers, executives, and admins all see different things.

---

## Features

- **RAG Pipeline** — PDF documents are chunked, embedded, and stored in ChromaDB. Queries are matched semantically and answered by LLaMA 3 via Groq
- **Role-Based Access Control (RBAC)** — 4 roles with different permissions enforced at the API level
- **JWT Authentication** — secure register/login flow with protected routes
- **Document Management** — compliance officers can upload and delete policy PDFs
- **Audit Logging** — every query is saved with the user, question, answer, and source chunks
- **Admin Panel** — admins can manage user roles directly from the UI

---

## Tech Stack

**Backend**
- FastAPI — REST API framework
- PostgreSQL — relational database (via Docker)
- SQLAlchemy — ORM
- ChromaDB — vector database for semantic search
- sentence-transformers — local embedding model (all-MiniLM-L6-v2)
- LangChain — document chunking
- Groq + LLaMA 3 — LLM for answer generation
- pdfplumber — PDF text extraction
- JWT (python-jose) + bcrypt — auth and password hashing

**Frontend**
- React 18
- Tailwind CSS
- Axios
- React Router

---

## Architecture

```
User Question
     │
     ▼
Embed Question (sentence-transformers)
     │
     ▼
Semantic Search (ChromaDB)
     │
     ▼
Retrieve Top K Chunks
     │
     ▼
Build Prompt with Context
     │
     ▼
LLaMA 3 via Groq API
     │
     ▼
Sourced Answer + Audit Log
```

---

## RBAC Roles

| Role | Permissions |
|---|---|
| `employee` | Ask compliance questions, view own query history |
| `compliance_officer` | Upload/delete policy documents + employee permissions |
| `executive` | View all audit logs across the organization |
| `admin` | Full access + user role management |

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker Desktop

### Backend Setup

```bash
cd compliance-checker

# Create and activate virtual environment
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL
docker-compose up -d

# Configure environment
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Run the server
uvicorn app.main:app --reload
```

API runs at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs at `http://localhost:3000`

---

## Environment Variables

Create a `.env` file in the `compliance-checker` directory:

```
DATABASE_URL=postgresql://compliance_user:compliance_pass@localhost:5432/compliance_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GROQ_API_KEY=your-groq-api-key-here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

---

## Project Structure

```
compliance-checker/
├── app/
│   ├── api/routes/
│   │   ├── auth.py          # Register & login
│   │   ├── users.py         # User management
│   │   ├── documents.py     # PDF upload & management
│   │   ├── query.py         # RAG query endpoint
│   │   └── audit_logs.py    # Audit log endpoints
│   ├── core/
│   │   ├── config.py        # Environment settings
│   │   ├── dependencies.py  # JWT auth + role enforcement
│   │   └── security.py      # Token utilities
│   ├── db/
│   │   └── database.py      # SQLAlchemy setup
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic request/response models
│   ├── services/
│   │   ├── document_processor.py  # PDF → chunks → embeddings → ChromaDB
│   │   └── query_service.py       # RAG pipeline + Groq
│   └── main.py
├── docker-compose.yml
└── requirements.txt

frontend/
└── src/
    ├── components/
    │   ├── QueryPanel.js      # Compliance question interface
    │   ├── DocumentsPanel.js  # PDF upload/management
    │   ├── AuditPanel.js      # Query history
    │   ├── Navbar.js
    │   └── Layout.js
    ├── pages/
    │   ├── Login.js
    │   ├── Register.js
    │   ├── Dashboard.js
    │   └── Admin.js
    ├── services/
    │   └── api.js             # Axios API calls
    └── context/
        └── AuthContext.js     # Global auth state
```

---

## Key Technical Decisions

**Why ChromaDB?** Runs locally with no external service required, perfect for development and small-to-medium deployments.

**Why sentence-transformers over OpenAI embeddings?** Free, runs locally, no API calls needed for embedding. The `all-MiniLM-L6-v2` model is fast and accurate enough for document retrieval.

**Why Groq + LLaMA 3?** Free tier is generous enough for a portfolio project, low latency, and LLaMA 3 handles instruction-following well for RAG prompts.

**Chunking strategy:** 1000 character chunks with 200 character overlap using `RecursiveCharacterTextSplitter`. Overlap prevents context loss at chunk boundaries.
