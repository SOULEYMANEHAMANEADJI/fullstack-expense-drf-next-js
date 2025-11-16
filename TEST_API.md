# Tests API - Guide de Vérification Rapide

## Prérequis
- Backend lancé sur http://localhost:8000
- Base de données migrée et peuplée avec `python manage.py seed_all`

## Tests avec cURL (Windows PowerShell)

### 1. Lister toutes les transactions (page 1)
```bash
curl http://localhost:8000/api/transactions/
```

**Résultat attendu :**
```json
{
  "count": 30,
  "next": "http://localhost:8000/api/transactions/?page=2",
  "previous": null,
  "results": [ ... 10 transactions ... ]
}
```

### 2. Rechercher une transaction
```bash
curl "http://localhost:8000/api/transactions/?search=Salaire"
```

**Résultat attendu :** Transactions contenant "Salaire" dans le texte

### 3. Filtrer par type (revenus uniquement)
```bash
curl "http://localhost:8000/api/transactions/?type=income"
```

**Résultat attendu :** Uniquement des transactions avec amount > 0

### 4. Filtrer par type (dépenses uniquement)
```bash
curl "http://localhost:8000/api/transactions/?type=expense"
```

**Résultat attendu :** Uniquement des transactions avec amount < 0

### 5. Lister toutes les catégories
```bash
curl http://localhost:8000/api/categories/
```

**Résultat attendu :**
```json
[
  {
    "id": "uuid-here",
    "name": "Salaire",
    "icon": "💼",
    "color": "#10B981",
    "created_at": "2024-...",
    "transactions_count": 5
  },
  ...
]
```

### 6. Filtrer par catégorie
Copiez l'UUID d'une catégorie depuis le résultat précédent, puis :
```bash
curl "http://localhost:8000/api/transactions/?category=UUID-ICI"
```

**Résultat attendu :** Uniquement les transactions de cette catégorie

### 7. Obtenir les statistiques globales
```bash
curl http://localhost:8000/api/statistics/
```

**Résultat attendu :**
```json
{
  "balance": 1234.56,
  "total_income": 5000.00,
  "total_expense": -3765.44,
  "income_count": 10,
  "expense_count": 20,
  "total_count": 30,
  "avg_income": 500.00,
  "avg_expense": -188.27,
  "ratio": 75.31,
  "largest_income": { ... },
  "largest_expense": { ... }
}
```

### 8. Obtenir les statistiques par catégorie
```bash
curl http://localhost:8000/api/categories/statistics/
```

**Résultat attendu :**
```json
[
  {
    "category": {
      "id": "uuid",
      "name": "Salaire",
      "icon": "💼",
      "color": "#10B981",
      ...
    },
    "total": 2500.00,
    "count": 5
  },
  ...
]
```

### 9. Créer une nouvelle transaction
```bash
curl -X POST http://localhost:8000/api/transactions/ ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Test API\",\"amount\":100.50,\"category\":null}"
```

**Résultat attendu :**
```json
{
  "id": "nouveau-uuid",
  "text": "Test API",
  "amount": "100.50",
  "category": null,
  "category_details": null,
  "created_at": "2024-..."
}
```

### 10. Modifier une transaction
Récupérez d'abord l'UUID d'une transaction :
```bash
curl -X PUT http://localhost:8000/api/transactions/UUID-ICI/ ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Transaction modifiée\",\"amount\":200.00,\"category\":null}"
```

**Résultat attendu :** Transaction mise à jour

### 11. Supprimer une transaction
```bash
curl -X DELETE http://localhost:8000/api/transactions/UUID-ICI/
```

**Résultat attendu :** Status 204 No Content

### 12. Export CSV
Ouvrez dans un navigateur :
```
http://localhost:8000/api/transactions/export/csv/
```

**Résultat attendu :** Téléchargement d'un fichier `transactions.csv`

### 13. Pagination (page 2)
```bash
curl "http://localhost:8000/api/transactions/?page=2"
```

**Résultat attendu :** 10 transactions suivantes

### 14. Combiner plusieurs filtres
```bash
curl "http://localhost:8000/api/transactions/?type=expense&search=Loyer"
```

**Résultat attendu :** Dépenses contenant "Loyer"

### 15. Tri par montant (croissant)
```bash
curl "http://localhost:8000/api/transactions/?ordering=amount"
```

**Résultat attendu :** Transactions triées par montant croissant

### 16. Tri par montant (décroissant)
```bash
curl "http://localhost:8000/api/transactions/?ordering=-amount"
```

**Résultat attendu :** Transactions triées par montant décroissant

## Tests avec Postman ou Insomnia

### Collection de tests

#### GET - Liste des transactions
```
GET http://localhost:8000/api/transactions/
```

#### GET - Recherche
```
GET http://localhost:8000/api/transactions/?search=Salaire
```

#### GET - Filtre par type
```
GET http://localhost:8000/api/transactions/?type=income
```

#### GET - Filtre par catégorie
```
GET http://localhost:8000/api/transactions/?category=UUID-ICI
```

#### GET - Statistiques
```
GET http://localhost:8000/api/statistics/
```

#### GET - Catégories
```
GET http://localhost:8000/api/categories/
```

#### GET - Statistiques par catégorie
```
GET http://localhost:8000/api/categories/statistics/
```

#### POST - Créer une transaction
```
POST http://localhost:8000/api/transactions/
Content-Type: application/json

{
  "text": "Test Postman",
  "amount": 150.75,
  "category": null
}
```

#### PUT - Modifier une transaction
```
PUT http://localhost:8000/api/transactions/UUID-ICI/
Content-Type: application/json

{
  "text": "Transaction modifiée",
  "amount": 200.00,
  "category": null
}
```

#### DELETE - Supprimer une transaction
```
DELETE http://localhost:8000/api/transactions/UUID-ICI/
```

## Tests Frontend

### 1. Ouvrir l'application
```
http://localhost:3000
```

### 2. Vérifier l'affichage
- [ ] Les statistiques sont visibles (solde, revenus, dépenses, ratio)
- [ ] La liste des transactions s'affiche
- [ ] Les badges de catégories sont colorés avec icônes
- [ ] La pagination est présente

### 3. Tester la recherche
- [ ] Taper "Salaire" dans la barre de recherche
- [ ] Vérifier que seules les transactions contenant "Salaire" apparaissent
- [ ] Effacer la recherche

### 4. Tester les filtres de type
- [ ] Cliquer sur "Revenus" → uniquement les montants positifs
- [ ] Cliquer sur "Dépenses" → uniquement les montants négatifs
- [ ] Cliquer sur "Toutes" → tout s'affiche

### 5. Tester le filtre par catégorie
- [ ] Ouvrir le panel "Filtres"
- [ ] Sélectionner une catégorie dans le dropdown
- [ ] Vérifier que seules les transactions de cette catégorie s'affichent
- [ ] Cliquer sur "Effacer" pour réinitialiser

### 6. Tester l'ajout
- [ ] Cliquer sur "Ajouter"
- [ ] Remplir le formulaire :
  - Texte : "Test Frontend"
  - Montant : 99.99
  - Catégorie : Sélectionner une catégorie
- [ ] Cliquer sur "Ajouter"
- [ ] Vérifier que la transaction apparaît
- [ ] Vérifier que les statistiques sont mises à jour

### 7. Tester la modification
- [ ] Cliquer sur le bouton "Modifier" (icône crayon) d'une transaction
- [ ] Vérifier que le formulaire est pré-rempli
- [ ] Modifier le texte et/ou le montant
- [ ] Cliquer sur "Modifier"
- [ ] Vérifier que la transaction est mise à jour

### 8. Tester la suppression
- [ ] Cliquer sur le bouton "Supprimer" (icône poubelle)
- [ ] Vérifier que la transaction disparaît
- [ ] Vérifier que les statistiques sont mises à jour

### 9. Tester l'export CSV
- [ ] Cliquer sur "Export CSV"
- [ ] Vérifier qu'un fichier `transactions.csv` se télécharge
- [ ] Ouvrir le CSV et vérifier les colonnes :
  - ID
  - Texte
  - Montant
  - Catégorie
  - Date de création

### 10. Tester la pagination
- [ ] Si plus de 10 transactions, vérifier la présence de numéros de page
- [ ] Cliquer sur "Page 2"
- [ ] Vérifier que les transactions changent
- [ ] Utiliser les boutons précédent/suivant

## Checklist Complète

### Backend ✅
- [ ] Les routes fonctionnent
- [ ] La pagination retourne 10 éléments par page
- [ ] Le filtre par type fonctionne
- [ ] Le filtre par catégorie fonctionne
- [ ] La recherche fonctionne
- [ ] Les statistiques sont correctes
- [ ] L'export CSV fonctionne
- [ ] Le CRUD complet fonctionne

### Frontend ✅
- [ ] L'affichage est correct
- [ ] Les filtres fonctionnent
- [ ] La recherche fonctionne
- [ ] La pagination fonctionne
- [ ] Les catégories s'affichent avec couleurs et icônes
- [ ] L'ajout fonctionne
- [ ] La modification fonctionne
- [ ] La suppression fonctionne
- [ ] L'export CSV fonctionne
- [ ] Les statistiques se mettent à jour

### Intégration ✅
- [ ] Le frontend communique correctement avec le backend
- [ ] Les filtres frontend sont bien transmis au backend
- [ ] Les données sont correctement formatées
- [ ] Les erreurs sont gérées avec des toasts
- [ ] L'interface est responsive

## Erreurs Courantes et Solutions

### Erreur 1 : CORS
**Symptôme :** Erreur CORS dans la console du navigateur

**Solution :**
```python
# Dans backend/backend/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### Erreur 2 : API non trouvée
**Symptôme :** 404 Not Found sur les appels API

**Solution :** Vérifier que le backend tourne sur http://localhost:8000

### Erreur 3 : Table n'existe pas
**Symptôme :** `no such table: api_category`

**Solution :**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Erreur 4 : Export CSV ne fonctionne pas
**Symptôme :** 404 sur `/api/transactions/export/csv/`

**Solution :** Vérifier l'ordre des routes dans `api/urls.py`. Les routes spécifiques doivent être AVANT les routes avec paramètres.

### Erreur 5 : Filtre par catégorie ne fonctionne pas
**Symptôme :** Le filtre par catégorie n'affecte pas les résultats

**Solution :** Vérifier que le backend filtre bien par `category__id` dans `views.py`

## Tout Fonctionne ? 🎉

Si tous les tests passent, félicitations ! L'application est 100% fonctionnelle avec :
- CRUD complet
- Filtres avancés
- Pagination
- Catégories avec icônes et couleurs
- Export CSV
- Statistiques en temps réel
- Interface moderne et responsive
