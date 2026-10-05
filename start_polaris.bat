@echo off
title POLARIS - Polar Knowledge & Outreach Intelligence System
echo ==============================================================================
echo    POLARIS - Polar Knowledge & Outreach Intelligence System
echo    Smart India Hackathon 2026 - Problem Statement SIH26063
echo    Ministry of Earth Sciences (MoES) / NCPOR
echo ==============================================================================
echo.

echo [1/3] Checking environment & seeding database...
python "%~dp0backend\sample_seed.py"

echo.
echo [2/3] Starting FastAPI Backend on http://localhost:8000 ...
start "POLARIS Backend (FastAPI)" cmd /k "cd /d %~dp0 && python run_backend.py"

echo.
echo [3/3] Starting Next.js Frontend on http://localhost:3000 ...
start "POLARIS Frontend (Next.js)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ==============================================================================
echo    POLARIS IS RUNNING!
echo    - Frontend Portal:  http://localhost:3000
echo    - Backend API:      http://localhost:8000
echo    - API Docs:         http://localhost:8000/docs
echo ==============================================================================
echo.
pause
