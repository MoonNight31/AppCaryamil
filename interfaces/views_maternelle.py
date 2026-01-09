# interfaces/views_maternelle.py
# Vue spécifique pour la MATERNELLE (Interface Messenger avec conversations)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from school_core.models import SchoolLevel, Classroom, Post, Student, Conversation
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone


@login_required
def maternelle_dashboard(request):
    """Interface Messenger - Conversations de groupe et privées"""
    level = get_object_or_404(SchoolLevel, slug='maternelle')
    
    # Récupérer toutes les conversations de l'utilisateur
    conversations = Conversation.objects.filter(
        Q(participants=request.user) | Q(created_by=request.user)
    ).filter(
        Q(classroom__level=level) | Q(classroom__isnull=True, participants__children__classroom__level=level)
    ).distinct().order_by('-last_message_at')[:50]
    
    # Conversation sélectionnée
    conversation_id = request.GET.get('conv')
    if conversation_id:
        selected_conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    else:
        selected_conversation = conversations.first() if conversations.exists() else None
    
    # Posts de la conversation sélectionnée
    posts = []
    if selected_conversation:
        posts = Post.objects.filter(
            conversation=selected_conversation,
            is_published=True
        ).select_related('author').order_by('-created_at')[:100]
    
    # Envoi de message/photo (POST)
    if request.method == 'POST' and selected_conversation:
        description = request.POST.get('description', '').strip()
        if 'image' in request.FILES or description:
            post = Post.objects.create(
                author=request.user,
                conversation=selected_conversation,
                image=request.FILES.get('image'),
                description=description,
                title=request.POST.get('title', '')
            )
            # Mettre à jour last_message_at
            selected_conversation.last_message_at = timezone.now()
            selected_conversation.save()
            django_messages.success(request, '✉️ Message envoyé avec succès !')
            return redirect(f'/niveaux/maternelle/?conv={selected_conversation.id}')
    
    # Classes disponibles (pour créer des conversations)
    if request.user.is_teacher:
        classrooms = request.user.taught_classes.filter(level=level)
    elif request.user.is_parent:
        children = request.user.children.filter(classroom__level=level)
        classrooms = Classroom.objects.filter(level=level, students__in=children).distinct()
    else:
        classrooms = Classroom.objects.filter(level=level)
    
    context = {
        'level': level,
        'conversations': conversations,
        'selected_conversation': selected_conversation,
        'posts': posts,
        'can_post': True,  # Tout le monde peut poster
        'classrooms': classrooms,
        'can_create_conversation': request.user.is_teacher,
    }
    return render(request, 'maternelle/messenger.html', context)


@login_required
def create_conversation(request):
    """Créer une nouvelle conversation privée (enseignants uniquement)"""
    if not request.user.is_teacher:
        django_messages.error(request, "Seuls les enseignants peuvent créer des conversations")
        return redirect('/niveaux/maternelle/')
    
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom')
        student_ids = request.POST.getlist('students')  # Changé de 'parents' à 'students'
        conversation_name = request.POST.get('name')
        
        if not (classroom_id and student_ids):
            django_messages.error(request, "Veuillez sélectionner une classe et au moins un élève")
            return redirect('/niveaux/maternelle/')
        
        classroom = get_object_or_404(Classroom, id=classroom_id)
        
        # Créer la conversation
        conversation = Conversation.objects.create(
            name=conversation_name or f"Discussion {classroom.name}",
            conversation_type='private',
            classroom=classroom,
            created_by=request.user
        )
        
        # Ajouter l'enseignant comme participant
        conversation.participants.add(request.user)
        
        # Ajouter les parents des élèves sélectionnés
        from school_core.models import Student
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            for parent in student.parents.all():
                conversation.participants.add(parent)
        
        django_messages.success(request, f"💬 Conversation créée avec succès !")
        return redirect(f'/niveaux/maternelle/?conv={conversation.id}')
    
    # GET: afficher le formulaire
    classrooms = request.user.taught_classes.filter(level__slug='maternelle')
    context = {
        'classrooms': classrooms,
    }
    return render(request, 'maternelle/create_conversation.html', context)


@login_required
def maternelle_photos(request, classroom_id):
    """Redirige vers le messenger avec la classe sélectionnée"""
    return redirect(f'/niveaux/maternelle/')


@login_required
def maternelle_eleves(request, classroom_id):
    """Liste des élèves d'une classe maternelle"""
    classroom = get_object_or_404(Classroom, id=classroom_id, level__slug='maternelle')
    students = classroom.students.all().prefetch_related('parents')
    
    context = {
        'classroom': classroom,
        'students': students,
    }
    return render(request, 'maternelle/eleves.html', context)
