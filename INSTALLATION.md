# Guide d'Installation - Gestion des Dépenses

Application fullstack de gestion des dépenses avec Django REST Framework et Next.js.

## Prérequis

- Python 3.10+ (Version installée: 3.13.0)
- Node.js 18+ (Version installée: 22.12.0)
- pip (gestionnaire de paquets Python)
- npm ou yarn (gestionnaire de paquets Node.js)

## Installation

### 1. Backend (Django)

#### a. Accéder au dossier backend
```bash
cd backend
```

#### b. Créer un environnement virtuel (recommandé)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### c. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### d. Configurer les variables d'environnement
Le fichier `.env` est déjà créé avec les valeurs par défaut. Pour la production, modifiez:
- `SECRET_KEY`: Générez une nouvelle clé secrète
- `DEBUG`: Mettez à `False`
- `ALLOWED_HOSTS`: Ajoutez vos domaines

#### e. Effectuer les migrations
```bash
python manage.py migrate
```

#### f. (Optionnel) Peupler la base de données avec des données de test
```bash
python manage.py seed_all
```
Cette commande crée :
- 12 catégories (Salaire, Freelance, Logement, Alimentation, Transport, etc.)
- 30 transactions de test (revenus et dépenses) avec catégories assignées
- Données réparties sur les 60 derniers jours

#### g. (Optionnel) Créer un super utilisateur
```bash
python manage.py createsuperuser
```

#### h. Lancer le serveur de développement
```bash
python manage.py runserver
```

Le backend sera accessible sur: http://localhost:8000

### 2. Frontend (Next.js)

#### a. Accéder au dossier frontend
```bash
cd frontend
```

#### b. Installer les dépendances
```bash
npm install
# ou
yarn install
```

#### c. Configurer les variables d'environnement
Le fichier `.env.local` est déjà créé avec:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/
```

#### d. Lancer le serveur de développement
```bash
npm run dev
# ou
yarn dev
```

Le frontend sera accessible sur: http://localhost:3000

## Structure du Projet

```
fullstack-expense-main/
├── backend/                 # API Django
│   ├── api/                 # Application principale
│   │   ├── models.py        # Modèle Transaction
│   │   ├── serializers.py   # Sérialiseurs avec validation
│   │   ├── views.py         # Vues API REST
│   │   └── urls.py          # Routes API
│   ├── backend/             # Configuration Django
│   │   └── settings.py      # Paramètres (avec env)
│   ├── .env                 # Variables d'environnement
│   └── requirements.txt     # Dépendances Python
│
└── frontend/                # Application Next.js
    ├── app/                 # App Router Next.js 15
    │   ├── page.tsx         # Page principale
    │   ├── layout.tsx       # Layout global
    │   └── api.ts           # Client Axios
    ├── .env.local           # Variables d'environnement
    └── package.json         # Dépendances Node.js
```

## API Endpoints

### Transactions

- **GET** `/api/transactions/` - Liste toutes les transactions (paginée)
  - Paramètres de pagination:
    - `page`: Numéro de page (défaut: 1)
    - `page_size`: Nombre d'éléments par page (défaut: 10, max: 100)
  - Paramètres de filtrage:
    - `type`: Filtrer par type (`income` ou `expense`)
    - `search`: Rechercher dans le texte
    - `min_amount`: Montant minimum
    - `max_amount`: Montant maximum
    - `start_date`: Date de début (format ISO)
    - `end_date`: Date de fin (format ISO)
  - Paramètres de tri:
    - `ordering`: Trier par champ (`created_at`, `-created_at`, `amount`, `-amount`)

- **POST** `/api/transactions/` - Créer une transaction
  ```json
  {
    "text": "Salaire",
    "amount": 2500.00
  }
  ```
- **GET** `/api/transactions/{id}/` - Récupérer une transaction
- **PUT** `/api/transactions/{id}/` - Mettre à jour une transaction
- **DELETE** `/api/transactions/{id}/` - Supprimer une transaction

### Statistiques

- **GET** `/api/statistics/` - Obtenir les statistiques globales
  - Retourne:
    - `balance`: Solde total
    - `total_income`: Total des revenus
    - `total_expense`: Total des dépenses
    - `income_count`: Nombre de revenus
    - `expense_count`: Nombre de dépenses
    - `total_count`: Nombre total de transactions
    - `avg_income`: Revenu moyen
    - `avg_expense`: Dépense moyenne
    - `ratio`: Ratio dépenses/revenus (%)
    - `largest_income`: Plus grand revenu
    - `largest_expense`: Plus grande dépense

## Validation

### Backend
- Le texte doit contenir au moins 3 caractères
- Le montant ne peut pas être zéro
- Les espaces sont automatiquement supprimés

### Frontend
- Vérification que le texte et le montant sont fournis
- Vérification que le montant est un nombre valide

## Technologies Utilisées

### Backend
- Django 5.2
- Django REST Framework
- django-cors-headers
- python-dotenv
- SQLite (base de données)

### Frontend
- Next.js 15.4.5 (avec Turbopack)
- React 19.1.0
- TypeScript
- TailwindCSS 4
- DaisyUI 5.0.50
- Axios
- react-hot-toast
- lucide-react (icônes)

## Fonctionnalités

- ✅ Ajout de transactions (revenus/dépenses)
- ✅ Suppression de transactions
- ✅ Calcul automatique du solde
- ✅ Calcul des revenus totaux
- ✅ Calcul des dépenses totales
- ✅ Ratio dépenses/revenus avec barre de progression
- ✅ **Pagination** (10 transactions par page)
- ✅ **Recherche** par texte
- ✅ **Filtres** par type (revenus/dépenses)
- ✅ **Statistiques avancées** (moyennes, plus grandes transactions)
- ✅ Dates formatées en français
- ✅ Interface responsive avec DaisyUI
- ✅ Notifications toast
- ✅ Validation des données
- ✅ Seeder avec 30 transactions de test

## Prochaines Étapes

### Améliorations suggérées
1. Ajouter l'authentification utilisateur (JWT)
2. Ajouter la pagination pour les transactions
3. Ajouter des filtres (par date, montant, type)
4. Ajouter des catégories pour les transactions
5. Ajouter des graphiques (revenus/dépenses par mois)
6. Exporter les données (CSV, PDF)
7. Ajouter des tests unitaires
8. Déployer en production (Docker, Heroku, Vercel)

## Problèmes Courants

### Le frontend ne peut pas se connecter au backend
- Vérifiez que le backend est lancé sur http://localhost:8000
- Vérifiez que CORS est correctement configuré dans settings.py
- Vérifiez la variable `NEXT_PUBLIC_API_URL` dans `.env.local`

### Erreur "Module not found"
- Backend: Assurez-vous que l'environnement virtuel est activé
- Frontend: Exécutez `npm install` pour installer les dépendances

### Erreur de migration
```bash
python manage.py migrate --run-syncdb
```

## Production

Pour déployer en production:

1. Générez une nouvelle `SECRET_KEY`
2. Mettez `DEBUG=False`
3. Configurez `ALLOWED_HOSTS`
4. Utilisez PostgreSQL au lieu de SQLite
5. Configurez un serveur web (Nginx, Apache)
6. Utilisez Gunicorn ou uWSGI pour Django
7. Build le frontend: `npm run build`
8. Configurez les variables d'environnement de production

## Support

Pour toute question ou problème, consultez la documentation:
- Django: https://docs.djangoproject.com/
- Next.js: https://nextjs.org/docs
