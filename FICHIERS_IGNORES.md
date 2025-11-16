# 📋 Fichiers Ignorés par Git

Ce document liste tous les fichiers et dossiers qui sont ignorés par Git (via `.gitignore`).

## 🔒 Pourquoi ignorer ces fichiers ?

Ces fichiers sont générés automatiquement, contiennent des informations sensibles, ou sont spécifiques à l'environnement local. Ils ne doivent **pas** être versionnés.

## 📁 Fichiers Ignorés

### 🌐 Global

- **Fichiers OS** : `.DS_Store`, `Thumbs.db`
- **Certificats/Clés** : `*.pem`
- **Logs** : `npm-debug.log*`, `yarn-debug.log*`, etc.
- **Variables d'environnement** : `.env*`, `.env.*`

### 🎨 Frontend

- **Node modules** : `/frontend/node_modules/`
- **Build Next.js** : `/frontend/.next/`, `/frontend/out/`, `/frontend/build`
- **Rapports de couverture** : `/frontend/coverage/`
- **TypeScript** : `/frontend/next-env.d.ts`, `*.tsbuildinfo`
- **Vercel** : `/frontend/.vercel`

### 🐍 Backend

- **Environnements virtuels Python** : `/backend/venv/`, `/backend/env/`, `/backend/.venv/`
- **Fichiers compilés Python** : `*.pyc`, `*.pyo`, `*.pyd`, `__pycache__/`
- **Packages Python** : `*.egg`, `*.egg-info/`, `dist/`, `build/`
- **Base de données** : `/backend/db.sqlite3`
- **Fichiers statiques Django** : `/backend/staticfiles/`
- **Rapports de couverture pytest** :
  - `/backend/.coverage`
  - `/backend/.coverage.*`
  - `/backend/htmlcov/`
  - `/backend/coverage.xml`
  - `/backend/.pytest_cache/`

### 💻 IDE / Éditeurs

- **VS Code** : `.vscode/`
- **IntelliJ/WebStorm** : `.idea/`
- **Vim** : `*.swp`, `*.swo`, `*~`

## ✅ Fichiers qui DOIVENT être versionnés

- ✅ Code source (`.py`, `.ts`, `.tsx`, `.js`, etc.)
- ✅ Fichiers de configuration (`package.json`, `requirements.txt`, `pytest.ini`, `jest.config.js`)
- ✅ Documentation (`.md`)
- ✅ Scripts de test (`test-*.bat`, `test-*.sh`)
- ✅ Workflows CI/CD (`.github/workflows/*.yml`)

## 🚨 Fichiers qui ont été retirés du dépôt

Si vous avez déjà commité des fichiers qui devraient être ignorés :

```bash
# Retirer un fichier du cache Git (mais le garder localement)
git rm --cached backend/.coverage
git rm --cached -r backend/htmlcov/
git rm --cached -r frontend/coverage/

# Commit les changements
git add .gitignore
git commit -m "Update .gitignore: Ignorer les fichiers générés"
```

## 📝 Vérifier quels fichiers sont ignorés

```bash
# Voir tous les fichiers ignorés
git status --ignored

# Vérifier si un fichier spécifique est ignoré
git check-ignore -v path/to/file
```

## 🔍 Fichiers à surveiller

Si vous voyez ces fichiers dans `git status`, ils ne devraient probablement pas être commités :

- ❌ `backend/.coverage`
- ❌ `backend/htmlcov/`
- ❌ `backend/coverage.xml`
- ❌ `frontend/coverage/`
- ❌ `backend/venv/` ou `backend/.venv/`
- ❌ `frontend/node_modules/`
- ❌ `frontend/.next/`
- ❌ `.env` ou `.env.local`
- ❌ `*.pyc` ou `__pycache__/`

---

**Note** : Les fichiers de couverture sont générés lors de l'exécution des tests. Ils sont utiles localement mais ne doivent pas être versionnés car ils changent à chaque exécution de tests.

