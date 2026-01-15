from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import SchoolLevel, Classroom, Student, Post, Message, Conversation


@admin.register(SchoolLevel)
class SchoolLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'classroom_count', 'student_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def classroom_count(self, obj):
        count = obj.classrooms.count()
        url = reverse('admin:school_core_classroom_changelist') + f'?level__id__exact={obj.id}'
        return format_html('<a href="{}">{} classe(s)</a>', url, count)
    classroom_count.short_description = 'Classes'
    
    def student_count(self, obj):
        count = Student.objects.filter(classroom__level=obj).count()
        return f"{count} élève(s)"
    student_count.short_description = 'Élèves'


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'teacher_link', 'school_year', 'student_count']
    list_filter = ['level', 'school_year']
    search_fields = ['name', 'teacher__username', 'teacher__first_name', 'teacher__last_name']
    autocomplete_fields = ['teacher']
    list_editable = ['school_year']
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    fieldsets = (
        ('Informations de la classe', {
            'fields': ('name', 'level', 'school_year')
        }),
        ('Enseignant', {
            'fields': ('teacher',)
        }),
    )
    
    def teacher_link(self, obj):
        if obj.teacher:
            url = reverse('admin:accounts_customuser_change', args=[obj.teacher.id])
            name = obj.teacher.get_full_name() or obj.teacher.username
            if obj.teacher.is_director:
                return format_html('<a href="{}">🎓 {} <span style="color: #1a73e8; font-weight: bold;">(Directeur)</span></a>', url, name)
            return format_html('<a href="{}">{}</a>', url, name)
        return "-"
    teacher_link.short_description = 'Professeur'
    
    def student_count(self, obj):
        count = obj.students.count()
        url = reverse('admin:school_core_student_changelist') + f'?classroom__id__exact={obj.id}'
        return format_html('<a href="{}">{} élève(s)</a>', url, count)
    student_count.short_description = 'Élèves'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'classroom_link', 'level', 'parent_count', 'age', 'photo_preview']
    list_filter = ['classroom__level', 'classroom']
    search_fields = ['first_name', 'last_name', 'parents__username', 'parents__first_name', 'parents__last_name']
    filter_horizontal = ['parents']
    autocomplete_fields = ['classroom']
    list_select_related = ['classroom', 'classroom__level']
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'photo')
        }),
        ('Scolarité', {
            'fields': ('classroom',)
        }),
        ('Famille', {
            'fields': ('parents',),
            'description': 'Sélectionnez les parents de l\'élève'
        }),
    )
    
    def classroom_link(self, obj):
        if obj.classroom:
            url = reverse('admin:school_core_classroom_change', args=[obj.classroom.id])
            return format_html('<a href="{}">{}</a>', url, obj.classroom.name)
        return "-"
    classroom_link.short_description = 'Classe'
    
    def level(self, obj):
        return obj.classroom.level if obj.classroom else "-"
    level.short_description = 'Niveau'
    
    def parent_count(self, obj):
        count = obj.parents.count()
        if count > 0:
            parents_list = ", ".join([p.get_full_name() or p.username for p in obj.parents.all()])
            return format_html('<span title="{}">{} parent(s)</span>', parents_list, count)
        return "0 parent"
    parent_count.short_description = 'Parents'
    
    def age(self, obj):
        if obj.date_of_birth:
            from datetime import date
            today = date.today()
            age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return f"{age} ans"
        return "-"
    age.short_description = 'Âge'
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />', obj.photo.url)
        return "-"
    photo_preview.short_description = 'Photo'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'conversation_link', 'author_link', 'created_at', 'is_published', 'has_image']
    list_filter = ['conversation__conversation_type', 'is_published', 'created_at', 'conversation__classroom__level']
    search_fields = ['title', 'description', 'author__username', 'author__first_name', 'author__last_name']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'image_preview']
    list_editable = ['is_published']
    autocomplete_fields = ['author', 'conversation', 'classroom']
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'description', 'image', 'image_preview')
        }),
        ('Publication', {
            'fields': ('author', 'conversation', 'classroom', 'is_published')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def conversation_link(self, obj):
        if obj.conversation:
            url = reverse('admin:school_core_conversation_change', args=[obj.conversation.id])
            return format_html('<a href="{}">{}</a>', url, obj.conversation.name)
        return "-"
    conversation_link.short_description = 'Conversation'
    
    def author_link(self, obj):
        url = reverse('admin:accounts_customuser_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.get_full_name() or obj.author.username)
    author_link.short_description = 'Auteur'
    
    def has_image(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.image else 'gray',
            '✓' if obj.image else '✗'
        )
    has_image.short_description = 'Image'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 300px;" />', obj.image.url)
        return "Aucune image"
    image_preview.short_description = 'Aperçu'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender_link', 'recipient_link', 'created_at', 'is_read', 'read_status']
    list_filter = ['is_read', 'created_at']
    search_fields = ['subject', 'content', 'sender__username', 'recipient__username', 
                    'sender__first_name', 'sender__last_name', 'recipient__first_name', 'recipient__last_name']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    autocomplete_fields = ['sender', 'recipient']
    list_editable = ['is_read']
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_delete_permission(self, request, obj=None):
        # Les directeurs ne peuvent pas supprimer les messages
        return request.user.is_superuser
    
    def sender_link(self, obj):
        url = reverse('admin:accounts_customuser_change', args=[obj.sender.id])
        return format_html('<a href="{}">{}</a>', url, obj.sender.get_full_name() or obj.sender.username)
    sender_link.short_description = 'Expéditeur'
    
    def recipient_link(self, obj):
        url = reverse('admin:accounts_customuser_change', args=[obj.recipient.id])
        return format_html('<a href="{}">{}</a>', url, obj.recipient.get_full_name() or obj.recipient.username)
    recipient_link.short_description = 'Destinataire'
    
    def read_status(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            'green' if obj.is_read else 'red',
            'Lu' if obj.is_read else 'Non lu'
        )
    read_status.short_description = 'Statut'


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['name', 'conversation_type', 'classroom_link', 'created_by_link', 'participant_count', 'post_count', 'last_message_at']
    list_filter = ['conversation_type', 'classroom__level', 'created_at']
    search_fields = ['name', 'participants__username', 'participants__first_name', 'participants__last_name']
    filter_horizontal = ['participants']
    readonly_fields = ['created_at', 'last_message_at', 'participant_list']
    date_hierarchy = 'created_at'
    autocomplete_fields = ['classroom', 'created_by']
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_director
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_director
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'conversation_type', 'classroom')
        }),
        ('Participants', {
            'fields': ('participants', 'participant_list')
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'created_at', 'last_message_at'),
            'classes': ('collapse',)
        }),
    )
    
    def classroom_link(self, obj):
        if obj.classroom:
            url = reverse('admin:school_core_classroom_change', args=[obj.classroom.id])
            return format_html('<a href="{}">{}</a>', url, obj.classroom.name)
        return "-"
    classroom_link.short_description = 'Classe'
    
    def created_by_link(self, obj):
        if obj.created_by:
            url = reverse('admin:accounts_customuser_change', args=[obj.created_by.id])
            return format_html('<a href="{}">{}</a>', url, obj.created_by.get_full_name() or obj.created_by.username)
        return "-"
    created_by_link.short_description = 'Créé par'
    
    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = 'Participants'
    
    def post_count(self, obj):
        count = obj.posts.count()
        url = reverse('admin:school_core_post_changelist') + f'?conversation__id__exact={obj.id}'
        return format_html('<a href="{}">{} post(s)</a>', url, count)
    post_count.short_description = 'Publications'
    
    def participant_list(self, obj):
        participants = obj.participants.all()
        if participants:
            html = '<ul>'
            for p in participants:
                url = reverse('admin:accounts_customuser_change', args=[p.id])
                role = []
                if p.is_teacher:
                    role.append('Professeur')
                if p.is_parent:
                    role.append('Parent')
                role_str = ' - ' + ', '.join(role) if role else ''
                html += f'<li><a href="{url}">{p.get_full_name() or p.username}</a>{role_str}</li>'
            html += '</ul>'
            return mark_safe(html)
        return "Aucun participant"
    participant_list.short_description = 'Liste des participants'
