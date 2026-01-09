# interfaces/views_parents.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from school_core.models import Post, Conversation
from django.db.models import Q


@login_required
def parent_home(request):
    """Page d'accueil pour les parents avec toutes les photos envoyées"""
    
    # Rediriger si ce n'est pas un parent
    if not request.user.is_parent:
        return redirect('niveau_selector')
    
    # Récupérer toutes les conversations du parent
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related('posts', 'classroom', 'classroom__level')
    
    # Récupérer tous les posts des conversations du parent
    posts = Post.objects.filter(
        conversation__participants=request.user,
        image__isnull=False  # Seulement les posts avec photo
    ).exclude(image='').select_related('author', 'conversation', 'conversation__classroom').order_by('-created_at')
    
    # Récupérer les enfants du parent
    children = request.user.children.all().select_related('classroom', 'classroom__level')
    
    context = {
        'posts': posts,
        'conversations': conversations,
        'children': children,
        'total_posts': posts.count(),
    }
    
    return render(request, 'parents/home.html', context)
