from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from decimal import Decimal
import csv
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer


class TransactionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Transaction.objects.all()

        # Filtre par type (revenu/dépense)
        transaction_type = self.request.query_params.get('type', None)
        if transaction_type == 'income':
            queryset = queryset.filter(amount__gt=0)
        elif transaction_type == 'expense':
            queryset = queryset.filter(amount__lt=0)

        # Filtre par catégorie
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        # Filtre par montant minimum
        min_amount = self.request.query_params.get('min_amount', None)
        if min_amount:
            queryset = queryset.filter(amount__gte=Decimal(min_amount))

        # Filtre par montant maximum
        max_amount = self.request.query_params.get('max_amount', None)
        if max_amount:
            queryset = queryset.filter(amount__lte=Decimal(max_amount))

        # Filtre par date de début
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)

        # Filtre par date de fin
        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset


class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = "id"


@api_view(['GET'])
def transaction_statistics(request):
    """
    Endpoint pour obtenir des statistiques sur les transactions
    """
    # Calculs de base
    all_transactions = Transaction.objects.all()

    total_income = all_transactions.filter(amount__gt=0).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    total_expense = all_transactions.filter(amount__lt=0).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    balance = total_income + total_expense

    # Compteurs
    income_count = all_transactions.filter(amount__gt=0).count()
    expense_count = all_transactions.filter(amount__lt=0).count()
    total_count = all_transactions.count()

    # Moyennes
    avg_income = all_transactions.filter(amount__gt=0).aggregate(
        avg=Sum('amount')
    )['avg'] or Decimal('0')
    if income_count > 0:
        avg_income = avg_income / income_count

    avg_expense = all_transactions.filter(amount__lt=0).aggregate(
        avg=Sum('amount')
    )['avg'] or Decimal('0')
    if expense_count > 0:
        avg_expense = avg_expense / expense_count

    # Plus grandes transactions
    largest_income = all_transactions.filter(amount__gt=0).order_by('-amount').first()
    largest_expense = all_transactions.filter(amount__lt=0).order_by('amount').first()

    # Ratio
    ratio = 0
    if total_income > 0:
        ratio = min((abs(total_expense) / total_income) * 100, 100)

    return Response({
        'balance': float(balance),
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'income_count': income_count,
        'expense_count': expense_count,
        'total_count': total_count,
        'avg_income': float(avg_income),
        'avg_expense': float(avg_expense),
        'ratio': float(ratio),
        'largest_income': TransactionSerializer(largest_income).data if largest_income else None,
        'largest_expense': TransactionSerializer(largest_expense).data if largest_expense else None,
    })


# ============ CATEGORY VIEWS ============

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"


@api_view(['GET'])
def category_statistics(request):
    """
    Statistiques par catégorie
    """
    categories = Category.objects.all()
    stats = []

    for category in categories:
        transactions = category.transactions.all()
        total = transactions.aggregate(total=Sum('amount'))['total'] or Decimal('0')
        count = transactions.count()

        stats.append({
            'category': CategorySerializer(category).data,
            'total': float(total),
            'count': count,
        })

    # Trier par total décroissant (en valeur absolue)
    stats.sort(key=lambda x: abs(x['total']), reverse=True)

    return Response(stats)


# ============ EXPORT CSV ============

@api_view(['GET'])
def export_transactions_csv(request):
    """
    Exporter toutes les transactions en CSV
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Texte', 'Montant', 'Catégorie', 'Date de création'])

    transactions = Transaction.objects.all().order_by('-created_at')
    for t in transactions:
        writer.writerow([
            str(t.id),
            t.text,
            str(t.amount),
            t.category.name if t.category else 'Sans catégorie',
            t.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response
