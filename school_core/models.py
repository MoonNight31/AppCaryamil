from django.db import models
from django.conf import settings
from django.utils import timezone

# 1. Le Niveau Scolaire (Maternelle, Primaire, Collège)
class SchoolLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Niveau scolaire"
        verbose_name_plural = "Niveaux scolaires"
        ordering = ['id']

    def __str__(self):
        return self.name


# 2. La Classe
class Classroom(models.Model):
    level = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE, related_name='classrooms')
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'is_teacher': True},
        related_name='taught_classes'
    )
    school_year = models.CharField(max_length=9, default='2025-2026')
    
    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"
        ordering = ['level', 'name']

    def __str__(self):
        return f"{self.name} ({self.level.name})"


# 3. L'Élève
class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    classroom = models.ForeignKey(
        Classroom, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='students'
    )
    parents = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='children',
        limit_choices_to={'is_parent': True},
        blank=True
    )
    photo = models.ImageField(upload_to='students/%Y/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Élève"
        verbose_name_plural = "Élèves"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# 4. Conversation (Groupe ou Discussion privée)
class Conversation(models.Model):
    CONVERSATION_TYPES = [
        ('group', 'Groupe Classe'),
        ('private', 'Discussion Privée'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom de la conversation")
    conversation_type = models.CharField(
        max_length=10, 
        choices=CONVERSATION_TYPES, 
        default='private',
        verbose_name="Type"
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='conversations',
        verbose_name="Classe (pour groupes)"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        verbose_name="Participants"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_conversations',
        verbose_name="Créé par"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    last_message_at = models.DateTimeField(default=timezone.now, verbose_name="Dernier message")
    
    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-last_message_at']
    
    def __str__(self):
        if self.conversation_type == 'group':
            return f"Groupe: {self.name}"
        return f"Discussion: {self.name}"
    
    def get_last_message(self):
        return self.posts.order_by('-created_at').first()


# 5. Publication (Photos/Messages dans une conversation)
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name="Auteur"
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Conversation",
        null=True,
        blank=True
    )
    # Garde pour compatibilité avec les données existantes
    classroom = models.ForeignKey(
        Classroom, 
        on_delete=models.CASCADE, 
        related_name='old_posts',
        verbose_name="Classe",
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200, blank=True, verbose_name="Titre")
    image = models.ImageField(upload_to='posts/%Y/%m/', blank=True, verbose_name="Photo")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    
    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ['-created_at']

    def __str__(self):
        if self.conversation:
            return f"{self.title or 'Publication'} - {self.conversation} ({self.created_at.strftime('%d/%m/%Y')})"
        return f"{self.title or 'Publication'} ({self.created_at.strftime('%d/%m/%Y')})"


# 6. Message (Communication directe)
class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name="Expéditeur"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name="Destinataire"
    )
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    content = models.TextField(verbose_name="Contenu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - De {self.sender} à {self.recipient}"
