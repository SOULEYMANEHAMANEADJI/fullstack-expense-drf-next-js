@echo off
setlocal
echo ========================================
echo Tests Complets (Backend + Frontend)
echo ========================================
echo.

echo [1/2] Tests Backend...
call .\test-backend.bat
set BACKEND_EXIT=%ERRORLEVEL%
if %BACKEND_EXIT% NEQ 0 (
    echo.
    echo ERREUR: Les tests backend ont echoue!
    pause
    exit /b %BACKEND_EXIT%
)

echo.
echo [2/2] Tests Frontend...
call .\test-frontend.bat
set FRONTEND_EXIT=%ERRORLEVEL%
if %FRONTEND_EXIT% NEQ 0 (
    echo.
    echo ERREUR: Les tests frontend ont echoue!
    pause
    exit /b %FRONTEND_EXIT%
)

echo.
echo ========================================
echo Tous les tests sont passes avec succes!
echo ========================================
pause
exit /b 0

