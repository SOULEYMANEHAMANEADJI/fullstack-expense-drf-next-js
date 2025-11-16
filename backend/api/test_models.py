"""
Tests pour les modèles Django
"""
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from api.models import Category, Transaction


@pytest.mark.django_db
class TestCategoryModel:
    """Tests pour le modèle Category"""

    def test_create_category(self):
        """Test de création d'une catégorie"""
        category = Category.objects.create(
            name="Test Category",
            icon="🎯",
            color="#FF0000"
        )
        assert category.name == "Test Category"
        assert category.icon == "🎯"
        assert category.color == "#FF0000"
        assert str(category) == "🎯 Test Category"

    def test_category_unique_name(self):
        """Test que le nom de catégorie doit être unique"""
        Category.objects.create(name="Duplicate", icon="🔥", color="#00FF00")

        with pytest.raises(Exception):  # IntegrityError
            Category.objects.create(name="Duplicate", icon="💰", color="#0000FF")

    def test_category_default_values(self):
        """Test des valeurs par défaut"""
        category = Category.objects.create(name="Default Test")
        assert category.icon == "📁"
        assert category.color == "#FFB800"

    def test_category_ordering(self):
        """Test du tri par nom"""
        Category.objects.create(name="Zebra", icon="🦓", color="#000000")
        Category.objects.create(name="Apple", icon="🍎", color="#FF0000")

        categories = list(Category.objects.all())
        assert categories[0].name == "Apple"
        assert categories[1].name == "Zebra"


@pytest.mark.django_db
class TestTransactionModel:
    """Tests pour le modèle Transaction"""

    def test_create_transaction_positive(self):
        """Test de création d'une transaction positive (revenu)"""
        transaction = Transaction.objects.create(
            text="Salaire",
            amount=Decimal("2500.00")
        )
        assert transaction.text == "Salaire"
        assert transaction.amount == Decimal("2500.00")
        assert transaction.category is None
        assert str(transaction) == "Salaire (2500.00)"

    def test_create_transaction_negative(self):
        """Test de création d'une transaction négative (dépense)"""
        transaction = Transaction.objects.create(
            text="Loyer",
            amount=Decimal("-850.50")
        )
        assert transaction.text == "Loyer"
        assert transaction.amount == Decimal("-850.50")

    def test_transaction_with_category(self):
        """Test de transaction avec catégorie"""
        category = Category.objects.create(
            name="Logement",
            icon="🏠",
            color="#3B82F6"
        )
        transaction = Transaction.objects.create(
            text="Loyer",
            amount=Decimal("-850.00"),
            category=category
        )
        assert transaction.category == category
        assert transaction.category.name == "Logement"

    def test_transaction_category_on_delete_set_null(self):
        """Test que la transaction reste quand la catégorie est supprimée"""
        category = Category.objects.create(name="Test", icon="🔥", color="#FF0000")
        transaction = Transaction.objects.create(
            text="Test",
            amount=Decimal("100.00"),
            category=category
        )

        category.delete()
        transaction.refresh_from_db()
        assert transaction.category is None

    def test_transaction_ordering(self):
        """Test du tri par date décroissante"""
        t1 = Transaction.objects.create(text="Old", amount=Decimal("100"))
        t2 = Transaction.objects.create(text="New", amount=Decimal("200"))

        transactions = list(Transaction.objects.all())
        assert transactions[0] == t2  # Plus récent en premier
        assert transactions[1] == t1

    def test_category_transactions_count(self):
        """Test du comptage des transactions par catégorie"""
        category = Category.objects.create(name="Food", icon="🍔", color="#10B981")

        Transaction.objects.create(text="Restaurant", amount=Decimal("-50"), category=category)
        Transaction.objects.create(text="Groceries", amount=Decimal("-100"), category=category)

        assert category.transactions.count() == 2
