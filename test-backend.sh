#!/bin/bash

echo "========================================"
echo "Tests Backend (Pytest)"
echo "========================================"
cd backend

echo ""
echo "Installation des dépendances..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Création du fichier .env..."
cat > .env << EOF
SECRET_KEY=django-insecure-test-key-for-ci
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

echo ""
echo "Exécution des migrations..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Exécution des tests..."
pytest --cov=api --cov-report=term-missing --cov-report=html

echo ""
echo "========================================"
echo "Tests terminés!"
echo "Rapport de couverture: backend/htmlcov/index.html"
echo "========================================"

