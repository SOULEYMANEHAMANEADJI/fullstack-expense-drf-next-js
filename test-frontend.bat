@echo off
setlocal
echo ========================================
echo Tests Frontend (Jest)
echo ========================================
pushd frontend

echo.
echo Installation des dependances...
call npm ci --legacy-peer-deps

echo.
echo Execution des tests...
set NEXT_PUBLIC_API_URL=http://localhost:8000/
call npm run test:coverage
set TEST_EXIT_CODE=%ERRORLEVEL%

echo.
echo ========================================
echo Tests termines!
echo Rapport de couverture: frontend\coverage\lcov-report\index.html
echo ========================================
popd
exit /b %TEST_EXIT_CODE%

