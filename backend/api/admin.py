from django.contrib import admin
from .models import Transaction, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'color', 'created_at', 'get_transactions_count']
    search_fields = ['name']
    list_filter = ['created_at']

    def get_transactions_count(self, obj):
        return obj.transactions.count()
    get_transactions_count.short_description = 'Transactions'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['text', 'amount', 'category', 'created_at']
    search_fields = ['text']
    list_filter = ['category', 'created_at']
    date_hierarchy = 'created_at'
