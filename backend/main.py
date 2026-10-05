import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.sample_seed import seed_database
from backend.routers import (
    auth_routes,
    repository_routes,
    station_routes,
    search_routes,
    rag_routes,
    outreach_routes,
    academy_routes,
    admin_routes
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal (SIH26063 - MoES/NCPOR)"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event: Initialize & seed database
@app.on_event("startup")
def on_startup():
    print("POLARIS Backend Starting Up...")
    seed_database()
    print("POLARIS Backend Ready to Serve.")

# Mount API Routers
app.include_router(auth_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(repository_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(station_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(search_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(rag_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(outreach_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(academy_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin_routes.router, prefix=settings.API_V1_PREFIX)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

DOWNLOADS_DIR = os.path.join(BASE_DIR, "explainer_video_output")

if os.path.exists(DOWNLOADS_DIR):
    app.mount("/downloads", StaticFiles(directory=DOWNLOADS_DIR), name="downloads")
    app.mount("/api/downloads", StaticFiles(directory=DOWNLOADS_DIR), name="api_downloads")

@app.get("/download-portal", response_class=HTMLResponse)
@app.get("/api/download-portal", response_class=HTMLResponse)
def download_portal():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>POLARIS | SIH26063 Project Explainer Video & Download Center</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: linear-gradient(135deg, #0A192F 0%, #0B132B 50%, #111D4A 100%);
      color: #E2E8F0;
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      padding: 40px 20px;
    }
    .container {
      max-width: 1000px;
      margin: 0 auto;
    }
    header {
      text-align: center;
      margin-bottom: 35px;
    }
    .badge {
      display: inline-block;
      padding: 6px 16px;
      background: rgba(100, 223, 223, 0.15);
      border: 1px solid #64DFDF;
      color: #64DFDF;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 12px;
    }
    h1 {
      font-family: 'Outfit', sans-serif;
      font-size: 38px;
      font-weight: 800;
      color: #FFFFFF;
      margin-bottom: 10px;
    }
    .subtitle {
      font-size: 16px;
      color: #94A3B8;
      max-width: 700px;
      margin: 0 auto;
    }
    .video-card {
      background: rgba(15, 30, 60, 0.7);
      border: 1px solid rgba(100, 223, 223, 0.3);
      border-radius: 16px;
      padding: 24px;
      backdrop-filter: blur(12px);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
      margin-bottom: 35px;
    }
    video {
      width: 100%;
      border-radius: 10px;
      background: #000;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-bottom: 35px;
    }
    .card {
      background: rgba(15, 30, 60, 0.6);
      border: 1px solid rgba(70, 110, 160, 0.3);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
    }
    .card:hover {
      border-color: #64DFDF;
      transform: translateY(-3px);
      background: rgba(20, 42, 78, 0.8);
    }
    .card h3 {
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      color: #FFFFFF;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .card p {
      font-size: 13px;
      color: #94A3B8;
      margin-bottom: 16px;
      line-height: 1.5;
    }
    .file-meta {
      font-size: 12px;
      color: #64DFDF;
      margin-bottom: 16px;
      font-weight: 600;
    }
    .btn {
      display: inline-block;
      text-align: center;
      padding: 12px 20px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      text-decoration: none;
      transition: background 0.2s ease, transform 0.1s ease;
      cursor: pointer;
    }
    .btn-primary {
      background: #00B4D8;
      color: #0A192F;
    }
    .btn-primary:hover {
      background: #64DFDF;
    }
    .btn-secondary {
      background: rgba(255, 255, 255, 0.1);
      color: #FFFFFF;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.2);
    }
    .btn-amber {
      background: #F59E0B;
      color: #0A192F;
    }
    .btn-amber:hover {
      background: #FBBF24;
    }
    footer {
      text-align: center;
      font-size: 13px;
      color: #64748B;
      margin-top: 30px;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge">SIH26063 • MoES / NCPOR</div>
      <h1>POLARIS Jury Demonstration Center</h1>
      <p class="subtitle">Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal</p>
    </header>

    <div class="video-card">
      <h2 style="font-family: 'Outfit'; font-size: 20px; color: #64DFDF; margin-bottom: 14px;">▶ Video Preview (Full HD 1080p • 4m 28s)</h2>
      <video controls poster="/api/downloads/real_demo_scenes/real_scene_01.png">
        <source src="/api/downloads/POLARIS_SIH26063_Real_Product_Demo_Video.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>

    <div class="grid">
      <div class="card" style="border-color: #64DFDF;">
        <div>
          <h3>📥 Master Demo Video</h3>
          <p>Full HD 1080p demonstration video featuring the live software interaction, en-IN voiceover, ambient audio, and burned-in subtitles.</p>
          <div class="file-meta">MP4 Video • 8.48 MB • 04:28</div>
        </div>
        <a href="/api/downloads/POLARIS_SIH26063_Real_Product_Demo_Video.mp4" download class="btn btn-primary">Download Master Video</a>
      </div>

      <div class="card" style="border-color: #F59E0B;">
        <div>
          <h3>📦 Complete Jury Package</h3>
          <p>All-in-one ZIP archive containing the Master MP4 Video, Subtitle File (.srt), and Master Voiceover Script (.txt).</p>
          <div class="file-meta">ZIP Archive • 7.81 MB</div>
        </div>
        <a href="/api/downloads/POLARIS_SIH26063_Jury_Package.zip" download class="btn btn-amber">Download All in ZIP</a>
      </div>

      <div class="card">
        <div>
          <h3>📝 Synchronized Subtitles</h3>
          <p>Standard SRT subtitle file with 36 calibrated timestamps matching every spoken line in the video.</p>
          <div class="file-meta">SRT File • 5.13 KB</div>
        </div>
        <a href="/api/downloads/POLARIS_SIH26063_Subtitles.srt" download class="btn btn-secondary">Download Subtitles (.srt)</a>
      </div>

      <div class="card">
        <div>
          <h3>📄 Master Script & Guide</h3>
          <p>Complete scene-by-scene script text, visual interaction mappings, and SIH26063 jury evaluation alignment.</p>
          <div class="file-meta">Text Document • 21.52 KB</div>
        </div>
        <a href="/api/downloads/POLARIS_SIH26063_Voiceover_Script.txt" download class="btn btn-secondary">Download Script (.txt)</a>
      </div>

      <div class="card">
        <div>
          <h3>🎬 High-Contrast Open Captions</h3>
          <p>Alternative video render with high-contrast burned-in Segoe UI Semibold typography and dark backdrop bars.</p>
          <div class="file-meta">MP4 Video • 10.51 MB • 04:28</div>
        </div>
        <a href="/api/downloads/POLARIS_SIH26063_Explainer_Video_Hardcoded_Subtitles.mp4" download class="btn btn-secondary">Download Open-Captions MP4</a>
      </div>

      <div class="card" style="border-color: #00B4D8;">
        <div>
          <h3>📊 Official Presentation (PDF)</h3>
          <p>Updated SIH26063 presentation deck with prototype video links, GitHub repository, live URL, and scanned QR code.</p>
          <div class="file-meta">PDF Document • 1.36 MB</div>
        </div>
        <a href="/api/downloads/POLARIS_SIH26063_Presentation_Final.pdf" download class="btn btn-primary">Download Presentation (PDF)</a>
      </div>

      <div class="card">
        <div>
          <h3>🌐 Live Portal Access</h3>
          <p>Access the live interactive application running on the Cloudflare Edge network 24/7.</p>
          <div class="file-meta">Web Application • Active</div>
        </div>
        <a href="/" target="_blank" class="btn btn-secondary">Open Live Portal</a>
      </div>
    </div>

    <footer>
      POLARIS — Polar Knowledge & Outreach Intelligence System | Smart India Hackathon SIH26063
    </footer>
  </div>
</body>
</html>
"""
    return HTMLResponse(content=html_content)

@app.get("/")
def root():
    return {
        "system": "POLARIS",
        "description": "Polar Knowledge & Outreach Intelligence System",
        "problem_statement": "SIH26063",
        "organization": "Ministry of Earth Sciences (MoES) / NCPOR",
        "status": "Operational",
        "api_docs": "/docs",
        "download_center": "/download-portal",
        "version": settings.VERSION
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "POLARIS Backend API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

