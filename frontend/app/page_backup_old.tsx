"use client"
import { useEffect, useState } from "react";
import api from "./api";
import toast from "react-hot-toast";
import { Activity, ArrowDownCircle, ArrowUpCircle, PlusCircle, Trash, TrendingDown, TrendingUp, Wallet, Search, Filter, ChevronLeft, ChevronRight, X } from "lucide-react"

type Transaction = {
  id: string;
  text: string;
  amount: number;
  created_at: string
}

type PaginatedResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Transaction[];
}

type Statistics = {
  balance: number;
  total_income: number;
  total_expense: number;
  income_count: number;
  expense_count: number;
  total_count: number;
  avg_income: number;
  avg_expense: number;
  ratio: number;
  largest_income: Transaction | null;
  largest_expense: Transaction | null;
}

export default function Home() {
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [statistics, setStatistics] = useState<Statistics | null>(null)
  const [text, setText] = useState<string>("");
  const [amount, setAmount] = useState<number | "">("");
  const [loading, setLoading] = useState(false)

  // Pagination
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [totalCount, setTotalCount] = useState(0)

  // Filtres
  const [searchText, setSearchText] = useState("")
  const [filterType, setFilterType] = useState<"all" | "income" | "expense">("all")
  const [showFilters, setShowFilters] = useState(false)

  const getStatistics = async () => {
    try {
      const res = await api.get<Statistics>("statistics/")
      setStatistics(res.data)
    } catch (error) {
      console.error("Erreur chargement statistiques", error);
    }
  }

  const getTransactions = async (page: number = 1) => {
    try {
      let url = `transactions/?page=${page}`

      if (searchText) {
        url += `&search=${searchText}`
      }

      if (filterType !== "all") {
        url += `&type=${filterType}`
      }

      const res = await api.get<PaginatedResponse>(url)
      setTransactions(res.data.results)
      setTotalCount(res.data.count)
      setTotalPages(Math.ceil(res.data.count / 10))
      setCurrentPage(page)
    } catch (error) {
      console.error("Erreur chargement transactions", error);
      toast.error("Erreur chargement transactions")
    }
  }

  const deleteTransaction = async (id: string) => {
    try {
      await api.delete(`transactions/${id}/`)
      getTransactions(currentPage)
      getStatistics()
      toast.success("Transaction supprimée avec succès")
    } catch (error) {
      console.error("Erreur suppression transaction", error);
      toast.error("Erreur suppression transaction")
    }
  }

  const addTransaction = async () => {
    if (!text || amount == "" || isNaN(Number(amount))) {
      toast.error("Merci de remplir texte et montant valides")
      return
    }
    setLoading(true)

    try {
      await api.post<Transaction>(`transactions/`, {
        text,
        amount: Number(amount)
      })
      getTransactions(1)
      getStatistics()
      const modal = document.getElementById('my_modal_3') as HTMLDialogElement
      if (modal) {
        modal.close()
      }

      toast.success("Transaction ajoutée avec succès")
      setText("")
      setAmount("")
    } catch (error: unknown) {
      console.error("Erreur ajout transaction", error);
      const axiosError = error as { response?: { data?: { text?: string[]; amount?: string[] } } };
      const errorMessage = axiosError?.response?.data?.text?.[0] || axiosError?.response?.data?.amount?.[0] || "Erreur ajout transaction"
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    getTransactions()
    getStatistics()
  }, []);

  useEffect(() => {
    getTransactions(1)
  }, [searchText, filterType])

  const balance = statistics?.balance || 0
  const income = statistics?.total_income || 0
  const expense = statistics?.total_expense || 0
  const ratio = statistics?.ratio || 0

  const formatDate = (dateString: string) => {
    const d = new Date(dateString);
    return d.toLocaleDateString("fr-FR", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const clearFilters = () => {
    setSearchText("")
    setFilterType("all")
  }

  return (
    <div className="w-full max-w-6xl mx-auto px-4 flex flex-col gap-4">
      {/* Header avec titre */}
      <div className="text-center py-6">
        <h1 className="text-4xl font-bold">Gestion des Dépenses</h1>
        <p className="text-sm opacity-70 mt-2">Suivez vos revenus et dépenses facilement</p>
      </div>

      {/* Statistiques principales */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="rounded-2xl border-2 border-warning/10 border-dashed bg-warning/5 p-5">
          <div className="badge badge-soft mb-2">
            <Wallet className="w-4 h-4 mr-1" />
            Solde
          </div>
          <div className="stat-value text-2xl">{balance.toFixed(2)} €</div>
        </div>

        <div className="rounded-2xl border-2 border-success/10 border-dashed bg-success/5 p-5">
          <div className="badge badge-soft badge-success mb-2">
            <ArrowUpCircle className="w-4 h-4 mr-1" />
            Revenus
          </div>
          <div className="stat-value text-2xl text-success">{income.toFixed(2)} €</div>
          {statistics && <div className="text-xs opacity-70 mt-1">{statistics.income_count} transactions</div>}
        </div>

        <div className="rounded-2xl border-2 border-error/10 border-dashed bg-error/5 p-5">
          <div className="badge badge-soft badge-error mb-2">
            <ArrowDownCircle className="w-4 h-4 mr-1" />
            Dépenses
          </div>
          <div className="stat-value text-2xl text-error">{expense.toFixed(2)} €</div>
          {statistics && <div className="text-xs opacity-70 mt-1">{statistics.expense_count} transactions</div>}
        </div>
      </div>

      {/* Ratio et statistiques avancées */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-2xl border-2 border-warning/10 border-dashed bg-warning/5 p-5">
          <div className="flex justify-between items-center mb-2">
            <div className="badge badge-soft badge-warning gap-1">
              <Activity className="w-4 h-4" />
              Ratio Dépenses/Revenus
            </div>
            <div className="text-lg font-bold">{ratio.toFixed(0)}%</div>
          </div>
          <progress className="progress progress-warning w-full" value={ratio} max={100}></progress>
        </div>

        {statistics && (
          <div className="rounded-2xl border-2 border-info/10 border-dashed bg-info/5 p-5">
            <div className="badge badge-soft badge-info mb-2">Moyennes</div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <div className="opacity-70">Revenu moyen</div>
                <div className="font-bold text-success">{statistics.avg_income.toFixed(2)} €</div>
              </div>
              <div>
                <div className="opacity-70">Dépense moyenne</div>
                <div className="font-bold text-error">{statistics.avg_expense.toFixed(2)} €</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Barre de recherche et filtres */}
      <div className="flex gap-2 flex-wrap">
        <div className="flex-1 min-w-[200px]">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 opacity-50" />
            <input
              type="text"
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              placeholder="Rechercher une transaction..."
              className="input w-full pl-10"
            />
          </div>
        </div>

        <button
          className={`btn ${showFilters ? 'btn-warning' : 'btn-ghost'}`}
          onClick={() => setShowFilters(!showFilters)}
        >
          <Filter className="w-4 h-4" />
          Filtres
        </button>

        <button className="btn btn-warning" onClick={() => (document.getElementById('my_modal_3') as HTMLDialogElement).showModal()}>
          <PlusCircle className="w-4 h-4" />
          Ajouter
        </button>
      </div>

      {/* Panel de filtres */}
      {showFilters && (
        <div className="rounded-2xl border-2 border-warning/10 border-dashed bg-warning/5 p-5">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-bold">Filtres</h3>
            <button className="btn btn-sm btn-ghost" onClick={clearFilters}>
              <X className="w-4 h-4" />
              Effacer
            </button>
          </div>
          <div className="flex gap-2 flex-wrap">
            <button
              className={`btn btn-sm ${filterType === 'all' ? 'btn-warning' : 'btn-ghost'}`}
              onClick={() => setFilterType('all')}
            >
              Toutes
            </button>
            <button
              className={`btn btn-sm ${filterType === 'income' ? 'btn-success' : 'btn-ghost'}`}
              onClick={() => setFilterType('income')}
            >
              <ArrowUpCircle className="w-4 h-4" />
              Revenus
            </button>
            <button
              className={`btn btn-sm ${filterType === 'expense' ? 'btn-error' : 'btn-ghost'}`}
              onClick={() => setFilterType('expense')}
            >
              <ArrowDownCircle className="w-4 h-4" />
              Dépenses
            </button>
          </div>
        </div>
      )}

      {/* Liste des transactions */}
      <div className="overflow-x-auto rounded-2xl border-2 border-warning/10 border-dashed bg-warning/5">
        <table className="table">
          <thead>
            <tr>
              <th>#</th>
              <th>Description</th>
              <th>Montant</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {transactions.length === 0 ? (
              <tr>
                <td colSpan={5} className="text-center py-8 opacity-70">
                  Aucune transaction trouvée
                </td>
              </tr>
            ) : (
              transactions.map((t, index) => (
                <tr key={t.id}>
                  <th>{(currentPage - 1) * 10 + index + 1}</th>
                  <td>{t.text}</td>
                  <td className="font-semibold flex items-center gap-2">
                    {t.amount > 0 ? (
                      <TrendingUp className="text-success w-6 h-6" />
                    ) : (
                      <TrendingDown className="text-error w-6 h-6" />
                    )}
                    <span className={t.amount > 0 ? 'text-success' : 'text-error'}>
                      {t.amount > 0 ? `+${t.amount}` : `${t.amount}`} €
                    </span>
                  </td>
                  <td>{formatDate(t.created_at)}</td>
                  <td>
                    <button
                      onClick={() => deleteTransaction(t.id)}
                      className="btn btn-sm btn-error btn-soft"
                      title="Supprimer"
                    >
                      <Trash className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-2">
          <button
            className="btn btn-sm"
            onClick={() => getTransactions(currentPage - 1)}
            disabled={currentPage === 1}
          >
            <ChevronLeft className="w-4 h-4" />
          </button>

          <div className="flex gap-1">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                className={`btn btn-sm ${page === currentPage ? 'btn-warning' : 'btn-ghost'}`}
                onClick={() => getTransactions(page)}
              >
                {page}
              </button>
            ))}
          </div>

          <button
            className="btn btn-sm"
            onClick={() => getTransactions(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            <ChevronRight className="w-4 h-4" />
          </button>

          <div className="ml-4 text-sm opacity-70">
            {totalCount} transaction{totalCount > 1 ? 's' : ''}
          </div>
        </div>
      )}

      {/* Modal d'ajout */}
      <dialog id="my_modal_3" className="modal backdrop-blur">
        <div className="modal-box border-2 border-warning/10 border-dashed">
          <form method="dialog">
            <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
          </form>
          <h3 className="font-bold text-lg">Ajouter une transaction</h3>
          <div className="flex flex-col gap-4 mt-4">
            <div className="flex flex-col gap-2">
              <label className="label">Texte</label>
              <input
                type="text"
                name="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Entrez le texte..."
                className="input w-full"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="label">Montant (négatif = dépense, positif = revenu)</label>
              <input
                type="number"
                name="amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value === "" ? "" : Number(e.target.value))}
                placeholder="Entrez le montant..."
                className="input w-full"
              />
            </div>
            <button
              className="w-full btn btn-warning"
              onClick={addTransaction}
              disabled={loading}
              type="button"
            >
              <PlusCircle className="w-4 h-4" />
              {loading ? "Ajout..." : "Ajouter"}
            </button>
          </div>
        </div>
      </dialog>
    </div>
  );
}
