# Configuration CI/CD et Tests Automatisés

Ce document décrit la configuration des tests automatisés (Pytest + Jest) et du CI/CD avec GitHub Actions.

## Tests Backend (Pytest)

### Configuration

- **Fichier de configuration**: `backend/pytest.ini`
- **Framework**: Pytest avec pytest-django
- **Couverture de code**: pytest-cov

### Exécution des tests

```bash
cd backend
pytest
```

Avec couverture de code :
```bash
cd backend
pytest --cov=api --cov-report=html --cov-report=term-missing
```

### Tests disponibles

- **Tests de modèles**: `backend/api/test_models.py`
- **Tests d'API**: `backend/api/test_api.py`

## Tests Frontend (Jest)

### Configuration

- **Fichier de configuration**: `frontend/jest.config.js`
- **Framework**: Jest avec Testing Library
- **Environnement**: jsdom

### Exécution des tests

```bash
cd frontend
npm test
```

Avec couverture de code :
```bash
cd frontend
npm test -- --coverage
```

### Tests disponibles

- **Tests API**: `frontend/app/__tests__/api.test.ts`
- **Tests utilitaires**: `frontend/app/__tests__/utils.test.ts`

## CI/CD avec GitHub Actions

### Workflow principal

Le workflow CI/CD est défini dans `.github/workflows/ci.yml` et s'exécute sur :
- Push vers les branches `main` et `develop`
- Pull requests vers `main` et `develop`

### Jobs du workflow

1. **backend-tests**: Exécute les tests Pytest du backend
   - Installation des dépendances Python
   - Création du fichier `.env` pour les tests
   - Exécution des migrations
   - Exécution des tests avec couverture
   - Upload de la couverture vers Codecov

2. **frontend-tests**: Exécute les tests Jest du frontend
   - Installation des dépendances Node.js
   - Exécution du linter
   - Exécution des tests avec couverture
   - Upload de la couverture vers Codecov

3. **build-backend**: Vérifie que le backend peut être construit
   - Vérification des migrations
   - Collecte des fichiers statiques

4. **build-frontend**: Vérifie que le frontend peut être construit
   - Build Next.js
   - Upload des artefacts de build

5. **code-quality**: Analyse de qualité de code avec CodeQL

### Corrections apportées

1. **Fichier .env manquant**: Le workflow crée maintenant le fichier `.env` directement au lieu de copier depuis `.env.example`
2. **Gestion des erreurs**: Les uploads de couverture utilisent `if: always()` et `fail_ci_if_error: false` pour ne pas faire échouer le pipeline
3. **Configuration Jest**: Ajout de la configuration des variables d'environnement pour les tests
4. **Tests frontend**: Suppression de `|| true` pour que les erreurs soient détectées
5. **Variables d'environnement**: Configuration de `NEXT_PUBLIC_API_URL` dans le workflow

## Déploiement

Le workflow de déploiement est défini dans `.github/workflows/deploy.yml` et s'exécute sur :
- Push vers la branche `main`
- Création de tags `v*`

### Jobs de déploiement

1. **deploy-frontend**: Déploie le frontend sur Vercel
2. **create-release**: Crée une release GitHub lors de la création d'un tag

## Vérification locale

Pour vérifier que tout fonctionne avant de pousser :

```bash
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
npm test
```

## Problèmes résolus

- ✅ Fichier `.env.example` manquant → Création du `.env` directement dans le workflow
- ✅ Tests frontend qui échouaient silencieusement → Suppression de `|| true`
- ✅ Variables d'environnement non définies → Configuration dans `jest.setup.js` et le workflow
- ✅ Upload de couverture qui faisait échouer le pipeline → Ajout de `if: always()` et `fail_ci_if_error: false`

