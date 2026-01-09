# school_core/management/commands/create_group_conversations.py
from django.core.management.base import BaseCommand
from school_core.models import Classroom, Conversation, Post
from django.utils import timezone


class Command(BaseCommand):
    help = 'Crée automatiquement des conversations de groupe pour chaque classe'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Création des conversations de groupe...'))
        
        classrooms = Classroom.objects.all()
        created_count = 0
        
        for classroom in classrooms:
            # Vérifier si une conversation de groupe existe déjà
            existing = Conversation.objects.filter(
                conversation_type='group',
                classroom=classroom
            ).first()
            
            if not existing:
                # Créer la conversation de groupe
                conversation = Conversation.objects.create(
                    name=f"Groupe {classroom.name}",
                    conversation_type='group',
                    classroom=classroom,
                    created_by=classroom.teacher if classroom.teacher else None
                )
                
                # Ajouter tous les parents des élèves de la classe
                for student in classroom.students.all():
                    for parent in student.parents.all():
                        conversation.participants.add(parent)
                
                # Ajouter l'enseignant
                if classroom.teacher:
                    conversation.participants.add(classroom.teacher)
                
                # Migrer les anciennes publications vers cette conversation
                old_posts = Post.objects.filter(classroom=classroom, conversation__isnull=True)
                migrated = 0
                for post in old_posts:
                    post.conversation = conversation
                    post.save()
                    migrated += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Conversation créée pour {classroom.name} ({conversation.participants.count()} participants, {migrated} photos migrées)'
                    )
                )
                created_count += 1
            else:
                self.stdout.write(f'⏭️  Conversation déjà existante pour {classroom.name}')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✅ {created_count} nouvelles conversations créées'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total conversations: {Conversation.objects.count()}'))
        self.stdout.write('='*60)
