# Frontend - Fonctionnalités à Ajouter

Le backend est 100% complet avec CRUD, catégories, export CSV, etc.
Le frontend actuel a CREATE, READ, DELETE mais manque UPDATE et catégories.

## 🔴 Ce Qu'il Manque

### 1. UPDATE (Modification de Transaction)

**Fichier:** `app/page.tsx`

**Ajouter un état pour l'édition:**
```typescript
const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null)
const [isEditMode, setIsEditMode] = useState(false)
```

**Fonction de mise à jour:**
```typescript
const updateTransaction = async () => {
  if (!editingTransaction) return

  try {
    await api.put(`transactions/${editingTransaction.id}/`, {
      text,
      amount: Number(amount),
      category: selectedCategory || null
    })
    getTransactions(currentPage)
    getStatistics()
    closeModal()
    toast.success("Transaction modifiée avec succès")
  } catch (error: any) {
    toast.error("Erreur lors de la modification")
  }
}
```

**Bouton Modifier dans le tableau:**
```tsx
<button
  onClick={() => {
    setEditingTransaction(t)
    setIsEditMode(true)
    setText(t.text)
    setAmount(t.amount)
    setSelectedCategory(t.category || "")
    (document.getElementById('my_modal_3') as HTMLDialogElement).showModal()
  }}
  className="btn btn-sm btn-warning"
>
  <Edit className="w-4 h-4" />
</button>
```

**Import à ajouter:**
```typescript
import { Edit, Download } from "lucide-react"
```

### 2. Catégories

**Types TypeScript:**
```typescript
type Category = {
  id: string;
  name: string;
  icon: string;
  color: string;
  transactions_count: number;
}

type Transaction = {
  id: string;
  text: string;
  amount: number;
  category: string | null;
  category_details: Category | null;
  created_at: string;
}
```

**État pour les catégories:**
```typescript
const [categories, setCategories] = useState<Category[]>([])
const [selectedCategory, setSelectedCategory] = useState<string>("")
const [filterCategory, setFilterCategory] = useState<string>("")
```

**Charger les catégories:**
```typescript
const getCategories = async () => {
  try {
    const res = await api.get<Category[]>("categories/")
    setCategories(res.data)
  } catch (error) {
    console.error("Erreur chargement catégories", error)
  }
}

// Dans useEffect
useEffect(() => {
  getTransactions()
  getStatistics()
  getCategories()  // <-- Ajouter
}, [])
```

**Sélecteur de catégorie dans le modal:**
```tsx
<div className="flex flex-col gap-2">
  <label className="label">Catégorie</label>
  <select
    value={selectedCategory}
    onChange={(e) => setSelectedCategory(e.target.value)}
    className="select w-full"
  >
    <option value="">Sans catégorie</option>
    {categories.map(cat => (
      <option key={cat.id} value={cat.id}>
        {cat.icon} {cat.name}
      </option>
    ))}
  </select>
</div>
```

**Afficher la catégorie dans le tableau:**
```tsx
<td>
  {t.category_details ? (
    <span
      className="badge"
      style={{
        backgroundColor: t.category_details.color,
        color: '#fff'
      }}
    >
      {t.category_details.icon} {t.category_details.name}
    </span>
  ) : (
    <span className="text-gray-400 text-sm">Sans catégorie</span>
  )}
</td>
```

**Filtre par catégorie:**
```tsx
<select
  value={filterCategory}
  onChange={(e) => setFilterCategory(e.target.value)}
  className="select select-sm"
>
  <option value="">Toutes les catégories</option>
  {categories.map(cat => (
    <option key={cat.id} value={cat.id}>
      {cat.icon} {cat.name}
    </option>
  ))}
</select>
```

**Ajouter le filtre dans getTransactions:**
```typescript
if (filterCategory) {
  url += `&category=${filterCategory}`
}
```

### 3. Export CSV

**Fonction d'export:**
```typescript
const exportCSV = () => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/'
  window.open(`${apiUrl}api/transactions/export/csv/`, '_blank')
  toast.success("Export CSV lancé")
}
```

**Bouton Export:**
```tsx
<button className="btn btn-success" onClick={exportCSV}>
  <Download className="w-4 h-4" />
  Export CSV
</button>
```

### 4. Modifications dans addTransaction

```typescript
const addTransaction = async () => {
  if (!text || amount == "" || isNaN(Number(amount))) {
    toast.error("Merci de remplir texte et montant valides")
    return
  }
  setLoading(true)

  try {
    await api.post<Transaction>(`transactions/`, {
      text,
      amount: Number(amount),
      category: selectedCategory || null  // <-- Ajouter
    })
    getTransactions(1)
    getStatistics()
    closeModal()  // Nouvelle fonction helper
    toast.success("Transaction ajoutée avec succès")
  } catch (error: any) {
    const errorMessage = error?.response?.data?.text?.[0] ||
                        error?.response?.data?.amount?.[0] ||
                        "Erreur ajout transaction"
    toast.error(errorMessage)
  } finally {
    setLoading(false)
  }
}
```

### 5. Helper Functions

```typescript
const closeModal = () => {
  const modal = document.getElementById('my_modal_3') as HTMLDialogElement
  if (modal) modal.close()

  // Reset
  setText("")
  setAmount("")
  setSelectedCategory("")
  setEditingTransaction(null)
  setIsEditMode(false)
}

const handleSubmit = () => {
  if (isEditMode) {
    updateTransaction()
  } else {
    addTransaction()
  }
}
```

### 6. Modifier le Modal

**Titre dynamique:**
```tsx
<h3 className="font-bold text-lg">
  {isEditMode ? "Modifier la transaction" : "Ajouter une transaction"}
</h3>
```

**Bouton submit:**
```tsx
<button
  className="w-full btn btn-warning"
  onClick={handleSubmit}
  disabled={loading}
  type="button"
>
  <PlusCircle className="w-4 h-4" />
  {loading ? "..." : (isEditMode ? "Modifier" : "Ajouter")}
</button>
```

## 🎨 Layout Suggéré

```
┌─────────────────────────────────────────────────┐
│  Gestion des Dépenses                          │
├─────────────────────────────────────────────────┤
│  [Solde]  [Revenus]  [Dépenses]                │
├─────────────────────────────────────────────────┤
│  [Ratio] [Moyennes]                             │
├─────────────────────────────────────────────────┤
│  [🔍 Recherche] [Filtres ▼] [+ Ajouter] [⬇ CSV] │
├─────────────────────────────────────────────────┤
│  Tableau des transactions                       │
│  # | Description | Catégorie | Montant | Date   │
│  1 | Salaire     | 💼 Salaire | +2500€ | ...    │
│  2 | Loyer       | 🏠 Logement | -850€  | ...    │
│    [✏️ Modifier] [🗑️ Supprimer]                 │
├─────────────────────────────────────────────────┤
│  [◀ Prev] [1] [2] [3] [Next ▶]  30 transactions│
└─────────────────────────────────────────────────┘
```

## 📝 Ordre d'Implémentation Recommandé

1. ✅ Ajouter les types TypeScript pour Category
2. ✅ Charger les catégories (getCategories)
3. ✅ Ajouter le sélecteur de catégorie au modal
4. ✅ Afficher la catégorie dans le tableau avec badge
5. ✅ Ajouter le bouton "Modifier" avec icône Edit
6. ✅ Implémenter updateTransaction()
7. ✅ Gérer isEditMode dans le modal
8. ✅ Ajouter le filtre par catégorie
9. ✅ Ajouter le bouton Export CSV
10. ✅ Tester tout !

## 🚀 Résultat Final

Une fois terminé, vous aurez :
- ✅ CRUD Complet (Create, Read, Update, Delete)
- ✅ Catégories avec icônes et couleurs
- ✅ Filtres avancés (type, catégorie, recherche)
- ✅ Export CSV
- ✅ Pagination
- ✅ Statistiques visuelles
- ✅ Interface moderne et responsive

## 💡 Exemple de Code Complet

Si vous voulez le code complet tout fait, je peux le générer.
Dites-moi et je créerai le fichier `page.tsx` complet avec tout !
