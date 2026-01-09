# interfaces/views_college.py
# Vue spécifique pour le COLLÈGE (Interface Messenger avec conversations)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from school_core.models import SchoolLevel, Classroom, Post, Student, Conversation
from django.db.models import Q
from django.utils import timezone


@login_required
def college_dashboard(request):
    """Interface Messenger - Conversations de groupe et privées"""
    level = get_object_or_404(SchoolLevel, slug='college')
    
    conversations = Conversation.objects.filter(
        Q(participants=request.user) | Q(created_by=request.user)
    ).filter(
        Q(classroom__level=level) | Q(classroom__isnull=True, participants__children__classroom__level=level)
    ).distinct().order_by('-last_message_at')[:50]
    
    conversation_id = request.GET.get('conv')
    if conversation_id:
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
            return redirect(f'/niveaux/college/?conv={selected_conversation.id}')
    
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
        'can_post': True,
        'classrooms': classrooms,
        'can_create_conversation': request.user.is_teacher,
    }
    return render(request, 'college/messenger.html', context)


@login_required
def create_conversation(request):
    """Créer une nouvelle conversation privée (enseignants uniquement)"""
    if not request.user.is_teacher:
        django_messages.error(request, "Seuls les enseignants peuvent créer des conversations")
        return redirect('/niveaux/college/')
    
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom')
        student_ids = request.POST.getlist('students')
        conversation_name = request.POST.get('name')
        
        if not (classroom_id and student_ids):
            django_messages.error(request, "Veuillez sélectionner une classe et au moins un élève")
            return redirect('/niveaux/college/')
        
        classroom = get_object_or_404(Classroom, id=classroom_id)
        
        # Créer la conversation
        conversation = Conversation.objects.create(
            name=conversation_name or f"Discussion {classroom.name}",
            conversation_type='private',
            classroom=classroom,
            created_by=request.user
        )
        
        # Ajouter l'enseignant
        conversation.participants.add(request.user)
        
        # Ajouter les parents des élèves sélectionnés
        from school_core.models import Student
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            for parent in student.parents.all():
                conversation.participants.add(parent)
        
        django_messages.success(request, f"💬 Conversation créée avec succès !")
        return redirect(f'/niveaux/college/?conv={conversation.id}')
    
    return redirect('/niveaux/college/')


@login_required
def college_notes(request, student_id):
    return redirect(f'/niveaux/college/')


@login_required
def college_messages(request):
    return redirect(f'/niveaux/college/')
