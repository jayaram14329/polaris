# POLARIS SIH 2026 Complete Demo Flow Walkthrough

This document outlines the exact 19-step workflow demonstrated to the Smart India Hackathon jury.

---

### Step 1: Open POLARIS
- Open the application at `http://localhost:3000`.
- Notice the dark polar aesthetic: deep navy (`#060d1f`), cyan highlights (`#38bdf8`), ice blue badges, and official Ministry of Earth Sciences (MoES) / NCPOR branding.

### Step 2: View Homepage
- Inspect the hero banner: "Polar Knowledge & Outreach Intelligence System".
- Notice the top navigation bar with user role switcher (`Public`, `Researcher`, `Science Editor`, `Admin`).

### Step 3: View Statistics
- Examine the 6 primary KPI metric cards:
  - 44+ Expeditions (Since 1981)
  - 3 Permanent Stations (Maitri, Bharati, Himadri)
  - 100% Grounded RAG (Zero Hallucination)
  - 128 Indexed Reports (FAIR DataCite 4.4)
  - 42 Curated Datasets (NetCDF & CSV)
  - 185+ Outreach Products (Human-Verified Media)

### Step 4: Open Polar Map
- Click the **"Polar Station GIS"** tab or the "Open Polar Station GIS" button.
- The interactive Leaflet map loads with dark OpenStreetMap / CARTO tiles.

### Step 5: Click Research Station
- Click on the **"BHARATI"** station pin in Larsemann Hills, East Antarctica (-69.41°S, 76.19°E).
- The Station Intelligence Drawer reveals:
  - Commissioned: 2012
  - Elevation: 35m ASL
  - Live Telemetry: Temp -18.4 °C, Wind 32 knots, Pressure 984 hPa
  - Architecture: Aerodynamic design elevated on structural stilts to prevent snow accumulation.

### Step 6: View Related Expedition
- In the station drawer, click **"View Related Expedition (Step 6)"**.
- The portal transitions to the **Expedition Explorer**, displaying the **43rd Indian Scientific Expedition to Antarctica (43rd IAE)**.

### Step 7: Open Expedition Report
- Select the **"43rd Indian Antarctic Expedition Scientific Report"** (48 pages, DataCite DOI: 10.5281/zenodo.polaris43).
- View the executive summary and indexed document preview.

### Step 8: Ask POLAR AI
- Click **"Ask POLAR AI"** or type into the query box:
  `"What were the major research objectives of this expedition?"`

### Step 9: Display Answer
- POLAR AI executes dense vector similarity retrieval against indexed chunks and synthesizes a 100% factual response:
  - 1. Atmospheric Physics: Evaluating boundary-layer greenhouse gases and aerosol optical depth.
  - 2. Glaciology & Paleoclimatology: Deep ice core drilling on Princess Elizabeth Land plateau.
  - 3. Polar Biology: Mapping psychrophilic bacteria in Priyadarshini Lake.

### Step 10: Display Source Citations
- Inspect the **Sources Used** evidence card:
  - Source: `43rd Indian Antarctic Expedition Scientific Report`
  - Section: `Research Objectives`
  - Page: `14`
  - Confidence Match: `94.2%`
  - Verbatim Evidence Snippet displayed.

### Step 11: Open Outreach Studio
- Click the **"Outreach Studio"** tab.
- The Studio opens with the 43rd Expedition Report selected as the verified source.

### Step 12: Select the Expedition Report
- Source is verified: `43rd Indian Antarctic Expedition Scientific Report`.

### Step 13: Generate Multi-Channel Content
- Select a channel (e.g., **Website Article**, **Instagram**, or **Student Explanation**).
- Click **"Generate AI Draft"**.
- POLAR AI synthesizes the publication draft.
- Notice: Status is strictly **`Draft`** — it is NEVER auto-published!

### Step 14: Send Generated Content for Review
- Click **"Send for Review (Step 14)"**.
- Draft status changes to **`Pending_Review`**, entering the official editorial queue.

### Step 15: Open Editor Dashboard
- Switch user role in top header to **"Science Editor (Dr. S. Sharma)"**.
- In the active review card, notice the editorial control panel.

### Step 16: Approve the Content
- Dr. S. Sharma reviews the scientific fidelity and clicks **"Approve Content"**.
- Draft status updates to **`Approved`**, and an immutable entry is logged in the audit trail.

### Step 17: View Approved / Scheduled Content
- Click **"Publish to MoES Channels"** or view the item in the **Editorial Review Queue**.
- Status is confirmed as **`Published`**.

### Step 18: Open POLAR Academy
- Click the **"Polar Academy"** tab.
- View the **Historic Polar Milestones Timeline** (1981 - 2026).

### Step 19: Generate a Quiz from Verified Content
- Under the **Verified Polar Science Quiz** section, answer the interactive 4-choice questions.
- Click **"Submit & Grade Quiz"**.
- View instant scoring, awarded badge (`Master Polar Explorer`), and scientific explanations referencing primary NCPOR literature!
