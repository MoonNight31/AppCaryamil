# interfaces/views_primaire.py
# Vue spécifique pour le PRIMAIRE (Interface Messenger avec conversations)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from school_core.models import SchoolLevel, Classroom, Post, Student, Conversation
from django.db.models import Q
from django.utils import timezone


@login_required
def primaire_dashboard(request):
    """Interface Messenger - Conversations de groupe et privées"""
    level = get_object_or_404(SchoolLevel, slug='primaire')
    
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
    
    conversation_id = request.GET.get('conv')
    if conversation_id:
        if request.user.is_director:
            selected_conversation = get_object_or_404(Conversation, id=conversation_id)
        else:
            selected_conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    else:
        selected_conversation = conversations.first() if conversations.exists() else None
    
    posts = []
    if selected_conversation:
        posts = Post.objects.filter(
            conversation=selected_conversation,
            is_published=True
        ).select_related('author').order_by('-created_at')[:100]
    
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
            selected_conversation.last_message_at = timezone.now()
            selected_conversation.save()
            django_messages.success(request, '✉️ Message envoyé avec succès !')
            return redirect(f'/niveaux/primaire/?conv={selected_conversation.id}')
    
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
        'can_post': True,
        'classrooms': classrooms,
        'can_create_conversation': request.user.is_teacher or request.user.is_director,
    }
    return render(request, 'primaire/messenger.html', context)


@login_required
def create_conversation(request):
    """Créer une nouvelle conversation privée (enseignants et directeurs uniquement)"""
    if not (request.user.is_teacher or request.user.is_director):
        django_messages.error(request, "Seuls les enseignants et directeurs peuvent créer des conversations")
        return redirect('/niveaux/primaire/')
    
    level = get_object_or_404(SchoolLevel, slug='primaire')
    
    if request.method == 'POST':
        student_ids = request.POST.getlist('students')
        conversation_name = request.POST.get('name')
        
        if not student_ids:
            django_messages.error(request, "Veuillez sélectionner au moins un élève")
            return redirect('/niveaux/primaire/create-conversation/')
        
        # Créer la conversation sans classe spécifique (multi-classes)
        conversation = Conversation.objects.create(
            name=conversation_name or f"Discussion Primaire",
            conversation_type='private',
            classroom=None,
            created_by=request.user
        )
        
        # Ajouter l'enseignant
        conversation.participants.add(request.user)
        
        # Ajouter les parents des élèves sélectionnés
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            for parent in student.parents.all():
                conversation.participants.add(parent)
        
        django_messages.success(request, f"💬 Conversation créée avec {len(student_ids)} élève(s) !")
        return redirect(f'/niveaux/primaire/?conv={conversation.id}')
    
    # GET: afficher le formulaire avec tous les élèves du niveau
    if request.user.is_director:
        classrooms = Classroom.objects.filter(level=level)
    else:
        classrooms = request.user.taught_classes.filter(level=level)
    
    students = Student.objects.filter(classroom__in=classrooms).select_related('classroom').order_by('classroom__name', 'last_name', 'first_name')
    
    context = {
        'level': level,
        'classrooms': classrooms,
        'students': students,
    }
    return render(request, 'primaire/create_conversation.html', context)


@login_required
def add_participants(request, conversation_id):
    """Ajouter des participants à une conversation existante"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    if not (request.user.is_director or conversation.created_by == request.user or request.user in conversation.participants.all()):
        django_messages.error(request, "Vous n'avez pas la permission de modifier cette conversation")
        return redirect(f'/niveaux/primaire/?conv={conversation.id}')
    
    level = get_object_or_404(SchoolLevel, slug='primaire')
    
    if request.method == 'POST':
        student_ids = request.POST.getlist('students')
        
        if not student_ids:
            django_messages.error(request, "Veuillez sélectionner au moins un élève")
            return redirect(f'/niveaux/primaire/conversation/{conversation_id}/add-participants/')
        
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
        
        return redirect(f'/niveaux/primaire/?conv={conversation.id}')
    
    if request.user.is_director:
        classrooms = Classroom.objects.filter(level=level)
    else:
        classrooms = request.user.taught_classes.filter(level=level)
    
    current_participants = conversation.participants.all()
    students = Student.objects.filter(classroom__in=classrooms).select_related('classroom').order_by('classroom__name', 'last_name', 'first_name')
    
    context = {
        'level': level,
        'conversation': conversation,
        'classrooms': classrooms,
        'students': students,
        'current_participants': current_participants,
    }
    return render(request, 'primaire/add_participants.html', context)


@login_required
def primaire_devoirs(request, classroom_id):
    return redirect(f'/niveaux/primaire/')


@login_required
def primaire_eleve(request, student_id):
    return redirect(f'/niveaux/primaire/')
