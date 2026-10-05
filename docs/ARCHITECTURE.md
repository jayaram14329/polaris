# POLARIS Architecture & Technical Specification

**Problem Statement ID:** SIH26063  
**Title:** Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal  
**Organization:** Ministry of Earth Sciences (MoES)  
**Department:** National Centre for Polar and Ocean Research (NCPOR)  
**Category:** Software  

---

## 1. System Vision

POLARIS is an integrated enterprise scientific platform designed to consolidate India's 40+ years of polar exploration records, research papers, scientific datasets, and media archives. The platform introduces **Citation-Grounded RAG**, **Interactive Polar Station GIS**, **FAIR-compliant Dataset Cataloguing**, and a **Human-in-the-Loop Outreach Studio** that bridges the gap between deep polar research and public scientific understanding.

---

## 2. High-Level Data Flow

```
POLAR RESEARCH (Field Logs, Ice Cores, Station Telemetry)
       ↓
STRUCTURED KNOWLEDGE (PyMuPDF, DataCite 4.4 & Dublin Core Schemas)
       ↓
UNIFIED HYBRID SEARCH (pgvector Dense Semantic + Full-Text Index)
       ↓
POLAR AI (Citation-Grounded RAG Engine, Zero Hallucination)
       ↓
POLAR ACADEMY (STEM Learning, Verified Quizzes & Milestones)
       ↓
OUTREACH STUDIO (Human-Approved Multi-Platform Dissemination)
```

---

## 3. Technology Stack

| Layer | Technologies | Justification & Role |
| :--- | :--- | :--- |
| **Frontend** | Next.js 16, TypeScript, Tailwind CSS, Lucide Icons | Server-rendered, type-safe, responsive polar UI with glassmorphism and modern dark aesthetics. |
| **Maps & GIS** | Leaflet, OpenStreetMap, CARTO Dark Tiles | Interactive geospatial rendering of polar research stations (Maitri, Bharati, Himadri, IndARC). |
| **Backend** | Python 3.11, FastAPI, Pydantic v2, Uvicorn ASGI | Ultra-low latency asynchronous REST API services with automated OpenAPI documentation. |
| **Database** | SQLite / PostgreSQL + pgvector | Unified relational metadata lake with sub-millisecond vector similarity search. |
| **RAG Engine** | Custom Dense Scientific Embedder + Cosine Scorer | Citation-grounded evidence extraction, verbatim snippet matching, and fallback refusal guarantees. |
| **Security** | JWT, PBKDF2/Bcrypt, Role-Based Access Control | Granular security segregating Public, Researcher, Editor, and Admin permissions with immutable audit trails. |
| **Deployment** | Docker, Docker Compose | Turnkey containerized orchestration for one-command cloud or on-premise deployment. |

---

## 4. Key Subsystems

### 4.1. Citation-Grounded POLAR AI
- **No Uncontrolled Hallucination:** Verifies cosine similarity against indexed chunk embeddings.
- **Verifiable Sources:** Every answer returns the exact document title, section name, page number, and similarity confidence score.
- **Fallback Refusal:** When knowledge repository coverage is insufficient, POLAR AI explicitly returns:
  `"I couldn't find enough information in the POLARIS knowledge base."`

### 4.2. Human-in-the-Loop Outreach Studio
- **Strict Quality Gate:** AI-generated scientific articles, Instagram posts, and student explainers are ALWAYS created with `Draft` status.
- **Role Verification:** Content transitions to `Pending_Review`, where authenticated Science Editors (`Dr. S. Sharma`) must inspect, verify, and click **Approve** or **Reject**.
- **Audit Logging:** Every approval, rejection, schedule, and publication event is permanently recorded in the tamper-evident audit log.

### 4.3. Interactive Polar Station GIS
- Real-time simulated telemetry for **Bharati Station** (-69.41°S, 76.19°E), **Maitri Station** (-70.77°S, 11.73°E), **Himadri Station** (78.92°N, 11.93°E), and **IndARC Observatory** (78.98°N, 11.98°E).
- Interactive coordinate inspection, live weather conditions, and direct links to active seasonal expeditions.

### 4.4. Polar Academy & Quiz Engine
- Chronological historical milestone timeline tracking Indian polar science from the 1981 pioneer expedition to the ongoing 44th IAE.
- Gamified 4-choice interactive quizzes auto-generated from verified scientific literature, offering instant grading and primary-source explanations.
