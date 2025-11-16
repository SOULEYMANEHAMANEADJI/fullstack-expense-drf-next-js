#!/bin/bash

echo "========================================"
echo "Tests Complets (Backend + Frontend)"
echo "========================================"
echo ""

echo "[1/2] Tests Backend..."
bash test-backend.sh
if [ $? -ne 0 ]; then
    echo ""
    echo "ERREUR: Les tests backend ont échoué!"
    exit 1
fi

echo ""
echo "[2/2] Tests Frontend..."
bash test-frontend.sh
if [ $? -ne 0 ]; then
    echo ""
    echo "ERREUR: Les tests frontend ont échoué!"
    exit 1
fi

echo ""
echo "========================================"
echo "Tous les tests sont passés avec succès!"
echo "========================================"

