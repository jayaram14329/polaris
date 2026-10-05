# POLARIS: Polar Knowledge & Outreach Intelligence System

**Smart India Hackathon 2026**  
**Problem Statement ID:** SIH26063  
**Problem Statement:** Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal  
**Organization:** Ministry of Earth Sciences (MoES)  
**Department:** National Centre for Polar and Ocean Research (NCPOR)  
**Category:** Software  
**Theme:** Smart Education  

---

## ❄️ Executive Overview

**POLARIS** is an enterprise polar knowledge lake and intelligence system uniting India's 40+ years of Antarctic, Arctic, and Southern Ocean exploration. It transitions scientific data from fragmented archives into an accessible, interactive, and actionable platform featuring:
- **Interactive Polar Station GIS:** Geospatial intelligence for **Maitri**, **Bharati**, **Himadri**, and **IndARC** with real-time simulated telemetry.
- **Citation-Grounded POLAR AI (RAG):** Dense vector similarity question answering with verbatim citations, page references, and zero hallucination.
- **Outreach Studio & Human-in-the-Loop Review:** Multi-channel science communicator (Website articles, Instagram, LinkedIn, Student explainers) governed by mandatory Editor sign-off before publishing.
- **Polar Academy:** Milestone timeline (1981–2026) and interactive STEM quizzes auto-generated from peer-reviewed scientific literature.
- **FAIR Dataset Catalogue:** Interactive table previews and dynamic anomaly charts for cryospheric and oceanographic datasets.

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.11+** installed
- **Node.js v20+** / **npm 10+** installed

### 1-Click Launch (Windows)
Double-click `start_polaris.bat` or run:
```bash
.\start_polaris.bat
```

### Manual Launch

#### 1. Backend (FastAPI)
```bash
cd C:\SIH\polaris
python backend/sample_seed.py
python run_backend.py
```
- API server runs at: `http://localhost:8000`
- Interactive Swagger documentation: `http://localhost:8000/docs`

#### 2. Frontend (Next.js 16)
```bash
cd C:\SIH\polaris\frontend
npm run dev
```
- Frontend portal runs at: `http://localhost:3000`

---

## 🔑 Demo Credentials & Roles

| Role | Username / Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **System Admin** | `admin@polaris.gov.in` | `admin123` | Full access, analytics, audit logs, user management |
| **Science Editor** | `editor@polaris.gov.in` | `editor123` | Outreach Studio verification, approval gate, schedule & publish |
| **Researcher** | `researcher@polaris.gov.in` | `researcher123` | Data ingestion, report upload, RAG research assistant |
| **Student / Public** | `public@polaris.gov.in` | `public123` | Search, Polar GIS, Polar Academy, public AI assistant |

*(Role switcher is also available directly in the top-right header of the web portal for rapid demonstration.)*

---

## 🎬 19-Step SIH Demo Flow

1. **Open POLARIS:** Navigate to `http://localhost:3000`.
2. **View Homepage:** Inspect the polar aesthetic (deep navy, cyan, ice blue) and MoES/NCPOR branding.
3. **View Statistics:** Examine the 6 primary KPI cards (44+ Expeditions, 3 Stations, 100% Grounded RAG, etc.).
4. **Open Polar Map:** Navigate to **Polar Station GIS** to view Leaflet geospatial projections.
5. **Click Research Station:** Select **Bharati Station** (-69.41°S, 76.19°E) to view telemetry and architecture specs.
6. **View Related Expedition:** Click **"View Related Expedition"** to inspect the 43rd / 44th IAE.
7. **Open Expedition Report:** Open the **"43rd Indian Antarctic Expedition Scientific Report"** (48 pages).
8. **Ask POLAR AI:** Query: `"What were the major research objectives of this expedition?"`.
9. **Display Answer:** View the synthesized, 100% grounded response detailing atmospheric physics, glaciology, and microbiology.
10. **Display Source Citations:** Expand the **Sources Used** panel to inspect verbatim quotes, section headings, and page 14 reference.
11. **Open Outreach Studio:** Transition to the **Outreach Studio** tab.
12. **Select Resource:** Source automatically set to the 43rd Expedition Report.
13. **Generate Content:** Select **Website Article**, **Instagram**, or **Student Explanation** and click **"Generate AI Draft"**. Notice status is strictly `Draft`.
14. **Send for Review:** Click **"Send for Review"**; status transitions to `Pending_Review`.
15. **Open Editor Dashboard:** Switch role to **Science Editor (Dr. S. Sharma)**.
16. **Approve Content:** Click **"Approve Content"**; status updates to `Approved` with timestamped audit trail.
17. **View Approved Content:** Click **"Publish to MoES Channels"**; content becomes publicly active.
18. **Open Polar Academy:** Transition to **Polar Academy** and explore the 1981–2026 Milestone Timeline.
19. **Take Verified Quiz:** Answer the 4-choice interactive quiz and receive instant evaluation, badge award, and literature citations.

---

## 📂 Project Directory Structure

```
polaris/
├── backend/
│   ├── main.py                  # FastAPI application entrypoint & middleware
│   ├── config.py                # Environment & security configuration
│   ├── database.py              # SQLite / PostgreSQL models & connection
│   ├── auth.py                  # JWT token management & RBAC dependencies
│   ├── sample_seed.py           # Comprehensive database seeder
│   ├── requirements.txt         # Python dependencies
│   └── routers/
│       ├── auth_routes.py       # Authentication & user profile endpoints
│       ├── repository_routes.py # Expeditions, reports, datasets, media CRUD
│       ├── station_routes.py    # Polar research stations & telemetry
│       ├── search_routes.py     # Global hybrid & multimodal media search
│       ├── rag_routes.py        # POLAR AI RAG engine & conversation history
│       ├── outreach_routes.py   # Outreach Studio generator & review workflow
│       ├── academy_routes.py    # Learning milestones & verified quizzes
│       └── admin_routes.py      # Operational analytics & audit trails
├── frontend/
│   ├── src/app/
│   │   ├── layout.tsx           # Polar metadata & Leaflet scripts
│   │   ├── page.tsx             # Complete multi-tab interactive portal
│   │   └── globals.css          # Polar tokens, glassmorphism & gradients
│   ├── package.json
│   └── tsconfig.json
├── ai/
│   ├── rag_engine.py            # Dense semantic vector search & source grounding
│   ├── outreach_generator.py    # Multi-channel draft synthesizer
│   └── quiz_generator.py        # Literature-verified STEM quiz generator
├── database/
│   └── polaris.db               # Pre-seeded SQLite database
├── sample-data/                 # Verified sample reports, datasets, and media
├── docs/
│   ├── ARCHITECTURE.md          # Technical architecture & pipeline diagrams
│   ├── API_DOCUMENTATION.md     # Full REST API specification
│   └── DEMO_FLOW_WALKTHROUGH.md # 19-step SIH demo script
├── presentation/
│   ├── POLARIS_SIH26063_Presentation.pptx # Official 6-slide submission PPTX
│   └── POLARIS_SIH26063_Presentation.pdf  # High-fidelity exported PDF
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml           # Turnkey multi-container deployment
├── .env.example                 # Environment variables template
└── README.md
```

---

## 🏆 Presentation Deliverables

The official Smart India Hackathon 2026 presentation has been crafted and formatted:
- **PowerPoint File:** `C:\SIH\POLARIS_SIH26063_Presentation.pptx`
- **PDF Export:** `C:\SIH\POLARIS_SIH26063_Presentation.pdf`
- **Slide Count:** Exactly 6 slides (Title, Idea, Technical Approach, Feasibility/Viability, Impact & Benefits, References).
- **Branding:** SIH 2026, Ministry of Earth Sciences (MoES), NCPOR.
- **Zero Criminal Content:** 100% replaced with polar science models, architecture diagrams, and real references.

---

## 🛡️ Prototype Disclosure
*This platform is an advanced prototype developed for the Smart India Hackathon 2026 (Problem Statement SIH26063). Sample datasets and telemetry are modeled accurately after NCPOR standards for demonstration purposes.*
