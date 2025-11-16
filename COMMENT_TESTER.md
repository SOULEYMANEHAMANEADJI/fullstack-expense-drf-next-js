# 🧪 Comment Tester le Projet

Ce guide explique comment exécuter les tests localement avant de pousser sur GitHub.

## 🚀 Méthode Rapide (Scripts Automatiques)

### Windows

```bash
# Tester uniquement le backend
test-backend.bat

# Tester uniquement le frontend
test-frontend.bat

# Tester les deux (recommandé)
test-all.bat
```

### Linux/Mac

```bash
# Rendre les scripts exécutables (première fois seulement)
chmod +x test-backend.sh test-frontend.sh test-all.sh

# Tester uniquement le backend
./test-backend.sh

# Tester uniquement le frontend
./test-frontend.sh

# Tester les deux (recommandé)
./test-all.sh
```

## 📝 Méthode Manuelle

### Tests Backend (Pytest)

```bash
# 1. Aller dans le dossier backend
cd backend

# 2. Installer les dépendances (si pas déjà fait)
pip install -r requirements.txt

# 3. Créer le fichier .env
echo SECRET_KEY=django-insecure-test-key-for-ci > .env
echo DEBUG=False >> .env
echo ALLOWED_HOSTS=localhost,127.0.0.1 >> .env

# 4. Exécuter les migrations
python manage.py makemigrations
python manage.py migrate

# 5. Exécuter les tests
pytest --cov=api --cov-report=html --cov-report=term-missing
```

### Tests Frontend (Jest)

```bash
# 1. Aller dans le dossier frontend
cd frontend

# 2. Installer les dépendances (si pas déjà fait)
npm ci

# 3. Exécuter les tests
# Windows (PowerShell)
$env:NEXT_PUBLIC_API_URL="http://localhost:8000/"; npm test -- --coverage --passWithNoTests --ci

# Linux/Mac
NEXT_PUBLIC_API_URL=http://localhost:8000/ npm test -- --coverage --passWithNoTests --ci
```

## ✅ Vérification Rapide

Pour une vérification rapide sans couverture :

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test -- --passWithNoTests
```

## 📊 Voir les Rapports de Couverture

### Backend
Après avoir exécuté les tests avec `--cov-report=html` :
- Ouvrir `backend/htmlcov/index.html` dans votre navigateur

### Frontend
Après avoir exécuté les tests avec `--coverage` :
- Ouvrir `frontend/coverage/lcov-report/index.html` dans votre navigateur

## 🔍 Vérifier le CI/CD

Une fois que les tests passent localement :

1. **Commit et push vos changements** :
```bash
git add .
git commit -m "Fix CI/CD: Configuration des tests automatisés"
git push
```

2. **Vérifier sur GitHub** :
   - Allez sur votre dépôt GitHub
   - Cliquez sur l'onglet "Actions"
   - Vérifiez que le workflow "CI/CD Pipeline" passe avec succès ✅

## 🐛 Dépannage

### Erreur : "pytest: command not found"
```bash
pip install pytest pytest-django pytest-cov
```

### Erreur : "npm: command not found"
```bash
# Installer Node.js depuis https://nodejs.org/
```

### Erreur : "Django settings not found"
```bash
# Assurez-vous d'être dans le dossier backend
cd backend
export DJANGO_SETTINGS_MODULE=backend.settings  # Linux/Mac
set DJANGO_SETTINGS_MODULE=backend.settings     # Windows
```

### Erreur : "Module not found"
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm ci
```

## 📋 Checklist Avant de Pousser

- [ ] Les tests backend passent (`pytest`)
- [ ] Les tests frontend passent (`npm test`)
- [ ] Aucune erreur de linting
- [ ] Les fichiers sont commités
- [ ] Le message de commit est clair

## 🎯 Prochaines Étapes

Une fois que tout fonctionne localement :

1. ✅ Commit vos changements
2. ✅ Push sur GitHub
3. ✅ Vérifier que le workflow CI/CD passe dans GitHub Actions
4. ✅ Vérifier les rapports de couverture sur Codecov (si configuré)

---

**Bon test ! 🧪**

