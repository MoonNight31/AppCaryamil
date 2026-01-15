from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rôles', {
            'fields': ('is_parent', 'is_teacher', 'is_director'),
            'description': '⚠️ Un directeur reçoit automatiquement : accès admin (is_staff) + statut professeur (is_teacher)'
        }),
    )
    list_display = ['username', 'email', 'full_name', 'role_badges', 'is_staff', 'related_info']
    list_filter = ['is_parent', 'is_teacher', 'is_director', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    # Configuration pour l'autocomplétion - important pour les références depuis d'autres modèles
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_delete_permission(self, request, obj=None):
        # Seuls les superusers peuvent supprimer des utilisateurs
        return request.user.is_superuser
    
    def full_name(self, obj):
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return "-"
    full_name.short_description = 'Nom complet'
    
    def role_badges(self, obj):
        badges = []
        if obj.is_director:
            badges.append('<span style="background: #1a73e8; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; margin-right: 3px;">🎓 DIRECTEUR</span>')
        elif obj.is_teacher:
            badges.append('<span style="background: #34a853; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; margin-right: 3px;">👨‍🏫 PROFESSEUR</span>')
        if obj.is_parent:
            badges.append('<span style="background: #fbbc04; color: #333; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; margin-right: 3px;">👨‍👩‍👧 PARENT</span>')
        return format_html(' '.join(badges)) if badges else '-'
    role_badges.short_description = 'Rôles'
    
    def related_info(self, obj):
        info = []
        
        # Si c'est un directeur
        if obj.is_director:
            info.append('<span style="color: #1a73e8; font-weight: bold;">🔑 Accès admin complet</span>')
        
        # Si c'est un professeur
        if obj.is_teacher:
            classes = obj.taught_classes.all()
            if classes:
                class_links = []
                for cls in classes:
                    url = reverse('admin:school_core_classroom_change', args=[cls.id])
                    class_links.append(f'<a href="{url}">{cls.name}</a>')
                info.append(f"Enseigne: {', '.join(class_links)}")
        
        # Si c'est un parent
        if obj.is_parent:
            children = obj.children.all()
            if children:
                child_links = []
                for child in children:
                    url = reverse('admin:school_core_student_change', args=[child.id])
                    child_links.append(f'<a href="{url}">{child.first_name} {child.last_name}</a>')
                info.append(f"Enfants: {', '.join(child_links)}")
        
        if info:
            return format_html('<br>'.join(info))
        return "-"
    related_info.short_description = 'Informations liées'
    
    # Ajouter des actions personnalisées
    actions = ['make_teacher', 'make_parent', 'make_director', 'remove_teacher', 'remove_parent', 'remove_director']
    
    def make_teacher(self, request, queryset):
        updated = queryset.update(is_teacher=True)
        self.message_user(request, f"{updated} utilisateur(s) marqué(s) comme professeur(s).")
    make_teacher.short_description = "✓ Marquer comme professeur"
    
    def make_parent(self, request, queryset):
        updated = queryset.update(is_parent=True)
        self.message_user(request, f"{updated} utilisateur(s) marqué(s) comme parent(s).")
    make_parent.short_description = "✓ Marquer comme parent"
    
    def make_director(self, request, queryset):
        updated = queryset.update(is_director=True, is_teacher=True)
        self.message_user(request, f"{updated} utilisateur(s) marqué(s) comme directeur(s) (et professeur).")
    make_director.short_description = "🎓 Marquer comme directeur"
    
    def remove_teacher(self, request, queryset):
        updated = queryset.update(is_teacher=False, is_director=False)
        self.message_user(request, f"{updated} utilisateur(s) n'est/ne sont plus professeur(s) ni directeur(s).")
    remove_teacher.short_description = "✗ Retirer le rôle professeur"
    
    def remove_parent(self, request, queryset):
        updated = queryset.update(is_parent=False)
        self.message_user(request, f"{updated} utilisateur(s) n'est/ne sont plus parent(s).")
    remove_parent.short_description = "✗ Retirer le rôle parent"
    
    def remove_director(self, request, queryset):
        updated = queryset.update(is_director=False)
        self.message_user(request, f"{updated} utilisateur(s) n'est/ne sont plus directeur(s) (reste professeur).")
    remove_director.short_description = "✗ Retirer le rôle directeur"
