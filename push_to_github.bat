@echo off
echo ===================================================
echo POLARIS - Push to GitHub (jayaram14329/polaris)
echo ===================================================
echo.
echo 1. Verifying git branch...
git branch -M main
echo.
echo 2. Pushing to https://github.com/jayaram14329/polaris.git ...
echo NOTE: A browser popup will open asking you to sign in to GitHub.
echo Please sign in with your account: jayaram14329
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] POLARIS has been pushed to https://github.com/jayaram14329/polaris !
) else (
    echo [NOTICE] If the repository does not exist on GitHub yet, please create it at:
    echo https://github.com/new?name=polaris
    echo Then run this script again.
)
echo.
pause
