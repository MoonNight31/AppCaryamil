from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # On ajoute des booléens pour savoir qui est qui facilement
    is_parent = models.BooleanField(default=False, verbose_name="Est parent")
    is_teacher = models.BooleanField(default=False, verbose_name="Est professeur")
    is_director = models.BooleanField(default=False, verbose_name="Est directeur")

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Les directeurs ont automatiquement accès au panel admin
        if self.is_director:
            self.is_staff = True
            self.is_teacher = True  # Un directeur est aussi professeur
        super().save(*args, **kwargs)
    
    def get_role_display(self):
        """Retourne une chaîne lisible des rôles de l'utilisateur"""
        roles = []
        if self.is_director:
            roles.append("Directeur")
        elif self.is_teacher:
            roles.append("Professeur")
        if self.is_parent:
            roles.append("Parent")
        return " / ".join(roles) if roles else "Utilisateur"