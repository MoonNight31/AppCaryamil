# interfaces/urls.py
from django.urls import path
from . import views_maternelle, views_primaire, views_college, views_home, views_parents, api_views, views_admin

urlpatterns = [
    # PAGE DE SÉLECTION
    path('', views_home.niveau_selector, name='niveau_selector'),
    
    # PANEL ADMINISTRATEUR PERSONNALISÉ
    path('administration/', views_admin.admin_dashboard, name='admin_dashboard'),
    path('administration/utilisateurs/', views_admin.admin_users_list, name='admin_users_list'),
    path('administration/professeurs/', views_admin.admin_teachers_list, name='admin_teachers_list'),
    path('administration/professeur/nouveau/', views_admin.admin_teacher_edit, name='admin_teacher_create'),
    path('administration/professeur/<int:teacher_id>/', views_admin.admin_teacher_edit, name='admin_teacher_edit'),
    path('administration/parents/', views_admin.admin_parents_list, name='admin_parents_list'),
    path('administration/parent/nouveau/', views_admin.admin_parent_edit, name='admin_parent_create'),
    path('administration/parent/<int:parent_id>/', views_admin.admin_parent_edit, name='admin_parent_edit'),
    path('administration/utilisateur/<int:user_id>/', views_admin.admin_user_edit, name='admin_user_edit'),
    path('administration/classes/', views_admin.admin_classes_list, name='admin_classes_list'),
    path('administration/classe/nouveau/', views_admin.admin_class_edit, name='admin_class_create'),
    path('administration/classe/<int:class_id>/', views_admin.admin_class_edit, name='admin_class_edit'),
    path('administration/eleves/', views_admin.admin_students_list, name='admin_students_list'),
    path('administration/eleve/nouveau/', views_admin.admin_student_edit, name='admin_student_create'),
    path('administration/eleve/<int:student_id>/', views_admin.admin_student_edit, name='admin_student_edit'),
    path('administration/niveaux/', views_admin.admin_levels_list, name='admin_levels_list'),
    path('administration/niveau/nouveau/', views_admin.admin_level_edit, name='admin_level_create'),
    path('administration/niveau/<int:level_id>/', views_admin.admin_level_edit, name='admin_level_edit'),
    
    # PAGE D'ACCUEIL PARENTS
    path('parents/', views_parents.parent_home, name='parent_home'),
    
    # API
    path('api/classroom/<int:classroom_id>/parents/', api_views.get_classroom_parents, name='api_classroom_parents'),
    
    # MATERNELLE - Interface Messenger
    path('maternelle/', views_maternelle.maternelle_dashboard, name='maternelle_dashboard'),
    path('maternelle/create-conversation/', views_maternelle.create_conversation, name='create_conversation'),
    path('maternelle/photos/<int:classroom_id>/', views_maternelle.maternelle_photos, name='maternelle_photos'),
    path('maternelle/eleves/<int:classroom_id>/', views_maternelle.maternelle_eleves, name='maternelle_eleves'),
    
    # PRIMAIRE - Interface structurée
    path('primaire/', views_primaire.primaire_dashboard, name='primaire_dashboard'),
    path('primaire/create-conversation/', views_primaire.create_conversation, name='primaire_create_conversation'),
    path('primaire/devoirs/<int:classroom_id>/', views_primaire.primaire_devoirs, name='primaire_devoirs'),
    path('primaire/eleve/<int:student_id>/', views_primaire.primaire_eleve, name='primaire_eleve'),
    
    # COLLÈGE - Interface académique
    path('college/', views_college.college_dashboard, name='college_dashboard'),
    path('college/create-conversation/', views_college.create_conversation, name='college_create_conversation'),
    path('college/notes/<int:student_id>/', views_college.college_notes, name='college_notes'),
    path('college/messages/', views_college.college_messages, name='college_messages'),
]
