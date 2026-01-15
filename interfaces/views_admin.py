# interfaces/views_admin.py
# Panel administrateur personnalisé

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from school_core.models import SchoolLevel, Classroom, Student, Conversation, Post, Message

User = get_user_model()


def user_is_admin(user):
    """Vérifie si l'utilisateur est admin (superuser ou directeur)"""
    return user.is_superuser or user.is_director


@login_required
def admin_dashboard(request):
    """Tableau de bord principal du panel admin"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé. Seuls les administrateurs peuvent accéder à cette page.")
        return redirect('niveau_selector')
    
    # Statistiques
    stats = {
        'total_students': Student.objects.count(),
        'total_teachers': User.objects.filter(is_teacher=True).count(),
        'total_parents': User.objects.filter(is_parent=True).count(),
        'total_classes': Classroom.objects.count(),
        'total_levels': SchoolLevel.objects.count(),
        'total_conversations': Conversation.objects.count(),
        'total_posts': Post.objects.filter(is_published=True).count(),
        'unread_messages': Message.objects.filter(is_read=False).count(),
    }
    
    # Activités récentes
    recent_posts = Post.objects.select_related('author', 'conversation').order_by('-created_at')[:5]
    recent_students = Student.objects.select_related('classroom').order_by('-id')[:5]
    
    context = {
        'stats': stats,
        'recent_posts': recent_posts,
        'recent_students': recent_students,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def admin_users_list(request):
    """Liste des utilisateurs (tous)"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    search = request.GET.get('search', '')
    role = request.GET.get('role', '')
    
    users = User.objects.all().order_by('-date_joined')
    
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    if role == 'teacher':
        users = users.filter(is_teacher=True)
    elif role == 'parent':
        users = users.filter(is_parent=True)
    elif role == 'director':
        users = users.filter(is_director=True)
    
    context = {
        'users': users,
        'search': search,
        'role': role,
    }
    return render(request, 'admin/users_list.html', context)


@login_required
def admin_teachers_list(request):
    """Liste des professeurs"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    search = request.GET.get('search', '')
    
    teachers = User.objects.filter(is_teacher=True).order_by('last_name', 'first_name')
    
    if search:
        teachers = teachers.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    context = {
        'teachers': teachers,
        'search': search,
    }
    return render(request, 'admin/teachers_list.html', context)


@login_required
def admin_parents_list(request):
    """Liste des parents"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    search = request.GET.get('search', '')
    
    parents = User.objects.filter(is_parent=True).prefetch_related('children').order_by('last_name', 'first_name')
    
    if search:
        parents = parents.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    context = {
        'parents': parents,
        'search': search,
    }
    return render(request, 'admin/parents_list.html', context)


@login_required
def admin_teacher_edit(request, teacher_id=None):
    """Créer ou éditer un professeur"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    teacher = get_object_or_404(User, id=teacher_id) if teacher_id else None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_director = request.POST.get('is_director') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        classroom_ids = request.POST.getlist('classrooms')
        
        if teacher:
            # Modification
            teacher.first_name = first_name
            teacher.last_name = last_name
            teacher.email = email
            teacher.is_director = is_director
            teacher.is_active = is_active
            if password:
                teacher.set_password(password)
            teacher.save()
            
            # Mettre à jour les classes
            Classroom.objects.filter(teacher=teacher).update(teacher=None)
            if classroom_ids:
                Classroom.objects.filter(id__in=classroom_ids).update(teacher=teacher)
            
            messages.success(request, f"Professeur {teacher.username} modifié avec succès.")
        else:
            # Création
            if not username or not password:
                messages.error(request, "Nom d'utilisateur et mot de passe sont obligatoires.")
                return redirect('admin_teacher_create')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Ce nom d'utilisateur existe déjà.")
                return redirect('admin_teacher_create')
            
            teacher = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_teacher=True,
                is_director=is_director,
                is_active=is_active
            )
            
            # Assigner les classes
            if classroom_ids:
                Classroom.objects.filter(id__in=classroom_ids).update(teacher=teacher)
            
            messages.success(request, f"Professeur {teacher.username} créé avec succès.")
        
        return redirect('admin_teachers_list')
    
    classrooms = Classroom.objects.select_related('level').order_by('level', 'name')
    assigned_classrooms = teacher.taught_classes.all() if teacher else []
    
    context = {
        'teacher': teacher,
        'classrooms': classrooms,
        'assigned_classrooms': assigned_classrooms,
    }
    return render(request, 'admin/teacher_edit.html', context)


@login_required
def admin_parent_edit(request, parent_id=None):
    """Créer ou éditer un parent"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    parent = get_object_or_404(User, id=parent_id) if parent_id else None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_active = request.POST.get('is_active') == 'on'
        student_ids = request.POST.getlist('children')
        
        if parent:
            # Modification
            parent.first_name = first_name
            parent.last_name = last_name
            parent.email = email
            parent.is_active = is_active
            if password:
                parent.set_password(password)
            parent.save()
            
            # Mettre à jour les enfants
            if student_ids:
                parent.children.set(student_ids)
            else:
                parent.children.clear()
            
            messages.success(request, f"Parent {parent.username} modifié avec succès.")
        else:
            # Création
            if not username or not password:
                messages.error(request, "Nom d'utilisateur et mot de passe sont obligatoires.")
                return redirect('admin_parent_create')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Ce nom d'utilisateur existe déjà.")
                return redirect('admin_parent_create')
            
            parent = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_parent=True,
                is_active=is_active
            )
            
            # Assigner les enfants
            if student_ids:
                parent.children.set(student_ids)
            
            messages.success(request, f"Parent {parent.username} créé avec succès.")
        
        return redirect('admin_parents_list')
    
    students = Student.objects.select_related('classroom').order_by('last_name', 'first_name')
    
    context = {
        'parent': parent,
        'students': students,
    }
    return render(request, 'admin/parent_edit.html', context)


@login_required
def admin_user_edit(request, user_id):
    """Éditer un utilisateur"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.is_teacher = request.POST.get('is_teacher') == 'on'
        user.is_parent = request.POST.get('is_parent') == 'on'
        user.is_director = request.POST.get('is_director') == 'on'
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
        
        messages.success(request, f"Utilisateur {user.username} modifié avec succès.")
        return redirect('admin_users_list')
    
    context = {
        'edit_user': user,
        'classes': user.taught_classes.all() if user.is_teacher else None,
        'children': user.children.all() if user.is_parent else None,
    }
    return render(request, 'admin/user_edit.html', context)


@login_required
def admin_classes_list(request):
    """Liste des classes"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    level_id = request.GET.get('level', '')
    search = request.GET.get('search', '')
    
    classes = Classroom.objects.select_related('level', 'teacher').annotate(
        student_count=Count('students')
    ).order_by('level', 'name')
    
    if level_id:
        classes = classes.filter(level_id=level_id)
    
    if search:
        classes = classes.filter(Q(name__icontains=search))
    
    levels = SchoolLevel.objects.all()
    
    context = {
        'classes': classes,
        'levels': levels,
        'selected_level': level_id,
        'search': search,
    }
    return render(request, 'admin/classes_list.html', context)


@login_required
def admin_class_edit(request, class_id=None):
    """Créer ou éditer une classe"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    classroom = get_object_or_404(Classroom, id=class_id) if class_id else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        level_id = request.POST.get('level')
        teacher_id = request.POST.get('teacher')
        school_year = request.POST.get('school_year')
        
        if classroom:
            classroom.name = name
            classroom.level_id = level_id
            classroom.teacher_id = teacher_id if teacher_id else None
            classroom.school_year = school_year
            classroom.save()
            messages.success(request, f"Classe {classroom.name} modifiée avec succès.")
        else:
            classroom = Classroom.objects.create(
                name=name,
                level_id=level_id,
                teacher_id=teacher_id if teacher_id else None,
                school_year=school_year
            )
            messages.success(request, f"Classe {classroom.name} créée avec succès.")
        
        return redirect('admin_classes_list')
    
    levels = SchoolLevel.objects.all()
    teachers = User.objects.filter(is_teacher=True)
    
    context = {
        'classroom': classroom,
        'levels': levels,
        'teachers': teachers,
    }
    return render(request, 'admin/class_edit.html', context)


@login_required
def admin_students_list(request):
    """Liste des élèves"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    class_id = request.GET.get('class', '')
    search = request.GET.get('search', '')
    
    students = Student.objects.select_related('classroom', 'classroom__level').prefetch_related('parents').order_by('last_name', 'first_name')
    
    if class_id:
        students = students.filter(classroom_id=class_id)
    
    if search:
        students = students.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    classes = Classroom.objects.select_related('level').order_by('level', 'name')
    
    context = {
        'students': students,
        'classes': classes,
        'selected_class': class_id,
        'search': search,
    }
    return render(request, 'admin/students_list.html', context)


@login_required
def admin_student_edit(request, student_id=None):
    """Créer ou éditer un élève"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    student = get_object_or_404(Student, id=student_id) if student_id else None
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        classroom_id = request.POST.get('classroom')
        parent_ids = request.POST.getlist('parents')
        
        if student:
            student.first_name = first_name
            student.last_name = last_name
            student.date_of_birth = date_of_birth if date_of_birth else None
            student.classroom_id = classroom_id if classroom_id else None
            if 'photo' in request.FILES:
                student.photo = request.FILES['photo']
            student.save()
            student.parents.set(parent_ids)
            messages.success(request, f"Élève {student.first_name} {student.last_name} modifié avec succès.")
        else:
            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth if date_of_birth else None,
                classroom_id=classroom_id if classroom_id else None,
                photo=request.FILES.get('photo')
            )
            student.parents.set(parent_ids)
            messages.success(request, f"Élève {student.first_name} {student.last_name} créé avec succès.")
        
        return redirect('admin_students_list')
    
    classrooms = Classroom.objects.select_related('level').order_by('level', 'name')
    parents = User.objects.filter(is_parent=True).order_by('last_name', 'first_name')
    
    context = {
        'student': student,
        'classrooms': classrooms,
        'parents': parents,
    }
    return render(request, 'admin/student_edit.html', context)


@login_required
def admin_levels_list(request):
    """Liste des niveaux scolaires"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    levels = SchoolLevel.objects.annotate(
        class_count=Count('classrooms')
    ).order_by('id')
    
    context = {
        'levels': levels,
    }
    return render(request, 'admin/levels_list.html', context)


@login_required
def admin_level_edit(request, level_id=None):
    """Créer ou éditer un niveau"""
    if not user_is_admin(request.user):
        messages.error(request, "Accès refusé.")
        return redirect('niveau_selector')
    
    level = get_object_or_404(SchoolLevel, id=level_id) if level_id else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        
        if level:
            level.name = name
            level.slug = slug
            level.description = description
            level.save()
            messages.success(request, f"Niveau {level.name} modifié avec succès.")
        else:
            level = SchoolLevel.objects.create(
                name=name,
                slug=slug,
                description=description
            )
            messages.success(request, f"Niveau {level.name} créé avec succès.")
        
        return redirect('admin_levels_list')
    
    context = {
        'level': level,
    }
    return render(request, 'admin/level_edit.html', context)
