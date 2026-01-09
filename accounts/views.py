# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    """Page de connexion personnalisée"""
    if request.user.is_authenticated:
        return redirect('/niveaux/')
    
    form = AuthenticationForm()
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        next_url = request.POST.get('next', '/niveaux/')
        
        if not username or not password:
            error_message = "Veuillez remplir tous les champs"
        else:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bienvenue {user.get_full_name() or user.username} !')
                return redirect(next_url)
            else:
                error_message = "Identifiant ou mot de passe incorrect"
    
    return render(request, 'accounts/login.html', {
        'form': form,
        'error_message': error_message,
        'next': request.GET.get('next', '/niveaux/')
    })


@login_required
def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès')
    return redirect('login')



