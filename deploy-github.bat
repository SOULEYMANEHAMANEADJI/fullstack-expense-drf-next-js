@echo off
echo ========================================
echo   Deploiement sur GitHub
echo ========================================
echo.

cd /d "%~dp0"

REM Verifier si Git est installe
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Git n'est pas installe !
    echo Installez Git depuis https://git-scm.com/
    pause
    exit /b 1
)

echo [1/6] Verification de l'image de demonstration...
if not exist "docs\images\screenshot.png" (
    echo [ATTENTION] L'image docs\images\screenshot.png n'existe pas !
    echo Veuillez ajouter une capture d'ecran avant de continuer.
    echo.
    set /p continue="Voulez-vous continuer quand meme ? (o/N) : "
    if /i not "%continue%"=="o" (
        echo Deploiement annule.
        pause
        exit /b 1
    )
)

echo [2/6] Initialisation de Git...
if not exist ".git" (
    git init
    echo Repository Git initialise.
) else (
    echo Repository Git deja initialise.
)

echo [3/6] Configuration du remote GitHub...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/SOULEYMANEHAMANEADJI/fullstack-expense-drf-next-js.git
echo Remote GitHub configure.

echo [4/6] Ajout des fichiers...
git add .
echo Fichiers ajoutes.

echo [5/6] Creation du commit...
git commit -m "🎉 Initial commit - Application complete de gestion des depenses - Backend Django REST Framework complet avec CRUD, filtres, pagination - Frontend Next.js avec React, TypeScript, TailwindCSS - Categories avec icones et couleurs personnalisees - Statistiques en temps reel - Export CSV - Interface moderne et responsive - Documentation complete - Confirmation de suppression ajoutee - 100%% fonctionnel"
if errorlevel 1 (
    echo [INFO] Aucune modification a commiter ou commit deja effectue.
)

echo [6/6] Push vers GitHub...
git branch -M main
git push -u origin main --force
if errorlevel 1 (
    echo.
    echo [ERREUR] Le push a echoue !
    echo Verifiez vos identifiants GitHub et votre connexion internet.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   DEPLOIEMENT REUSSI ! ✓
echo ========================================
echo.
echo Votre projet est maintenant sur GitHub :
echo https://github.com/SOULEYMANEHAMANEADJI/fullstack-expense-drf-next-js
echo.
echo N'oubliez pas d'ajouter :
echo - Des Topics au repository
echo - Une description
echo - Un lien website si vous deployez l'app
echo.
pause
