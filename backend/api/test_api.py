"""
Tests pour les endpoints API
"""
import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Category, Transaction


@pytest.fixture
def api_client():
    """Fixture pour le client API"""
    return APIClient()


@pytest.fixture
def sample_category():
    """Fixture pour créer une catégorie de test"""
    return Category.objects.create(
        name="Test Category",
        icon="🎯",
        color="#FF0000"
    )


@pytest.fixture
def sample_transaction(sample_category):
    """Fixture pour créer une transaction de test"""
    return Transaction.objects.create(
        text="Test Transaction",
        amount=Decimal("100.00"),
        category=sample_category
    )


@pytest.mark.django_db
class TestCategoryAPI:
    """Tests pour l'API des catégories"""

    def test_list_categories(self, api_client, sample_category):
        """Test de récupération de la liste des catégories"""
        response = api_client.get('/api/categories/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == "Test Category"

    def test_create_category(self, api_client):
        """Test de création d'une catégorie"""
        data = {
            'name': 'New Category',
            'icon': '💰',
            'color': '#00FF00'
        }
        response = api_client.post('/api/categories/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Category'
        assert Category.objects.count() == 1

    def test_retrieve_category(self, api_client, sample_category):
        """Test de récupération d'une catégorie spécifique"""
        response = api_client.get(f'/api/categories/{sample_category.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "Test Category"

    def test_update_category(self, api_client, sample_category):
        """Test de mise à jour d'une catégorie"""
        data = {
            'name': 'Updated Category',
            'icon': '🔥',
            'color': '#0000FF'
        }
        response = api_client.put(
            f'/api/categories/{sample_category.id}/',
            data
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Category'

    def test_delete_category(self, api_client, sample_category):
        """Test de suppression d'une catégorie"""
        response = api_client.delete(f'/api/categories/{sample_category.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Category.objects.count() == 0


@pytest.mark.django_db
class TestTransactionAPI:
    """Tests pour l'API des transactions"""

    def test_list_transactions(self, api_client, sample_transaction):
        """Test de récupération de la liste des transactions"""
        response = api_client.get('/api/transactions/')
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) == 1

    def test_list_transactions_pagination(self, api_client):
        """Test de la pagination"""
        # Créer 15 transactions
        for i in range(15):
            Transaction.objects.create(
                text=f"Transaction {i}",
                amount=Decimal(f"{i}.00")
            )

        response = api_client.get('/api/transactions/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 15
        assert len(response.data['results']) == 10  # Page size par défaut

    def test_create_transaction(self, api_client, sample_category):
        """Test de création d'une transaction"""
        data = {
            'text': 'New Transaction',
            'amount': '250.50',
            'category': str(sample_category.id)
        }
        response = api_client.post('/api/transactions/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == 'New Transaction'
        assert Decimal(response.data['amount']) == Decimal('250.50')

    def test_create_transaction_validation_empty_text(self, api_client):
        """Test de validation : texte vide"""
        data = {
            'text': '',
            'amount': '100.00'
        }
        response = api_client.post('/api/transactions/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_transaction_validation_short_text(self, api_client):
        """Test de validation : texte trop court"""
        data = {
            'text': 'ab',  # Moins de 3 caractères
            'amount': '100.00'
        }
        response = api_client.post('/api/transactions/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_transaction_validation_zero_amount(self, api_client):
        """Test de validation : montant zéro"""
        data = {
            'text': 'Test Transaction',
            'amount': '0.00'
        }
        response = api_client.post('/api/transactions/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_transaction(self, api_client, sample_transaction):
        """Test de mise à jour d'une transaction"""
        data = {
            'text': 'Updated Transaction',
            'amount': '500.00',
            'category': None
        }
        response = api_client.put(
            f'/api/transactions/{sample_transaction.id}/',
            data
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == 'Updated Transaction'

    def test_delete_transaction(self, api_client, sample_transaction):
        """Test de suppression d'une transaction"""
        response = api_client.delete(
            f'/api/transactions/{sample_transaction.id}/'
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Transaction.objects.count() == 0

    def test_filter_by_type_income(self, api_client):
        """Test de filtrage par type (revenus)"""
        Transaction.objects.create(text="Income", amount=Decimal("1000"))
        Transaction.objects.create(text="Expense", amount=Decimal("-500"))

        response = api_client.get('/api/transactions/?type=income')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_filter_by_type_expense(self, api_client):
        """Test de filtrage par type (dépenses)"""
        Transaction.objects.create(text="Income", amount=Decimal("1000"))
        Transaction.objects.create(text="Expense", amount=Decimal("-500"))

        response = api_client.get('/api/transactions/?type=expense')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_filter_by_category(self, api_client, sample_category):
        """Test de filtrage par catégorie"""
        Transaction.objects.create(
            text="With category",
            amount=Decimal("100"),
            category=sample_category
        )
        Transaction.objects.create(
            text="Without category",
            amount=Decimal("200")
        )

        response = api_client.get(
            f'/api/transactions/?category={sample_category.id}'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_search_transactions(self, api_client):
        """Test de recherche de transactions"""
        Transaction.objects.create(text="Salaire mensuel", amount=Decimal("2500"))
        Transaction.objects.create(text="Loyer", amount=Decimal("-850"))

        response = api_client.get('/api/transactions/?search=Salaire')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1


@pytest.mark.django_db
class TestStatisticsAPI:
    """Tests pour l'API des statistiques"""

    def test_transaction_statistics(self, api_client):
        """Test des statistiques globales"""
        Transaction.objects.create(text="Income 1", amount=Decimal("1000"))
        Transaction.objects.create(text="Income 2", amount=Decimal("500"))
        Transaction.objects.create(text="Expense 1", amount=Decimal("-300"))
        Transaction.objects.create(text="Expense 2", amount=Decimal("-200"))

        response = api_client.get('/api/statistics/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_income'] == 1500.0
        assert response.data['total_expense'] == -500.0
        assert response.data['balance'] == 1000.0
        assert response.data['income_count'] == 2
        assert response.data['expense_count'] == 2

    def test_category_statistics(self, api_client, sample_category):
        """Test des statistiques par catégorie"""
        Transaction.objects.create(
            text="Test 1",
            amount=Decimal("100"),
            category=sample_category
        )
        Transaction.objects.create(
            text="Test 2",
            amount=Decimal("200"),
            category=sample_category
        )

        response = api_client.get('/api/categories/statistics/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['count'] == 2
        assert response.data[0]['total'] == 300.0


@pytest.mark.django_db
class TestExportCSV:
    """Tests pour l'export CSV"""

    def test_export_csv(self, api_client, sample_transaction):
        """Test de l'export CSV"""
        response = api_client.get('/api/transactions/export/csv/')
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/csv'
        assert 'attachment' in response['Content-Disposition']

        content = response.content.decode('utf-8')
        assert 'Test Transaction' in content
        assert '100.00' in content
