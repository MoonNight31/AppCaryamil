# 🔐 Guide de Connexion - AppCaryamil

## 🚀 Accéder à l'application

### 1️⃣ **Démarrer le serveur**
```bash
python manage.py runserver
```

Le serveur démarre sur: **http://127.0.0.1:8000/**

---

## 👨‍💼 **Administration (Super Admin)**

### Se connecter à l'admin Django
1. Allez sur: **http://127.0.0.1:8000/admin/**
2. Utilisez vos identifiants de superutilisateur:
   - **Username**: `admin`
   - **Password**: celui créé avec `createsuperuser`

### Configuration initiale (OBLIGATOIRE)

#### ✅ **Étape 1: Créer les niveaux scolaires**
1. Dans l'admin, cliquez sur **"Niveaux scolaires"** → **"Ajouter"**
2. Créez:
   - **Maternelle** (slug: `maternelle`)
   - **Primaire** (slug: `primaire`)
   - **Collège** (slug: `college`)
   - **Lycée** (slug: `lycee`)

#### ✅ **Étape 2: Créer des classes**
1. Cliquez sur **"Classes"** → **"Ajouter"**
2. Exemple pour maternelle:
   - Nom: `Petite Section A`
   - Niveau: `Maternelle`
   - Enseignant: (optionnel)

#### ✅ **Étape 3: Créer des utilisateurs**
1. Cliquez sur **"Custom users"** → **"Ajouter"**
2. Pour un parent:
   - Username: `parent1`
   - Cochez: ✅ `Is parent`
3. Pour un enseignant:
   - Username: `prof1`
   - Cochez: ✅ `Is teacher`

#### ✅ **Étape 4: Créer des élèves**
1. Cliquez sur **"Élèves"** → **"Ajouter"**
2. Remplissez:
   - Prénom, Nom
   - Classe (sélectionnez une classe créée)
   - Parents (sélectionnez les parents)

---

## 🎓 **Accéder aux Interfaces par Niveau**

### 🌐 Page de sélection
**URL**: http://127.0.0.1:8000/niveaux/

Cette page affiche tous les niveaux disponibles. Cliquez sur celui que vous voulez.

### 🎨 **Maternelle** (Interface colorée)
**URL**: http://127.0.0.1:8000/niveaux/maternelle/
- Design ludique avec police Comic Neue
- Focus sur les photos et activités
- Grandes icônes colorées

### 📘 **Primaire** (Interface structurée)
**URL**: http://127.0.0.1:8000/niveaux/primaire/
- Design sobre et organisé
- Devoirs et évaluations
- Suivi des élèves

### 📚 **Collège** (Interface académique)
**URL**: http://127.0.0.1:8000/niveaux/college/
- Notes par matière
- Messagerie enseignant-parent
- Bulletin scolaire

### 🎓 **Lycée** (Interface professionnelle)
**URL**: http://127.0.0.1:8000/niveaux/lycee/
- Bulletins détaillés avec moyennes
- Statistiques de classe
- Graphiques de progression

---

## 🔑 **Connexion selon votre rôle**

### 👨‍🏫 **Enseignant** (`is_teacher = True`)
1. Connectez-vous avec votre compte enseignant
2. Allez sur: http://127.0.0.1:8000/niveaux/
3. Vous verrez les niveaux où vous avez des classes assignées
4. Vous pouvez:
   - Voir vos classes
   - Publier des photos/messages
   - Ajouter des notes (Primaire/Collège/Lycée)
   - Envoyer des messages aux parents

### 👨‍👩‍👧 **Parent** (`is_parent = True`)
1. Connectez-vous avec votre compte parent
2. Allez sur: http://127.0.0.1:8000/niveaux/
3. Vous verrez les niveaux de vos enfants
4. Vous pouvez:
   - Voir les photos/publications
   - Consulter les notes
   - Recevoir/envoyer des messages
   - Suivre le bulletin

### 👑 **Super Admin**
- Accès complet à tous les niveaux
- Peut gérer toutes les données via l'admin
- Peut créer/modifier utilisateurs, classes, élèves

---

## 📋 **Flux de connexion complet**

```
1. Démarrer serveur
   ↓
2. http://127.0.0.1:8000/admin/
   ↓
3. Créer niveaux, classes, utilisateurs, élèves
   ↓
4. Se déconnecter de l'admin
   ↓
5. http://127.0.0.1:8000/niveaux/
   ↓
6. Se connecter avec un compte (parent/enseignant)
   ↓
7. Choisir un niveau (maternelle/primaire/college/lycee)
   ↓
8. Accéder à l'interface personnalisée
```

---

## 🛠️ **Données de test rapides**

Pour créer des données de test rapidement, utilisez le shell Django:

```bash
python manage.py shell
```

```python
from school_core.models import SchoolLevel, Classroom, Student
from accounts.models import CustomUser

# Créer les niveaux
maternelle = SchoolLevel.objects.create(name="Maternelle", slug="maternelle")
primaire = SchoolLevel.objects.create(name="Primaire", slug="primaire")
college = SchoolLevel.objects.create(name="Collège", slug="college")
lycee = SchoolLevel.objects.create(name="Lycée", slug="lycee")

# Créer une classe
classe = Classroom.objects.create(
    level=maternelle,
    name="Petite Section A"
)

# Créer un parent
parent = CustomUser.objects.create_user(
    username="parent1",
    password="password123",
    is_parent=True
)

# Créer un élève
eleve = Student.objects.create(
    first_name="Pierre",
    last_name="Dupont",
    classroom=classe
)
eleve.parents.add(parent)

print("✅ Données de test créées !")
```

---

## ❓ **Problèmes fréquents**

### "Page not found" sur /niveaux/
→ Vérifiez que le serveur tourne et que les URLs sont bien configurées

### "Aucun niveau disponible"
→ Créez les niveaux via l'admin Django

### "Permission denied"
→ Connectez-vous d'abord avec un compte valide

### Impossible de se connecter
→ Vérifiez vos identifiants ou créez un nouveau superuser:
```bash
python manage.py createsuperuser
```

---

## 📱 **Accès rapide - Liens utiles**

| Page | URL |
|------|-----|
| Accueil | http://127.0.0.1:8000/ |
| Admin Django | http://127.0.0.1:8000/admin/ |
| Sélection niveau | http://127.0.0.1:8000/niveaux/ |
| Maternelle | http://127.0.0.1:8000/niveaux/maternelle/ |
| Primaire | http://127.0.0.1:8000/niveaux/primaire/ |
| Collège | http://127.0.0.1:8000/niveaux/college/ |
| Lycée | http://127.0.0.1:8000/niveaux/lycee/ |

---

**🎉 Vous êtes prêt à utiliser AppCaryamil !**
