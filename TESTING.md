# 🧪 Guide de Tests

Ce guide explique comment exécuter les tests automatisés pour le backend et le frontend.

## 📋 Table des Matières

- [Tests Backend (Pytest)](#tests-backend-pytest)
- [Tests Frontend (Jest)](#tests-frontend-jest)
- [CI/CD avec GitHub Actions](#cicd-avec-github-actions)
- [Coverage](#coverage)

## Tests Backend (Pytest)

### Installation des dépendances

```bash
cd backend
pip install -r requirements.txt
```

Les packages de test inclus :
- `pytest>=7.4.0` - Framework de test
- `pytest-django>=4.5.0` - Plugin Django pour pytest
- `pytest-cov>=4.1.0` - Couverture de code
- `factory-boy>=3.3.0` - Création de fixtures

### Exécuter les tests

```bash
cd backend

# Tous les tests
pytest

# Tests avec couverture
pytest --cov=api

# Tests avec rapport HTML
pytest --cov=api --cov-report=html

# Tests spécifiques
pytest api/test_models.py
pytest api/test_api.py

# Tests avec marqueurs
pytest -m unit
pytest -m api
```

### Structure des Tests Backend

```
backend/
├── api/
│   ├── test_models.py       # Tests des modèles
│   ├── test_api.py          # Tests des endpoints API
│   └── tests.py             # Tests existants (à supprimer)
└── pytest.ini               # Configuration pytest
```

### Tests Disponibles

#### test_models.py

**TestCategoryModel**
- ✅ Création de catégorie
- ✅ Unicité du nom
- ✅ Valeurs par défaut
- ✅ Tri par nom

**TestTransactionModel**
- ✅ Création de transaction positive (revenu)
- ✅ Création de transaction négative (dépense)
- ✅ Transaction avec catégorie
- ✅ Suppression en cascade (SET_NULL)
- ✅ Tri par date décroissante
- ✅ Comptage des transactions par catégorie

#### test_api.py

**TestCategoryAPI**
- ✅ Liste des catégories (GET)
- ✅ Création de catégorie (POST)
- ✅ Récupération d'une catégorie (GET /{id}/)
- ✅ Mise à jour de catégorie (PUT /{id}/)
- ✅ Suppression de catégorie (DELETE /{id}/)

**TestTransactionAPI**
- ✅ Liste des transactions avec pagination
- ✅ Pagination (15 items → 2 pages)
- ✅ Création de transaction
- ✅ Validation : texte vide
- ✅ Validation : texte trop court (< 3 caractères)
- ✅ Validation : montant zéro
- ✅ Mise à jour de transaction
- ✅ Suppression de transaction
- ✅ Filtre par type (revenus)
- ✅ Filtre par type (dépenses)
- ✅ Filtre par catégorie
- ✅ Recherche de transactions

**TestStatisticsAPI**
- ✅ Statistiques globales
- ✅ Statistiques par catégorie

**TestExportCSV**
- ✅ Export CSV avec Content-Type correct
- ✅ Export CSV avec données

### Configuration Pytest

Le fichier `pytest.ini` configure :
- Module Django à utiliser
- Patterns de fichiers de test
- Options de couverture
- Marqueurs personnalisés

### Marqueurs

```bash
# Tests unitaires uniquement
pytest -m unit

# Tests d'intégration
pytest -m integration

# Tests API
pytest -m api
```

## Tests Frontend (Jest)

### Installation des dépendances

```bash
cd frontend
npm install
```

Les packages de test inclus :
- `jest>=29.7.0` - Framework de test
- `@testing-library/react>=14.1.2` - Tests React
- `@testing-library/jest-dom>=6.1.5` - Matchers DOM
- `@testing-library/user-event>=14.5.1` - Simulation utilisateur

### Exécuter les tests

```bash
cd frontend

# Tous les tests
npm test

# Tests en mode watch
npm run test:watch

# Tests avec couverture
npm run test:coverage
```

### Structure des Tests Frontend

```
frontend/
├── app/
│   └── __tests__/
│       ├── api.test.ts      # Tests configuration API
│       └── utils.test.ts    # Tests utilitaires
├── jest.config.js           # Configuration Jest
└── jest.setup.js            # Setup Jest
```

### Tests Disponibles

#### api.test.ts

- ✅ Configuration de l'URL de base
- ✅ Présence des méthodes HTTP (GET, POST, PUT, DELETE)

#### utils.test.ts

- ✅ Formatage des dates
- ✅ Formatage des montants positifs
- ✅ Formatage des montants négatifs
- ✅ Gestion du zéro
- ✅ Validation du type de transaction

### Configuration Jest

Le fichier `jest.config.js` configure :
- Environnement jsdom
- Setup files
- Module mapper
- Seuils de couverture (70%)
- Patterns de collecte

### Seuils de Couverture

```javascript
coverageThreshold: {
  global: {
    branches: 70,
    functions: 70,
    lines: 70,
    statements: 70,
  },
}
```

## CI/CD avec GitHub Actions

Le projet inclut deux workflows GitHub Actions :

### 1. CI Pipeline (.github/workflows/ci.yml)

Déclenché sur :
- Push vers `main` ou `develop`
- Pull requests vers `main` ou `develop`

**Jobs :**

#### backend-tests
- Setup Python 3.11
- Installation des dépendances
- Migrations Django
- Tests avec pytest
- Upload couverture vers Codecov

#### frontend-tests
- Setup Node.js 20
- Installation des dépendances
- Linter
- Tests avec Jest
- Upload couverture vers Codecov

#### build-backend
- Vérification des migrations
- Collecte des fichiers statiques

#### build-frontend
- Build Next.js
- Upload des artifacts

#### code-quality
- Analyse CodeQL (JavaScript, Python)

### 2. Deploy Pipeline (.github/workflows/deploy.yml)

Déclenché sur :
- Push vers `main`
- Tags `v*` (releases)

**Jobs :**

#### deploy-frontend
- Déploiement automatique sur Vercel

#### create-release
- Création automatique de releases GitHub

### Secrets Nécessaires

Pour activer le déploiement, ajoutez ces secrets dans GitHub :

```
VERCEL_TOKEN          # Token d'API Vercel
VERCEL_ORG_ID        # ID de votre organisation Vercel
VERCEL_PROJECT_ID    # ID de votre projet Vercel
```

## Coverage

### Backend

Après avoir exécuté `pytest --cov=api --cov-report=html` :

```bash
# Ouvrir le rapport HTML
cd backend
open htmlcov/index.html  # Mac
start htmlcov/index.html # Windows
xdg-open htmlcov/index.html # Linux
```

### Frontend

Après avoir exécuté `npm run test:coverage` :

```bash
# Ouvrir le rapport HTML
cd frontend
open coverage/lcov-report/index.html  # Mac
start coverage/lcov-report/index.html # Windows
xdg-open coverage/lcov-report/index.html # Linux
```

### Codecov

Les rapports de couverture sont automatiquement envoyés à Codecov via GitHub Actions.

Vous pouvez voir les rapports sur :
```
https://codecov.io/gh/SOULEYMANEHAMANEADJI/fullstack-expense-drf-next-js
```

## Badges

Ajoutez ces badges à votre README :

```markdown
[![Backend Tests](https://github.com/SOULEYMANEHAMANEADJI/fullstack-expense-drf-next-js/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/SOULEYMANEHAMANEADJI/fullstack-expense-drf-next-js/actions)
[![codecov](https://codecov.io/gh/SOULEYMANEHAMANEADJI/fullstack-expense-drf-next-js/branch/main/graph/badge.svg)](https://codecov.io/gh/SOULEYMANEHAMANEADJI/fullstack-expense-drf-next-js)
```

## Bonnes Pratiques

### Backend

1. **Isolation** - Chaque test est isolé avec `@pytest.mark.django_db`
2. **Fixtures** - Utilisez des fixtures pour les données de test
3. **Validation** - Testez tous les cas de validation
4. **API** - Testez tous les endpoints et codes de statut

### Frontend

1. **Render** - Testez le rendu des composants
2. **Interaction** - Testez les interactions utilisateur
3. **État** - Testez les changements d'état
4. **Props** - Testez avec différentes props

### CI/CD

1. **Cache** - Les dépendances sont cachées pour accélérer
2. **Parallèle** - Les jobs tournent en parallèle
3. **Artifacts** - Les builds sont sauvegardés
4. **Security** - CodeQL analyse automatiquement le code

## Commandes Rapides

```bash
# Backend - Tests complets
cd backend && pytest --cov=api --cov-report=html

# Frontend - Tests complets
cd frontend && npm run test:coverage

# Les deux en séquentiel
cd backend && pytest && cd ../frontend && npm test

# Vérifier les workflows GitHub Actions localement (act)
act -l
act push
```

## Dépannage

### Backend

**Erreur : "Django settings not found"**
```bash
export DJANGO_SETTINGS_MODULE=backend.settings
```

**Erreur : "No module named 'api'"**
```bash
cd backend
python -m pytest
```

### Frontend

**Erreur : "Cannot find module 'next/jest'"**
```bash
npm install
```

**Erreur : "SyntaxError: Unexpected token"**
- Vérifiez que `jest.config.js` est correct
- Vérifiez que `jest.setup.js` existe

### GitHub Actions

**Erreur : "Codecov upload failed"**
- Vérifiez que le fichier de couverture existe
- Vérifiez le chemin du fichier

**Erreur : "Vercel deployment failed"**
- Vérifiez que les secrets sont configurés
- Vérifiez les IDs Vercel

## Ressources

- [Pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/)
- [Testing Library](https://testing-library.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Codecov](https://docs.codecov.com/)

---

**Happy Testing! 🧪**
