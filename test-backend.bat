@echo off
setlocal
echo ========================================
echo Tests Backend (Pytest)
echo ========================================
pushd backend

echo.
echo Installation des dependances...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Creation du fichier .env...
echo SECRET_KEY=django-insecure-test-key-for-ci > .env
echo DEBUG=False >> .env
echo ALLOWED_HOSTS=localhost,127.0.0.1 >> .env

echo.
echo Execution des migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Execution des tests...
pytest --cov=api --cov-report=term-missing --cov-report=html
set TEST_EXIT_CODE=%ERRORLEVEL%

echo.
echo ========================================
echo Tests termines!
echo Rapport de couverture: backend\htmlcov\index.html
echo ========================================
popd
exit /b %TEST_EXIT_CODE%

