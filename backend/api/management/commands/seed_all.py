from django.core.management.base import BaseCommand
from api.models import Transaction, Category
from decimal import Decimal
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Génère des catégories et 30 transactions de test pour la base de données'

    def handle(self, *args, **kwargs):
        # Supprimer les anciennes données
        Transaction.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING('Anciennes données supprimées'))

        # Créer les catégories
        categories_data = [
            {'name': 'Salaire', 'icon': '💼', 'color': '#10B981'},
            {'name': 'Freelance', 'icon': '💻', 'color': '#3B82F6'},
            {'name': 'Ventes', 'icon': '🛍️', 'color': '#8B5CF6'},
            {'name': 'Investissements', 'icon': '📈', 'color': '#06B6D4'},
            {'name': 'Logement', 'icon': '🏠', 'color': '#EF4444'},
            {'name': 'Alimentation', 'icon': '🍔', 'color': '#F59E0B'},
            {'name': 'Transport', 'icon': '🚗', 'color': '#6366F1'},
            {'name': 'Loisirs', 'icon': '🎮', 'color': '#EC4899'},
            {'name': 'Santé', 'icon': '💊', 'color': '#14B8A6'},
            {'name': 'Shopping', 'icon': '🛒', 'color': '#F97316'},
            {'name': 'Services', 'icon': '📱', 'color': '#8B5CF6'},
            {'name': 'Éducation', 'icon': '📚', 'color': '#0EA5E9'},
        ]

        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[cat_data['name']] = category
            self.stdout.write(f'  Catégorie créée: {category}')

        # Données de test réalistes avec catégories
        revenus = [
            ('Salaire mensuel', Decimal('2500.00'), 'Salaire'),
            ('Freelance - Projet web', Decimal('800.00'), 'Freelance'),
            ('Freelance - Design logo', Decimal('300.00'), 'Freelance'),
            ('Vente en ligne', Decimal('150.00'), 'Ventes'),
            ('Vente voiture', Decimal('3500.00'), 'Ventes'),
            ('Remboursement', Decimal('45.50'), 'Investissements'),
            ('Prime', Decimal('500.00'), 'Salaire'),
            ('Dividendes', Decimal('120.00'), 'Investissements'),
            ('Location appartement', Decimal('650.00'), 'Investissements'),
            ('Cadeau', Decimal('100.00'), 'Ventes'),
        ]

        depenses = [
            ('Loyer', Decimal('-850.00'), 'Logement'),
            ('Électricité', Decimal('-75.30'), 'Logement'),
            ('Internet', Decimal('-39.99'), 'Services'),
            ('Téléphone', Decimal('-25.00'), 'Services'),
            ('Assurance voiture', Decimal('-85.00'), 'Transport'),
            ('Essence', Decimal('-60.00'), 'Transport'),
            ('Courses Carrefour', Decimal('-120.50'), 'Alimentation'),
            ('Courses Lidl', Decimal('-85.20'), 'Alimentation'),
            ('Courses Auchan', Decimal('-95.80'), 'Alimentation'),
            ('Restaurant', Decimal('-45.00'), 'Loisirs'),
            ('Restaurant sushi', Decimal('-55.00'), 'Loisirs'),
            ('Cinéma', Decimal('-22.00'), 'Loisirs'),
            ('Netflix', Decimal('-13.99'), 'Loisirs'),
            ('Spotify', Decimal('-9.99'), 'Loisirs'),
            ('Salle de sport', Decimal('-45.00'), 'Santé'),
            ('Pharmacie', Decimal('-32.50'), 'Santé'),
            ('Dentiste', Decimal('-80.00'), 'Santé'),
            ('Vêtements Zara', Decimal('-120.00'), 'Shopping'),
            ('Cadeau anniversaire', Decimal('-65.00'), 'Shopping'),
            ('Amazon - Gadgets', Decimal('-42.30'), 'Shopping'),
            ('Coiffeur', Decimal('-35.00'), 'Santé'),
            ('Achat livre', Decimal('-18.50'), 'Éducation'),
            ('Réparation voiture', Decimal('-250.00'), 'Transport'),
            ('Café Starbucks', Decimal('-8.50'), 'Alimentation'),
            ('Uber', Decimal('-15.00'), 'Transport'),
        ]

        # Mélanger et sélectionner 30 transactions
        toutes_transactions = []
        toutes_transactions.extend(revenus)
        depenses_selectionnees = random.sample(depenses, 20)
        toutes_transactions.extend(depenses_selectionnees)
        random.shuffle(toutes_transactions)

        # Créer les transactions avec des dates variées (sur les 60 derniers jours)
        transactions_created = []
        base_date = datetime.now()

        for i, (text, amount, category_name) in enumerate(toutes_transactions):
            days_ago = random.randint(0, 60)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)

            created_at = base_date - timedelta(
                days=days_ago,
                hours=hours_ago,
                minutes=minutes_ago
            )

            transaction = Transaction.objects.create(
                text=text,
                amount=amount,
                category=categories.get(category_name),
                created_at=created_at
            )
            transactions_created.append(transaction)

        # Afficher un résumé
        total_revenus = sum(t.amount for t in transactions_created if t.amount > 0)
        total_depenses = sum(t.amount for t in transactions_created if t.amount < 0)
        solde = total_revenus + total_depenses

        self.stdout.write(self.style.SUCCESS(f'\n✓ {len(categories)} catégories créées'))
        self.stdout.write(self.style.SUCCESS(f'✓ {len(transactions_created)} transactions créées'))
        self.stdout.write(self.style.SUCCESS(f'\nRésumé:'))
        self.stdout.write(f'  Revenus totaux: {total_revenus:.2f} €')
        self.stdout.write(f'  Dépenses totales: {total_depenses:.2f} €')
        self.stdout.write(f'  Solde: {solde:.2f} €')
        self.stdout.write(self.style.SUCCESS(f'\n✓ Base de données peuplée avec succès!\n'))
