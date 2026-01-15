"""
Script pour configurer les permissions des directeurs
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from school_core.models import SchoolLevel, Classroom, Student, Conversation, Post, Message
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Configure les permissions pour les directeurs et met à jour les utilisateurs existants'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('CONFIGURATION DES PERMISSIONS DIRECTEURS'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        
        # Créer ou récupérer le groupe Directeurs
        directors_group, created = Group.objects.get_or_create(name='Directeurs')
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Groupe "Directeurs" créé'))
        else:
            self.stdout.write(self.style.WARNING('○ Groupe "Directeurs" existe déjà'))
        
        # Liste des modèles et permissions à attribuer
        models_permissions = [
            (User, ['view', 'add', 'change']),  # Peut gérer les utilisateurs (sauf delete)
            (SchoolLevel, ['view', 'add', 'change', 'delete']),
            (Classroom, ['view', 'add', 'change', 'delete']),
            (Student, ['view', 'add', 'change', 'delete']),
            (Conversation, ['view', 'add', 'change', 'delete']),
            (Post, ['view', 'add', 'change', 'delete']),
            (Message, ['view', 'change']),  # Peut voir et marquer comme lu
        ]
        
        permissions_added = 0
        for model, perms in models_permissions:
            content_type = ContentType.objects.get_for_model(model)
            for perm in perms:
                codename = f'{perm}_{model._meta.model_name}'
                try:
                    permission = Permission.objects.get(
                        codename=codename,
                        content_type=content_type
                    )
                    directors_group.permissions.add(permission)
                    permissions_added += 1
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Permission {codename} non trouvée')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'✓ {permissions_added} permissions ajoutées au groupe Directeurs')
        )
        self.stdout.write('')
        
        # Mettre à jour tous les directeurs existants
        directors = User.objects.filter(is_director=True)
        updated_count = 0
        
        for director in directors:
            changes = []
            if not director.is_staff:
                director.is_staff = True
                changes.append('is_staff=True')
            if not director.is_teacher:
                director.is_teacher = True
                changes.append('is_teacher=True')
            
            if changes:
                director.save()
                updated_count += 1
                self.stdout.write(
                    f'  • {director.username} : {", ".join(changes)}'
                )
            
            # Ajouter au groupe
            director.groups.add(directors_group)
        
        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'✓ {updated_count} directeur(s) mis à jour')
            )
        else:
            self.stdout.write(
                self.style.WARNING('○ Aucun directeur existant à mettre à jour')
            )
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('RÉSUMÉ DES PERMISSIONS DIRECTEURS'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write('Les directeurs peuvent maintenant :')
        self.stdout.write('  ✓ Accéder au panel administrateur')
        self.stdout.write('  ✓ Gérer les niveaux scolaires')
        self.stdout.write('  ✓ Gérer les classes')
        self.stdout.write('  ✓ Gérer les élèves')
        self.stdout.write('  ✓ Gérer les conversations')
        self.stdout.write('  ✓ Gérer les publications')
        self.stdout.write('  ✓ Voir et gérer les messages')
        self.stdout.write('  ✓ Voir et modifier les utilisateurs (professeurs/parents)')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('⚠ Les directeurs ne peuvent PAS :'))
        self.stdout.write('  ✗ Supprimer des utilisateurs')
        self.stdout.write('  ✗ Créer des super-utilisateurs')
        self.stdout.write('  ✗ Modifier les permissions')
        self.stdout.write('')
