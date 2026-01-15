"""
Script pour créer facilement des données de démonstration pour le panel administrateur
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from school_core.models import SchoolLevel, Classroom, Student
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Crée un super-utilisateur pour accéder au panel admin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Nom d\'utilisateur du super-utilisateur (défaut: admin)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Mot de passe du super-utilisateur (défaut: admin123)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@caryamil.com',
            help='Email du super-utilisateur'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'L\'utilisateur "{username}" existe déjà.'
                )
            )
            user = User.objects.get(username=username)
            if not user.is_superuser:
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'L\'utilisateur "{username}" a été promu super-utilisateur.'
                    )
                )
        else:
            # Créer le super-utilisateur
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Super-utilisateur "{username}" créé avec succès !'
                )
            )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═' * 60))
        self.stdout.write(self.style.SUCCESS('ACCÈS AU PANEL ADMINISTRATEUR'))
        self.stdout.write(self.style.SUCCESS('═' * 60))
        self.stdout.write(f'URL        : http://localhost:8000/admin/')
        self.stdout.write(f'Username   : {username}')
        self.stdout.write(f'Password   : {password}')
        self.stdout.write(self.style.SUCCESS('═' * 60))
        self.stdout.write('')
        self.stdout.write('Pour démarrer le serveur : python manage.py runserver')
