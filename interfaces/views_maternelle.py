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
    # Les directeurs voient toutes les conversations du niveau
    if request.user.is_director:
        conversations = Conversation.objects.filter(
            Q(classroom__level=level) | Q(classroom__isnull=True, participants__children__classroom__level=level)
        ).distinct().order_by('-last_message_at')[:50]
    else:
        conversations = Conversation.objects.filter(
            Q(participants=request.user) | Q(created_by=request.user)
        ).filter(
            Q(classroom__level=level) | Q(classroom__isnull=True, participants__children__classroom__level=level)
        ).distinct().order_by('-last_message_at')[:50]
    
    # Conversation sélectionnée
    conversation_id = request.GET.get('conv')
    if conversation_id:
        if request.user.is_director:
            selected_conversation = get_object_or_404(Conversation, id=conversation_id)
        else:
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
    if request.user.is_director:
        # Directeurs: toutes les classes du niveau
        classrooms = Classroom.objects.filter(level=level)
    elif request.user.is_teacher:
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
        'can_create_conversation': request.user.is_teacher or request.user.is_director,
    }
    return render(request, 'maternelle/messenger.html', context)


@login_required
def create_conversation(request):
    """Créer une nouvelle conversation privée (enseignants et directeurs uniquement)"""
    if not (request.user.is_teacher or request.user.is_director):
        django_messages.error(request, "Seuls les enseignants et directeurs peuvent créer des conversations")
        return redirect('/niveaux/maternelle/')
    
    level = get_object_or_404(SchoolLevel, slug='maternelle')
    
    if request.method == 'POST':
        student_ids = request.POST.getlist('students')
        conversation_name = request.POST.get('name')
        
        if not student_ids:
            django_messages.error(request, "Veuillez sélectionner au moins un élève")
            return redirect('/niveaux/maternelle/create-conversation/')
        
        # Créer la conversation sans classe spécifique (multi-classes)
        conversation = Conversation.objects.create(
            name=conversation_name or f"Discussion Maternelle",
            conversation_type='private',
            classroom=None,  # Pas de classe spécifique pour conversations multi-classes
            created_by=request.user
        )
        
        # Ajouter l'enseignant comme participant
        conversation.participants.add(request.user)
        
        # Ajouter les parents des élèves sélectionnés
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            for parent in student.parents.all():
                conversation.participants.add(parent)
        
        django_messages.success(request, f"💬 Conversation créée avec {len(student_ids)} élève(s) !")
        return redirect(f'/niveaux/maternelle/?conv={conversation.id}')
    
    # GET: afficher le formulaire avec tous les élèves du niveau
    if request.user.is_director:
        classrooms = Classroom.objects.filter(level=level)
    else:
        classrooms = request.user.taught_classes.filter(level=level)
    
    # Récupérer tous les élèves des classes du niveau
    students = Student.objects.filter(classroom__in=classrooms).select_related('classroom').order_by('classroom__name', 'last_name', 'first_name')
    
    context = {
        'level': level,
        'classrooms': classrooms,
        'students': students,
    }
    return render(request, 'maternelle/create_conversation.html', context)


@login_required
def add_participants(request, conversation_id):
    """Ajouter des participants à une conversation existante"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Vérifier que l'utilisateur peut modifier cette conversation
    if not (request.user.is_director or conversation.created_by == request.user or request.user in conversation.participants.all()):
        django_messages.error(request, "Vous n'avez pas la permission de modifier cette conversation")
        return redirect(f'/niveaux/maternelle/?conv={conversation.id}')
    
    level = get_object_or_404(SchoolLevel, slug='maternelle')
    
    if request.method == 'POST':
        student_ids = request.POST.getlist('students')
        
        if not student_ids:
            django_messages.error(request, "Veuillez sélectionner au moins un élève")
            return redirect(f'/niveaux/maternelle/conversation/{conversation_id}/add-participants/')
        
        # Ajouter les parents des élèves sélectionnés
        added_count = 0
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            for parent in student.parents.all():
                if parent not in conversation.participants.all():
                    conversation.participants.add(parent)
                    added_count += 1
        
        if added_count > 0:
            django_messages.success(request, f"✅ {added_count} participant(s) ajouté(s) à la conversation")
        else:
            django_messages.info(request, "Tous ces participants sont déjà dans la conversation")
        
        return redirect(f'/niveaux/maternelle/?conv={conversation.id}')
    
    # GET: afficher le formulaire
    if request.user.is_director:
        classrooms = Classroom.objects.filter(level=level)
    else:
        classrooms = request.user.taught_classes.filter(level=level)
    
    # Récupérer tous les élèves du niveau dont les parents ne sont pas encore dans la conversation
    current_participants = conversation.participants.all()
    students = Student.objects.filter(classroom__in=classrooms).select_related('classroom').order_by('classroom__name', 'last_name', 'first_name')
    
    context = {
        'level': level,
        'conversation': conversation,
        'classrooms': classrooms,
        'students': students,
        'current_participants': current_participants,
    }
    return render(request, 'maternelle/add_participants.html', context)


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
