from rest_framework import serializers
from .models import Transaction, Category


class CategorySerializer(serializers.ModelSerializer):
    transactions_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "icon", "color", "created_at", "transactions_count"]
        read_only_fields = ["id", "created_at", "transactions_count"]

    def get_transactions_count(self, obj):
        return obj.transactions.count()

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Le nom ne peut pas être vide")
        return value.strip()


class TransactionSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "text", "amount", "category", "category_details", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_text(self, value):
        """Valide que le texte n'est pas vide"""
        if not value or not value.strip():
            raise serializers.ValidationError("Le texte ne peut pas être vide")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Le texte doit contenir au moins 3 caractères")
        return value.strip()

    def validate_amount(self, value):
        """Valide que le montant est un nombre valide"""
        if value == 0:
            raise serializers.ValidationError("Le montant ne peut pas être zéro")
        return value
