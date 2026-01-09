from django.contrib import admin
from .models import SchoolLevel, Classroom, Student, Post, Message, Conversation


@admin.register(SchoolLevel)
class SchoolLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'teacher', 'school_year', 'student_count']
    list_filter = ['level', 'school_year']
    search_fields = ['name', 'teacher__username']
    
    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Nombre d\'élèves'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'classroom', 'date_of_birth']
    list_filter = ['classroom__level', 'classroom']
    search_fields = ['first_name', 'last_name']
    filter_horizontal = ['parents']
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'photo')
        }),
        ('Scolarité', {
            'fields': ('classroom',)
        }),
        ('Famille', {
            'fields': ('parents',)
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'conversation', 'classroom', 'author', 'created_at', 'is_published']
    list_filter = ['conversation__conversation_type', 'is_published', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'recipient', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['subject', 'content', 'sender__username', 'recipient__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['name', 'conversation_type', 'classroom', 'created_by', 'participant_count', 'last_message_at']
    list_filter = ['conversation_type', 'classroom__level', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['participants']
    readonly_fields = ['created_at', 'last_message_at']
    date_hierarchy = 'created_at'
    
    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = 'Participants'
