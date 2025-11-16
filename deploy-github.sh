#!/bin/bash

echo "========================================"
echo "  Déploiement sur GitHub"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# Vérifier si Git est installé
if ! command -v git &> /dev/null; then
    echo "[ERREUR] Git n'est pas installé !"
    echo "Installez Git depuis https://git-scm.com/"
    exit 1
fi

echo "[1/6] Vérification de l'image de démonstration..."
if [ ! -f "docs/images/screenshot.png" ]; then
    echo "[ATTENTION] L'image docs/images/screenshot.png n'existe pas !"
    echo "Veuillez ajouter une capture d'écran avant de continuer."
    echo ""
    read -p "Voulez-vous continuer quand même ? (o/N) : " continue
    if [[ ! "$continue" =~ ^[oO]$ ]]; then
        echo "Déploiement annulé."
        exit 1
    fi
fi

echo "[2/6] Initialisation de Git..."
if [ ! -d ".git" ]; then
    git init
    echo "Repository Git initialisé."
else
    echo "Repository Git déjà initialisé."
fi

echo "[3/6] Configuration du remote GitHub..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/SOULEYMANEHAMANEADJI/fullstack-expense-drf-next-js.git
echo "Remote GitHub configuré."

echo "[4/6] Ajout des fichiers..."
git add .
echo "Fichiers ajoutés."

echo "[5/6] Création du commit..."
git commit -m "🎉 Initial commit - Application complète de gestion des dépenses

- Backend Django REST Framework complet avec CRUD, filtres, pagination
- Frontend Next.js avec React, TypeScript, TailwindCSS
- Catégories avec icônes et couleurs personnalisées
- Statistiques en temps réel
- Export CSV
- Interface moderne et responsive
- Documentation complète
- Confirmation de suppression ajoutée
- 100% fonctionnel"

if [ $? -ne 0 ]; then
    echo "[INFO] Aucune modification à commiter ou commit déjà effectué."
fi

echo "[6/6] Push vers GitHub..."
git branch -M main
git push -u origin main --force

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERREUR] Le push a échoué !"
    echo "Vérifiez vos identifiants GitHub et votre connexion internet."
    exit 1
fi

echo ""
echo "========================================"
echo "  DÉPLOIEMENT RÉUSSI ! ✓"
echo "========================================"
echo ""
echo "Votre projet est maintenant sur GitHub :"
echo "https://github.com/SOULEYMANEHAMANEADJI/fullstack-expense-drf-next-js"
echo ""
echo "N'oubliez pas d'ajouter :"
echo "- Des Topics au repository"
echo "- Une description"
echo "- Un lien website si vous déployez l'app"
echo ""
