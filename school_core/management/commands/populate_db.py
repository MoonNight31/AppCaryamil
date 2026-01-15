# school_core/management/commands/populate_db.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import CustomUser
from school_core.models import SchoolLevel, Classroom, Student, Post, Message, Grade
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Remplit la base de données avec des données de test'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Démarrage du remplissage de la base de données...'))
        
        # 1. Créer les niveaux scolaires
        self.stdout.write('📚 Création des niveaux scolaires...')
        maternelle, _ = SchoolLevel.objects.get_or_create(
            slug='maternelle',
            defaults={'name': 'Maternelle', 'description': 'Petite, Moyenne et Grande Section'}
        )
        primaire, _ = SchoolLevel.objects.get_or_create(
            slug='primaire',
            defaults={'name': 'Primaire', 'description': 'Du CP au CM2'}
        )
        college, _ = SchoolLevel.objects.get_or_create(
            slug='college',
            defaults={'name': 'Collège', 'description': 'De la 6ème à la 3ème'}
        )
        self.stdout.write(self.style.SUCCESS('✅ Niveaux créés'))

        # 2. Créer des enseignants
        self.stdout.write('👨‍🏫 Création des enseignants...')
        teachers = []
        teacher_names = [
            ('Marie', 'Dubois'),
            ('Jean', 'Martin'),
            ('Sophie', 'Bernard'),
            ('Pierre', 'Petit'),
            ('Lucie', 'Robert'),
            ('Thomas', 'Richard'),
        ]
        
        for first_name, last_name in teacher_names:
            username = f"{first_name.lower()}.{last_name.lower()}"
            teacher, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f"{username}@ecole.fr",
                    'is_teacher': True,
                }
            )
            if created:
                teacher.set_password('prof123')
                teacher.save()
            teachers.append(teacher)
        self.stdout.write(self.style.SUCCESS(f'✅ {len(teachers)} enseignants créés'))

        # 3. Créer des classes
        self.stdout.write('🏫 Création des classes...')
        classes_data = [
            # Maternelle
            (maternelle, 'Petite Section A', teachers[0]),
            (maternelle, 'Moyenne Section B', teachers[1]),
            (maternelle, 'Grande Section C', teachers[0]),
            # Primaire
            (primaire, 'CP A', teachers[2]),
            (primaire, 'CE1 B', teachers[3]),
            (primaire, 'CE2 A', teachers[2]),
            (primaire, 'CM1 B', teachers[4]),
            (primaire, 'CM2 A', teachers[3]),
            # Collège
            (college, '6ème A', teachers[4]),
            (college, '5ème B', teachers[5]),
            (college, '4ème A', teachers[4]),
            (college, '3ème B', teachers[5]),
        ]
        
        classrooms = []
        for level, name, teacher in classes_data:
            classroom, _ = Classroom.objects.get_or_create(
                level=level,
                name=name,
                defaults={'teacher': teacher, 'school_year': '2025-2026'}
            )
            classrooms.append(classroom)
        self.stdout.write(self.style.SUCCESS(f'✅ {len(classrooms)} classes créées'))

        # 4. Créer des parents
        self.stdout.write('👨‍👩‍👧 Création des parents...')
        parents = []
        parent_names = [
            ('Amélie', 'Dupont'), ('Marc', 'Dupont'),
            ('Julie', 'Moreau'), ('Paul', 'Moreau'),
            ('Claire', 'Laurent'), ('David', 'Laurent'),
            ('Emma', 'Simon'), ('Lucas', 'Simon'),
            ('Sarah', 'Michel'), ('Alexandre', 'Michel'),
            ('Isabelle', 'Leroy'), ('François', 'Leroy'),
            ('Camille', 'Fournier'), ('Nicolas', 'Fournier'),
            ('Élise', 'Girard'), ('Julien', 'Girard'),
        ]
        
        for first_name, last_name in parent_names:
            username = f"{first_name.lower()}.{last_name.lower()}"
            parent, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f"{username}@email.fr",
                    'is_parent': True,
                }
            )
            if created:
                parent.set_password('parent123')
                parent.save()
            parents.append(parent)
        self.stdout.write(self.style.SUCCESS(f'✅ {len(parents)} parents créés'))

        # 5. Créer des élèves et les lier aux parents
        self.stdout.write('👶 Création des élèves...')
        students_data = [
            # Maternelle
            ('Léa', 'Dupont', classrooms[0], [parents[0], parents[1]]),
            ('Hugo', 'Moreau', classrooms[0], [parents[2], parents[3]]),
            ('Chloé', 'Laurent', classrooms[1], [parents[4], parents[5]]),
            ('Louis', 'Simon', classrooms[1], [parents[6], parents[7]]),
            ('Emma', 'Michel', classrooms[2], [parents[8], parents[9]]),
            ('Nathan', 'Leroy', classrooms[2], [parents[10], parents[11]]),
            # Primaire
            ('Alice', 'Fournier', classrooms[3], [parents[12], parents[13]]),
            ('Tom', 'Girard', classrooms[3], [parents[14], parents[15]]),
            ('Jade', 'Dupont', classrooms[4], [parents[0], parents[1]]),
            ('Noah', 'Moreau', classrooms[4], [parents[2], parents[3]]),
            ('Lola', 'Laurent', classrooms[5], [parents[4], parents[5]]),
            ('Arthur', 'Simon', classrooms[5], [parents[6], parents[7]]),
            ('Zoé', 'Michel', classrooms[6], [parents[8], parents[9]]),
            ('Gabriel', 'Leroy', classrooms[6], [parents[10], parents[11]]),
            ('Manon', 'Fournier', classrooms[7], [parents[12], parents[13]]),
            ('Jules', 'Girard', classrooms[7], [parents[14], parents[15]]),
            # Collège
            ('Léonie', 'Dupont', classrooms[8], [parents[0], parents[1]]),
            ('Raphaël', 'Moreau', classrooms[8], [parents[2], parents[3]]),
            ('Juliette', 'Laurent', classrooms[9], [parents[4], parents[5]]),
            ('Maxime', 'Simon', classrooms[9], [parents[6], parents[7]]),
            ('Inès', 'Michel', classrooms[10], [parents[8], parents[9]]),
            ('Antoine', 'Leroy', classrooms[10], [parents[10], parents[11]]),
            ('Clara', 'Fournier', classrooms[11], [parents[12], parents[13]]),
            ('Mathis', 'Girard', classrooms[11], [parents[14], parents[15]]),
        ]
        
        students = []
        for first_name, last_name, classroom, student_parents in students_data:
            # Date de naissance aléatoire selon le niveau
            if classroom.level == maternelle:
                birth_year = 2022
            elif classroom.level == primaire:
                birth_year = random.randint(2016, 2020)
            elif classroom.level == college:
                birth_year = random.randint(2011, 2015)
            else:
                birth_year = random.randint(2011, 2015)
            
            birth_date = date(birth_year, random.randint(1, 12), random.randint(1, 28))
            
            student, created = Student.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                classroom=classroom,
                defaults={'date_of_birth': birth_date}
            )
            if created:
                student.parents.set(student_parents)
            students.append(student)
        self.stdout.write(self.style.SUCCESS(f'✅ {len(students)} élèves créés'))

        # 6. Créer des publications/photos
        self.stdout.write('📸 Création des publications...')
        posts_data = [
            (classrooms[0], teachers[0], "Activité Peinture", "Les enfants ont créé de magnifiques tableaux aujourd'hui ! 🎨"),
            (classrooms[0], teachers[0], "Sortie au parc", "Belle journée au parc avec la classe ! ☀️"),
            (classrooms[1], teachers[1], "Atelier musique", "Découverte des instruments de musique 🎵"),
            (classrooms[2], teachers[0], "Spectacle de fin d'année", "Répétitions pour le spectacle 🎭"),
            (classrooms[3], teachers[2], "Exercices de lecture", "Progrès remarquables en lecture ! 📖"),
            (classrooms[4], teachers[3], "Sciences naturelles", "Observation des papillons 🦋"),
            (classrooms[5], teachers[2], "Projet d'écriture", "Les élèves écrivent leurs propres histoires ✍️"),
        ]
        
        posts = []
        for classroom, author, title, description in posts_data:
            post, created = Post.objects.get_or_create(
                classroom=classroom,
                author=author,
                title=title,
                defaults={
                    'description': description,
                    'is_published': True,
                }
            )
            posts.append(post)
        self.stdout.write(self.style.SUCCESS(f'✅ {len(posts)} publications créées'))

        # 7. Créer des notes pour le collège
        self.stdout.write('📝 Création des notes...')
        subjects = ['Mathématiques', 'Français', 'Histoire-Géo', 'Anglais', 'Sciences', 'EPS']
        grades_created = 0
        
        # Notes pour le collège
        for student in students:
            if student.classroom.level == college:
                for subject in subjects:
                    for i in range(random.randint(3, 6)):
                        grade_value = round(random.uniform(8, 19), 2)
                        grade_date = date.today() - timedelta(days=random.randint(1, 90))
                        
                        Grade.objects.get_or_create(
                            student=student,
                            subject=subject,
                            date=grade_date,
                            defaults={
                                'grade': grade_value,
                                'max_grade': 20,
                                'teacher': student.classroom.teacher,
                                'comment': random.choice([
                                    'Très bien',
                                    'Bon travail',
                                    'Peut mieux faire',
                                    'Excellent',
                                    'À approfondir',
                                ])
                            }
                        )
                        grades_created += 1
        self.stdout.write(self.style.SUCCESS(f'✅ {grades_created} notes créées'))

        # 8. Créer des messages
        self.stdout.write('💬 Création des messages...')
        messages_data = [
            (teachers[0], parents[0], "Réunion parents-profs", "Bonjour, la réunion parents-professeurs aura lieu le 15 janvier."),
            (parents[2], teachers[3], "Absence de Hugo", "Bonjour, Hugo sera absent demain pour raison médicale."),
            (teachers[5], parents[8], "Excellent travail", "Félicitations, votre enfant fait d'excellents progrès !"),
            (parents[10], teachers[4], "Question sur les devoirs", "Bonjour, pourriez-vous préciser les devoirs de mathématiques ?"),
        ]
        
        for sender, recipient, subject, content in messages_data:
            Message.objects.get_or_create(
                sender=sender,
                recipient=recipient,
                subject=subject,
                defaults={'content': content, 'is_read': random.choice([True, False])}
            )
        self.stdout.write(self.style.SUCCESS(f'✅ {len(messages_data)} messages créés'))

        # Résumé
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ Base de données remplie avec succès !'))
        self.stdout.write('='*60)
        self.stdout.write(f'📚 Niveaux: {SchoolLevel.objects.count()}')
        self.stdout.write(f'🏫 Classes: {Classroom.objects.count()}')
        self.stdout.write(f'👨‍🏫 Enseignants: {CustomUser.objects.filter(is_teacher=True).count()}')
        self.stdout.write(f'👨‍👩‍👧 Parents: {CustomUser.objects.filter(is_parent=True).count()}')
        self.stdout.write(f'👶 Élèves: {Student.objects.count()}')
        self.stdout.write(f'📸 Publications: {Post.objects.count()}')
        self.stdout.write(f'📝 Notes: {Grade.objects.count()}')
        self.stdout.write(f'💬 Messages: {Message.objects.count()}')
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('🔐 Identifiants de connexion:'))
        self.stdout.write('='*60)
        self.stdout.write('👨‍🏫 Enseignant:')
        self.stdout.write('   Username: marie.dubois')
        self.stdout.write('   Password: prof123')
        self.stdout.write('')
        self.stdout.write('👨‍👩‍👧 Parent:')
        self.stdout.write('   Username: amelie.dupont')
        self.stdout.write('   Password: parent123')
        self.stdout.write('')
        self.stdout.write('👑 Admin:')
        self.stdout.write('   Username: admin')
        self.stdout.write('   Password: (votre mot de passe)')
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('\n🎉 Vous pouvez maintenant utiliser l\'application !'))
        self.stdout.write('🌐 Allez sur: http://127.0.0.1:8000/niveaux/')
