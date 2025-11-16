# Migration vers la version avec Catégories

## Étapes pour appliquer les nouvelles fonctionnalités

### 1. Créer les migrations

```bash
cd backend
python manage.py makemigrations
```

### 2. Appliquer les migrations

```bash
python manage.py migrate
```

### 3. Peupler la base de données avec les catégories et transactions

```bash
python manage.py seed_all
```

Cette commande va :
- Créer 12 catégories (Salaire, Freelance, Logement, Alimentation, etc.)
- Créer 30 transactions de test avec des catégories assignées
- Afficher un résumé des données créées

### 4. (Optionnel) Créer un super utilisateur pour l'admin Django

```bash
python manage.py createsuperuser
```

Puis accédez à http://localhost:8000/admin pour gérer les catégories et transactions.

## Nouvelles fonctionnalités disponibles

### API Endpoints

**Catégories:**
- `GET /api/categories/` - Liste toutes les catégories
- `POST /api/categories/` - Créer une catégorie
- `GET /api/categories/{id}/` - Détails d'une catégorie
- `PUT /api/categories/{id}/` - Modifier une catégorie
- `DELETE /api/categories/{id}/` - Supprimer une catégorie
- `GET /api/categories/statistics/` - Statistiques par catégorie

**Export:**
- `GET /api/transactions/export/csv/` - Exporter toutes les transactions en CSV

**Transactions (mis à jour):**
- Les transactions incluent maintenant un champ `category` (UUID)
- Les réponses incluent `category_details` avec les infos complètes de la catégorie
