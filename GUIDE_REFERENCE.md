# Guide de Référence Rapide - AppCaryamil

## 📚 Table des Matières
1. [Résumé du Système](#résumé-du-système)
2. [Structure de la BDD](#structure-de-la-bdd)
3. [Relations Clés](#relations-clés)
4. [Cas d'Utilisation Principaux](#cas-dutilisation-principaux)
5. [API Endpoints](#api-endpoints)
6. [Commandes Management](#commandes-management)
7. [Checklist d'Implémentation](#checklist-dimplémentation)

---

## Résumé du Système

### 🎯 Objectif
Application Django de gestion et communication scolaire pour une école avec trois niveaux : **Maternelle**, **Primaire** et **Collège**.

### 👥 Acteurs
- **Directeur** : Administration complète
- **Professeur** : Gestion de classe et communication
- **Parent** : Suivi des enfants

### 🏗️ Architecture
```
┌─────────────────────────────────────────────────────┐
│                   AppCaryamil                        │
├─────────────────────────────────────────────────────┤
│  Modules Django:                                    │
│  ├─ accounts       (Authentification)               │
│  ├─ school_core    (Modèles métier)                 │
│  ├─ interfaces     (Vues et templates)              │
│  └─ config         (Configuration)                  │
└─────────────────────────────────────────────────────┘
```

---

## Structure de la BDD

### 📊 Modèles (7 au total)

| Modèle | Module | Description | Rôle |
|--------|--------|-------------|------|
| **CustomUser** | accounts | Utilisateurs (parents, profs, directeurs) | Authentification & Autorisation |
| **SchoolLevel** | school_core | Niveaux scolaires (Maternelle, Primaire, Collège) | Organisation hiérarchique |
| **Classroom** | school_core | Classes (CP A, CE1 B, etc.) | Regroupement d'élèves |
| **Student** | school_core | Élèves | Enfants scolarisés |
| **Conversation** | school_core | Conversations (groupe ou privées) | Communication |
| **Post** | school_core | Publications (photos, messages) | Contenu partagé |
| **Message** | school_core | Messages directs | Messagerie privée |

---

## Relations Clés

### Diagramme Simplifié
```
        CustomUser
            │
    ┌───────┼───────┬────────┐
    │       │       │        │
    ▼       ▼       ▼        ▼
Teacher  Parents  Author  Participants
    │       │       │        │
    ▼       ▼       ▼        ▼
Classroom ← Student → Post ← Conversation
    │                          │
    ▼                          │
SchoolLevel                    │
                               │
                          Message
```

### Relations par Modèle

#### CustomUser (1 utilisateur peut...)
- ✅ Enseigner plusieurs classes (`taught_classes`)
- ✅ Être parent de plusieurs élèves (`children`)
- ✅ Participer à plusieurs conversations (`conversations`)
- ✅ Créer plusieurs conversations (`created_conversations`)
- ✅ Envoyer/recevoir des messages (`sent_messages`, `received_messages`)
- ✅ Publier plusieurs posts (author de `Post`)

#### Classroom (1 classe...)
- ✅ Appartient à 1 niveau scolaire
- ✅ A 1 professeur principal (nullable)
- ✅ Contient plusieurs élèves
- ✅ A 1 conversation de groupe

#### Student (1 élève...)
- ✅ Est dans 1 classe (nullable)
- ✅ A plusieurs parents (N:N)

#### Conversation (1 conversation...)
- ✅ Peut être liée à 1 classe (si type='group')
- ✅ A plusieurs participants (N:N)
- ✅ Contient plusieurs posts

---

## Cas d'Utilisation Principaux

### 🔑 Matrice des Actions

| Action | Directeur | Professeur | Parent |
|--------|-----------|------------|--------|
| **GESTION** |
| Créer/Modifier niveaux | ✅ | ❌ | ❌ |
| Créer/Modifier classes | ✅ | ❌ | ❌ |
| Créer/Modifier élèves | ✅ | ❌ | ❌ |
| Créer/Modifier utilisateurs | ✅ | ❌ | ❌ |
| **COMMUNICATION** |
| Publier dans groupe classe | ✅ | ✅ | ❌ |
| Publier dans conversation privée | ✅ | ✅ | ✅ |
| Créer conversation de groupe | ✅ | ✅ | ❌ |
| Créer conversation privée | ✅ | ✅ | ✅ |
| Envoyer message direct | ✅ | ✅ | ✅ (limité) |
| **CONSULTATION** |
| Voir toutes les classes | ✅ | ❌ | ❌ |
| Voir sa classe | ✅ | ✅ | ❌ |
| Voir ses enfants | N/A | N/A | ✅ |
| Voir publications | ✅ | ✅ | ✅ (limité) |
| Voir statistiques | ✅ | ✅ (limité) | ❌ |

---

## API Endpoints

### 🌐 Structure des URLs

#### Authentification
```
/accounts/
├─ login/           GET, POST   - Page de connexion
└─ logout/          POST        - Déconnexion
```

#### Interface Directeur (Admin)
```
/admin/
├─ dashboard/                  - Tableau de bord
├─ levels/                     - Liste des niveaux
│  ├─ create/                 - Créer niveau
│  ├─ <id>/edit/              - Modifier niveau
│  └─ <id>/delete/            - Supprimer niveau
├─ classes/                    - Liste des classes
│  ├─ create/                 - Créer classe
│  ├─ <id>/edit/              - Modifier classe
│  └─ <id>/delete/            - Supprimer classe
├─ students/                   - Liste des élèves
│  ├─ create/                 - Créer élève
│  ├─ <id>/edit/              - Modifier élève
│  └─ <id>/delete/            - Supprimer élève
├─ teachers/                   - Liste des professeurs
├─ parents/                    - Liste des parents
└─ users/                      - Liste des utilisateurs
```

#### Interface Professeur
```
/interfaces/
├─ maternelle/
│  ├─ dashboard/              - Tableau de bord Maternelle
│  ├─ messenger/              - Messagerie
│  ├─ photos/                 - Galerie photos
│  └─ create-conversation/    - Créer conversation
├─ primaire/
│  ├─ dashboard/              - Tableau de bord Primaire
│  ├─ messenger/              - Messagerie
│  └─ create-conversation/    - Créer conversation
└─ college/
   ├─ messenger/              - Messagerie
   └─ create-conversation/    - Créer conversation
```

#### Interface Parent
```
/interfaces/
├─ home/                       - Sélecteur de niveau
├─ parents/
│  └─ home/                   - Tableau de bord parent
├─ maternelle/
│  ├─ dashboard/              - Tableau de bord Maternelle
│  ├─ messenger/              - Messagerie
│  └─ photos/                 - Galerie photos
├─ primaire/
│  ├─ dashboard/              - Tableau de bord Primaire
│  └─ messenger/              - Messagerie
└─ college/
   └─ messenger/              - Messagerie
```

#### API (JSON)
```
/api/
├─ conversations/
│  ├─ list/                   - Liste conversations
│  └─ <id>/messages/          - Messages d'une conversation
└─ posts/
   ├─ create/                 - Créer publication
   └─ <id>/delete/            - Supprimer publication
```

---

## Commandes Management

### 📜 Commandes Disponibles

#### 1. Créer un Administrateur
```bash
python manage.py create_admin
```
**Effet** : Crée un utilisateur directeur avec tous les droits

**Utilisation** : Première installation

---

#### 2. Peupler la Base de Données
```bash
python manage.py populate_db
```
**Effet** :
- Crée 3 niveaux (Maternelle, Primaire, Collège)
- Crée des classes pour chaque niveau
- Crée des professeurs et les assigne aux classes
- Crée des élèves
- Crée des parents et les associe aux élèves
- Crée des publications de test

**Utilisation** : Développement et tests

---

#### 3. Créer les Conversations de Groupe
```bash
python manage.py create_group_conversations
```
**Effet** :
- Pour chaque classe existante :
  - Crée une conversation de type 'group'
  - Ajoute le professeur comme participant
  - Ajoute tous les parents des élèves

**Utilisation** : Après création de classes ou en production

---

#### 4. Configurer les Permissions Directeur
```bash
python manage.py setup_director_permissions
```
**Effet** :
- Configure les permissions Django pour les directeurs
- Donne tous les droits sur tous les modèles

**Utilisation** : Après migration initiale

---

### 🔄 Ordre d'Exécution Recommandé

**Pour une nouvelle installation :**
```bash
# 1. Migrations
python manage.py makemigrations
python manage.py migrate

# 2. Créer admin
python manage.py create_admin

# 3. Configurer permissions
python manage.py setup_director_permissions

# 4. (Optionnel) Peupler pour tests
python manage.py populate_db

# 5. Créer conversations de groupe
python manage.py create_group_conversations

# 6. Lancer serveur
python manage.py runserver
```

---

## Checklist d'Implémentation

### ✅ Phase 1 : Setup Initial
- [x] Installation Django
- [x] Configuration `settings.py`
- [x] Création de la base de données
- [x] Modèles définis
- [x] Migrations créées et appliquées
- [x] Modèle CustomUser configuré
- [x] Commandes management créées

### ✅ Phase 2 : Authentification
- [x] Vue de connexion
- [x] Vue de déconnexion
- [x] Template de login
- [x] Redirection selon rôle
- [x] Gestion des sessions
- [x] Décorateurs de permission

### ✅ Phase 3 : Interface Directeur
- [x] Dashboard admin
- [x] CRUD niveaux scolaires
- [x] CRUD classes
- [x] CRUD élèves
- [x] CRUD utilisateurs
- [x] Association parent-élève
- [x] Assignment professeur-classe

### ✅ Phase 4 : Interface Professeur
- [x] Dashboard professeur
- [x] Vue de la classe
- [x] Messagerie/Messenger
- [x] Publication de contenu
- [x] Création de conversations
- [x] Galerie de photos (Maternelle)

### ✅ Phase 5 : Interface Parent
- [x] Sélecteur de niveau
- [x] Dashboard parent
- [x] Vue des publications
- [x] Messagerie
- [x] Vue des enfants
- [x] Galerie de photos (Maternelle)

### 🔲 Phase 6 : Fonctionnalités Avancées (À faire)
- [ ] Notifications en temps réel (WebSocket)
- [ ] Upload de fichiers (PDF, documents)
- [ ] Recherche avancée
- [ ] Filtres et tri
- [ ] Export PDF
- [ ] API REST complète
- [ ] Tests unitaires
- [ ] Tests d'intégration
- [ ] Documentation API (Swagger)

### 🔲 Phase 7 : Production (À faire)
- [ ] Configuration PostgreSQL
- [ ] Configuration HTTPS
- [ ] Stockage médias (S3/Cloud)
- [ ] Cache (Redis)
- [ ] Monitoring (Sentry)
- [ ] Backup automatique
- [ ] CI/CD
- [ ] Documentation déploiement

---

## Schémas de Données

### 📋 CustomUser
```python
{
    "id": 1,
    "username": "jdupont",
    "email": "jdupont@example.com",
    "first_name": "Jean",
    "last_name": "Dupont",
    "is_parent": true,
    "is_teacher": false,
    "is_director": false,
    "is_active": true,
    "date_joined": "2025-09-01T08:00:00Z"
}
```

### 📋 Classroom
```python
{
    "id": 1,
    "name": "CP A",
    "school_year": "2025-2026",
    "level": {
        "id": 2,
        "name": "Primaire",
        "slug": "primaire"
    },
    "teacher": {
        "id": 5,
        "username": "mmartin",
        "first_name": "Marie",
        "last_name": "Martin"
    },
    "students_count": 25
}
```

### 📋 Student
```python
{
    "id": 1,
    "first_name": "Pierre",
    "last_name": "Dubois",
    "date_of_birth": "2018-05-15",
    "classroom": {
        "id": 1,
        "name": "CP A"
    },
    "parents": [
        {
            "id": 1,
            "username": "jdupont",
            "first_name": "Jean",
            "last_name": "Dupont"
        }
    ],
    "photo": "/media/students/2025/pierre_dubois.jpg"
}
```

### 📋 Conversation
```python
{
    "id": 1,
    "name": "Groupe CP A",
    "conversation_type": "group",
    "classroom": {
        "id": 1,
        "name": "CP A"
    },
    "participants": [
        {"id": 5, "username": "mmartin", "role": "Professeur"},
        {"id": 1, "username": "jdupont", "role": "Parent"},
        {"id": 2, "username": "aleblanc", "role": "Parent"}
    ],
    "created_by": {
        "id": 10,
        "username": "directeur"
    },
    "created_at": "2025-09-01T08:00:00Z",
    "last_message_at": "2026-01-25T14:30:00Z",
    "posts_count": 45
}
```

### 📋 Post
```python
{
    "id": 1,
    "title": "Sortie au musée",
    "description": "Les élèves ont adoré la visite !",
    "image": "/media/posts/2026/01/sortie_musee.jpg",
    "author": {
        "id": 5,
        "username": "mmartin",
        "first_name": "Marie",
        "last_name": "Martin"
    },
    "conversation": {
        "id": 1,
        "name": "Groupe CP A"
    },
    "created_at": "2026-01-25T14:30:00Z",
    "is_published": true
}
```

### 📋 Message
```python
{
    "id": 1,
    "subject": "Question sur les devoirs",
    "content": "Bonjour, je voudrais savoir...",
    "sender": {
        "id": 1,
        "username": "jdupont",
        "first_name": "Jean"
    },
    "recipient": {
        "id": 5,
        "username": "mmartin",
        "first_name": "Marie"
    },
    "created_at": "2026-01-25T10:00:00Z",
    "is_read": false
}
```

---

## Règles de Validation

### CustomUser
- ✅ `username` : unique, 3-150 caractères
- ✅ `email` : format email valide
- ✅ `password` : min 8 caractères (Django default)
- ✅ Si `is_director = True` → `is_staff = True` et `is_teacher = True` (auto)

### Classroom
- ✅ `name` : max 50 caractères, non vide
- ✅ `teacher` : doit avoir `is_teacher = True`
- ✅ `level` : doit exister
- ✅ `school_year` : format "YYYY-YYYY" (9 caractères)

### Student
- ✅ `first_name`, `last_name` : max 50 caractères, non vides
- ✅ `date_of_birth` : date valide, dans le passé
- ✅ `parents` : doivent avoir `is_parent = True`
- ✅ `photo` : formats acceptés (JPG, PNG), max 5 MB

### Conversation
- ✅ `name` : max 200 caractères, non vide
- ✅ `conversation_type` : 'group' ou 'private'
- ✅ Si `type = 'group'` → `classroom` obligatoire
- ✅ `participants` : min 2 participants

### Post
- ✅ Au moins `description` ou `image` obligatoire
- ✅ `image` : formats acceptés (JPG, PNG, GIF), max 10 MB
- ✅ `title` : max 200 caractères

### Message
- ✅ `subject` : max 200 caractères, non vide
- ✅ `content` : non vide
- ✅ `sender` ≠ `recipient`

---

## Requêtes SQL Fréquentes

### Obtenir tous les élèves d'un parent
```python
parent = CustomUser.objects.get(id=1)
students = parent.children.all()
```
```sql
SELECT * FROM school_core_student
INNER JOIN school_core_student_parents
ON school_core_student.id = school_core_student_parents.student_id
WHERE school_core_student_parents.customuser_id = 1;
```

### Obtenir toutes les conversations d'un utilisateur
```python
user = CustomUser.objects.get(id=1)
conversations = user.conversations.all()
```
```sql
SELECT * FROM school_core_conversation
INNER JOIN school_core_conversation_participants
ON school_core_conversation.id = school_core_conversation_participants.conversation_id
WHERE school_core_conversation_participants.customuser_id = 1
ORDER BY last_message_at DESC;
```

### Obtenir toutes les publications d'une conversation
```python
conversation = Conversation.objects.get(id=1)
posts = conversation.posts.filter(is_published=True).order_by('-created_at')
```
```sql
SELECT * FROM school_core_post
WHERE conversation_id = 1 AND is_published = TRUE
ORDER BY created_at DESC;
```

### Obtenir les classes d'un professeur
```python
teacher = CustomUser.objects.get(id=5)
classrooms = teacher.taught_classes.all()
```
```sql
SELECT * FROM school_core_classroom
WHERE teacher_id = 5;
```

### Obtenir les parents d'une classe via les élèves
```python
classroom = Classroom.objects.get(id=1)
parents = CustomUser.objects.filter(
    is_parent=True,
    children__classroom=classroom
).distinct()
```
```sql
SELECT DISTINCT * FROM accounts_customuser
INNER JOIN school_core_student_parents
ON accounts_customuser.id = school_core_student_parents.customuser_id
INNER JOIN school_core_student
ON school_core_student_parents.student_id = school_core_student.id
WHERE accounts_customuser.is_parent = TRUE
AND school_core_student.classroom_id = 1;
```

---

## Performance & Optimisation

### 🚀 N+1 Queries - À éviter

**❌ Mauvais (N+1) :**
```python
classrooms = Classroom.objects.all()
for classroom in classrooms:
    print(classroom.teacher.username)  # 1 query par classe !
```

**✅ Bon (select_related) :**
```python
classrooms = Classroom.objects.select_related('teacher', 'level').all()
for classroom in classrooms:
    print(classroom.teacher.username)  # 1 seule query
```

### 🚀 Préchargement de relations M2M

**❌ Mauvais :**
```python
students = Student.objects.all()
for student in students:
    print(student.parents.count())  # 1 query par élève !
```

**✅ Bon (prefetch_related) :**
```python
students = Student.objects.prefetch_related('parents').all()
for student in students:
    print(student.parents.count())  # 2 queries au total
```

### 🚀 Indexes Recommandés

Ajouter dans les modèles :
```python
class Post(models.Model):
    # ... champs existants ...
    
    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['conversation', '-created_at']),
            models.Index(fields=['is_published', '-created_at']),
        ]

class Message(models.Model):
    # ... champs existants ...
    
    class Meta:
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['-created_at']),
        ]
```

---

## Sécurité

### 🔒 Bonnes Pratiques Implémentées

1. **Authentification** : Django Auth avec sessions sécurisées
2. **CSRF Protection** : Activé sur tous les formulaires
3. **Permissions** : Décorateurs `@login_required`, vérifications de rôle
4. **SQL Injection** : Protection via Django ORM
5. **XSS** : Auto-escape dans les templates Django
6. **Uploads** : Validation des types de fichiers

### 🔒 À Implémenter en Production

```python
# settings.py pour production

# HTTPS obligatoire
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Headers de sécurité
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Limitation upload
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

# Passwords
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

---

## Dépannage

### ❓ Problèmes Courants

#### 1. "No such table: accounts_customuser"
**Solution** : Exécuter les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 2. "Aucune classe assignée" pour un professeur
**Solution** : Vérifier l'assignment dans l'admin
```python
classroom = Classroom.objects.get(id=1)
classroom.teacher = CustomUser.objects.get(id=5)
classroom.save()
```

#### 3. Parent ne voit pas ses enfants
**Solution** : Vérifier la relation M2M
```python
student = Student.objects.get(id=1)
parent = CustomUser.objects.get(id=2)
student.parents.add(parent)
```

#### 4. Images ne s'affichent pas
**Solution** : Configurer MEDIA_URL et MEDIA_ROOT
```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# urls.py (en développement)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Ressources

### 📖 Documentation Complète
- [DOCUMENTATION_BDD.md](DOCUMENTATION_BDD.md) - Structure détaillée de la BDD
- [CAS_UTILISATION.md](CAS_UTILISATION.md) - Tous les cas d'utilisation
- [DIAGRAMMES_UML.md](DIAGRAMMES_UML.md) - Diagrammes UML complets