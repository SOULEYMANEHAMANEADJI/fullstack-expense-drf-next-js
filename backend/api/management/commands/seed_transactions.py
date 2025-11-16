from django.core.management.base import BaseCommand
from api.models import Transaction
from decimal import Decimal
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Génère 30 transactions de test pour la base de données'

    def handle(self, *args, **kwargs):
        # Supprimer les anciennes transactions si elles existent
        Transaction.objects.all().delete()
        self.stdout.write(self.style.WARNING('Anciennes transactions supprimées'))

        # Données de test réalistes
        revenus = [
            ('Salaire mensuel', Decimal('2500.00')),
            ('Freelance - Projet web', Decimal('800.00')),
            ('Vente en ligne', Decimal('150.00')),
            ('Remboursement', Decimal('45.50')),
            ('Prime', Decimal('500.00')),
            ('Dividendes', Decimal('120.00')),
            ('Location appartement', Decimal('650.00')),
            ('Freelance - Design logo', Decimal('300.00')),
            ('Vente voiture', Decimal('3500.00')),
            ('Cadeau', Decimal('100.00')),
        ]

        depenses = [
            ('Loyer', Decimal('-850.00')),
            ('Courses Carrefour', Decimal('-120.50')),
            ('Électricité', Decimal('-75.30')),
            ('Internet', Decimal('-39.99')),
            ('Restaurant', Decimal('-45.00')),
            ('Essence', Decimal('-60.00')),
            ('Assurance voiture', Decimal('-85.00')),
            ('Téléphone', Decimal('-25.00')),
            ('Netflix', Decimal('-13.99')),
            ('Spotify', Decimal('-9.99')),
            ('Courses Lidl', Decimal('-85.20')),
            ('Pharmacie', Decimal('-32.50')),
            ('Vêtements Zara', Decimal('-120.00')),
            ('Restaurant sushi', Decimal('-55.00')),
            ('Cinéma', Decimal('-22.00')),
            ('Coiffeur', Decimal('-35.00')),
            ('Salle de sport', Decimal('-45.00')),
            ('Achat livre', Decimal('-18.50')),
            ('Courses Auchan', Decimal('-95.80')),
            ('Cadeau anniversaire', Decimal('-65.00')),
            ('Réparation voiture', Decimal('-250.00')),
            ('Dentiste', Decimal('-80.00')),
            ('Amazon - Gadgets', Decimal('-42.30')),
            ('Café Starbucks', Decimal('-8.50')),
            ('Uber', Decimal('-15.00')),
        ]

        # Mélanger et sélectionner 30 transactions
        toutes_transactions = []

        # Ajouter tous les revenus (10)
        toutes_transactions.extend(revenus)

        # Sélectionner 20 dépenses aléatoires
        depenses_selectionnees = random.sample(depenses, 20)
        toutes_transactions.extend(depenses_selectionnees)

        # Mélanger pour un ordre aléatoire
        random.shuffle(toutes_transactions)

        # Créer les transactions avec des dates variées (sur les 60 derniers jours)
        transactions_created = []
        base_date = datetime.now()

        for i, (text, amount) in enumerate(toutes_transactions):
            # Générer une date aléatoire dans les 60 derniers jours
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
                created_at=created_at
            )
            transactions_created.append(transaction)

        # Afficher un résumé
        total_revenus = sum(t.amount for t in transactions_created if t.amount > 0)
        total_depenses = sum(t.amount for t in transactions_created if t.amount < 0)
        solde = total_revenus + total_depenses

        self.stdout.write(self.style.SUCCESS(f'\n✓ {len(transactions_created)} transactions créées avec succès!'))
        self.stdout.write(self.style.SUCCESS(f'\nRésumé:'))
        self.stdout.write(f'  Revenus totaux: {total_revenus:.2f} €')
        self.stdout.write(f'  Dépenses totales: {total_depenses:.2f} €')
        self.stdout.write(f'  Solde: {solde:.2f} €')
        self.stdout.write(self.style.SUCCESS(f'\n✓ Base de données peuplée avec succès!\n'))
