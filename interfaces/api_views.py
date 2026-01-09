# interfaces/api_views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from school_core.models import Classroom
from django.shortcuts import get_object_or_404


@login_required
def get_classroom_parents(request, classroom_id):
    """API pour récupérer les élèves d'une classe (pour inviter leurs parents)"""
    classroom = get_object_or_404(Classroom, id=classroom_id)
    
    # Récupérer tous les élèves de cette classe avec le nombre de parents
    students = []
    
    for student in classroom.students.all():
        parents_count = student.parents.count()
        students.append({
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'parents_count': parents_count
        })
    
    return JsonResponse(students, safe=False)
