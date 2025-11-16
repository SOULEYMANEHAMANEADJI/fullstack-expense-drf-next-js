from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Transactions - Routes spécifiques AVANT les routes avec paramètres
    path('transactions/export/csv/', views.export_transactions_csv, name='export-transactions-csv'),
    path('transactions/', views.TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<uuid:id>/', views.TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),

    # Categories - Routes spécifiques AVANT les routes avec paramètres
    path('categories/statistics/', views.category_statistics, name='category-statistics'),
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:id>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    # Statistics
    path('statistics/', views.transaction_statistics, name='transaction-statistics'),
]
