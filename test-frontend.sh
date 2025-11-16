#!/bin/bash

echo "========================================"
echo "Tests Frontend (Jest)"
echo "========================================"
cd frontend

echo ""
echo "Installation des dépendances..."
npm ci

echo ""
echo "Exécution des tests..."
export NEXT_PUBLIC_API_URL=http://localhost:8000/
npm test -- --coverage --passWithNoTests --ci

echo ""
echo "========================================"
echo "Tests terminés!"
echo "Rapport de couverture: frontend/coverage/lcov-report/index.html"
echo "========================================"

