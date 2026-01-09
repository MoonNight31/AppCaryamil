# interfaces/urls.py
from django.urls import path
from . import views_maternelle, views_primaire, views_college, views_home, views_parents, api_views

urlpatterns = [
    # PAGE DE SÉLECTION
    path('', views_home.niveau_selector, name='niveau_selector'),
    
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
