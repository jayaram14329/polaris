# POLARIS API Documentation

**Interactive Swagger UI:** `http://localhost:8000/docs`  
**ReDoc Specification:** `http://localhost:8000/redoc`  
**Base URL:** `http://localhost:8000/api`

---

## 1. Authentication (`/api/auth`)

### `POST /api/auth/login`
Authenticates a user and issues a signed JWT access token.
```json
// Request
{
  "username": "editor@polaris.gov.in",
  "password": "editor123"
}

// Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 2,
    "username": "editor",
    "email": "editor@polaris.gov.in",
    "full_name": "Dr. S. Sharma (Chief Science Editor)",
    "role": "editor"
  }
}
```

### `GET /api/auth/me`
Returns current user profile decoded from the `Authorization: Bearer <token>` header.

---

## 2. Research Stations (`/api/stations`)

### `GET /api/stations`
Lists all active polar research stations and underwater observatories.

### `GET /api/stations/{code}`
Retrieves station deep dive: coordinates, elevation, live weather telemetry, linked expeditions, and media.

---

## 3. Polar Knowledge Repository (`/api/repository`)

- `GET /api/repository/summary`: High-level asset statistics.
- `GET /api/repository/expeditions`: List of expeditions with optional `region` and `year` filters.
- `GET /api/repository/expeditions/{id}`: Full expedition details and related reports, datasets, and publications.
- `GET /api/repository/reports`: List of expedition reports.
- `GET /api/repository/datasets`: List of scientific datasets with metadata.
- `GET /api/repository/datasets/{id}/preview`: First 5 rows of CSV data for live table preview and chart telemetry.
- `GET /api/repository/media`: Photos, videos, and drone surveys with tags.

---

## 4. POLAR AI RAG Assistant (`/api/ai`)

### `POST /api/ai/query`
Executes vector similarity search against the polar knowledge repository and generates a source-grounded response.
```json
// Request
{
  "query": "What were the major research objectives of this expedition?",
  "session_id": "optional-uuid"
}

// Response
{
  "session_id": "7fa8e1b2-...",
  "answer": "Based on verified NCPOR records in the POLARIS knowledge repository:\n• [43rd Indian Antarctic Expedition Scientific Report - Research Objectives, p.14]: The primary research objectives comprised atmospheric physics, glaciology, and marine biology...",
  "confidence_score": 98.4,
  "grounded": true,
  "sources_used": [
    {
      "source": "43rd Indian Antarctic Expedition Scientific Report",
      "section": "Research Objectives",
      "page": 14,
      "relevance": "High",
      "similarity_score": 94.2,
      "evidence_snippet": "The primary research objectives of the 43rd Indian Antarctic Expedition comprised atmospheric physics, glaciology, and marine biology."
    }
  ]
}
```

---

## 5. Outreach Studio (`/api/outreach`)

### `POST /api/outreach/generate`
Generates an AI outreach draft. **Status is always `Draft`**.
```json
// Request
{
  "source_type": "report",
  "source_id": 1,
  "channel": "Website Article"
}
```

### `POST /api/outreach/submit-for-review/{id}`
Submits draft to editorial verification queue (`Pending_Review`).

### `POST /api/outreach/review/{id}`
Editor approves or rejects draft (`Approved` / `Rejected`). Requires authenticated Editor or Admin credentials.

### `POST /api/outreach/publish/{id}`
Publishes approved content to public portal and social channels.

---

## 6. Polar Academy (`/api/academy`)

- `GET /api/academy/milestones`: Chronological timeline of Indian polar milestones from 1981 to 2026.
- `GET /api/academy/quizzes`: List of verified STEM quiz questions.
- `POST /api/academy/quizzes/evaluate`: Evaluates student answers and returns percentage, badge awarded, and scientific explanations.

---

## 7. Admin & Security (`/api/admin`)

- `GET /api/admin/analytics`: Aggregations for charts: resources by year, expeditions by region, and outreach status breakdown.
- `GET /api/admin/audit-logs`: Immutable action log tracking all logins, queries, content approvals, and system events.
