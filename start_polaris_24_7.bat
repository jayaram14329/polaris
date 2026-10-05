@echo off
title POLARIS 24/7 Live Server & Cloudflare Edge Tunnel
echo ========================================================
echo POLARIS - 24/7 Live Deployment Launcher
echo ========================================================
echo.

echo [1/3] Starting FastAPI Backend on port 8000...
start /b python run_backend.py

echo [2/3] Starting Next.js Production Frontend on port 3000...
cd frontend
start /b npm start
cd ..

echo [3/3] Establishing Cloudflare Global Edge Tunnel...
start /b .\cloudflared.exe tunnel --url http://localhost:3000

echo.
echo ========================================================
echo POLARIS is now running 24/7!
echo Press Ctrl+C or close this window to stop.
echo ========================================================
pause
