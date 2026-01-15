# interfaces/views_home.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from school_core.models import SchoolLevel


@login_required
def niveau_selector(request):
    """Page de sélection du niveau scolaire"""
    levels = SchoolLevel.objects.all()
    
    # Déterminer les niveaux accessibles pour l'utilisateur
    user_levels = []
    
    if request.user.is_director or request.user.is_superuser:
        # Directeurs et super admin: tous les niveaux
        user_levels = list(levels)
    elif request.user.is_parent:
        # Parents: afficher les niveaux de leurs enfants
        children = request.user.children.all()
        for child in children:
            if child.classroom and child.classroom.level not in user_levels:
                user_levels.append(child.classroom.level)
    elif request.user.is_teacher:
        # Enseignants: afficher les niveaux de leurs classes
        classrooms = request.user.taught_classes.all()
        for classroom in classrooms:
            if classroom.level not in user_levels:
                user_levels.append(classroom.level)
    
    context = {
        'levels': levels,
        'user_levels': user_levels,
    }
    return render(request, 'home/niveau_selector.html', context)
