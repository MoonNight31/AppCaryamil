# Documentation de la Base de Données - AppCaryamil

## Vue d'ensemble

Cette application Django gère un système de communication scolaire pour une école avec trois niveaux : Maternelle, Primaire et Collège. Elle permet aux enseignants, parents et directeurs de communiquer et de partager du contenu.

## Architecture des Modèles

### 1. Module Accounts

#### CustomUser
Modèle personnalisé d'authentification basé sur `AbstractUser`.

**Champs :**
- Hérite de tous les champs de `AbstractUser` (username, email, password, etc.)
- `is_parent` (Boolean) : Indique si l'utilisateur est un parent
- `is_teacher` (Boolean) : Indique si l'utilisateur est un professeur
- `is_director` (Boolean) : Indique si l'utilisateur est un directeur

**Logique métier :**
- Un directeur devient automatiquement `is_staff = True` et `is_teacher = True`
- Un utilisateur peut avoir plusieurs rôles simultanément
- Méthode `get_role_display()` pour afficher les rôles de manière lisible

**Relations :**
- Un utilisateur peut être parent de plusieurs élèves (via `Student.parents`)
- Un utilisateur peut enseigner plusieurs classes (via `Classroom.teacher`)
- Un utilisateur peut participer à plusieurs conversations
- Un utilisateur peut créer des publications et messages

---

### 2. Module School_Core

#### SchoolLevel (Niveau Scolaire)
Représente les niveaux d'enseignement (Maternelle, Primaire, Collège).

**Champs :**
- `name` (CharField, 50, unique) : Nom du niveau
- `slug` (SlugField, unique) : Identifiant URL
- `description` (TextField) : Description optionnelle

**Relations :**
- Un niveau possède plusieurs classes (1:N avec Classroom)

---

#### Classroom (Classe)
Représente une classe au sein d'un niveau scolaire.

**Champs :**
- `level` (ForeignKey → SchoolLevel) : Niveau scolaire de la classe
- `name` (CharField, 50) : Nom de la classe (ex: "CP A", "CE1 B")
- `teacher` (ForeignKey → CustomUser, nullable) : Professeur principal
- `school_year` (CharField, 9) : Année scolaire (défaut: "2025-2026")

**Relations :**
- Appartient à un niveau (N:1 avec SchoolLevel)
- A un professeur principal (N:1 avec CustomUser)
- Contient plusieurs élèves (1:N avec Student)
- Possède plusieurs conversations de groupe (1:N avec Conversation)

---

#### Student (Élève)
Représente un élève de l'école.

**Champs :**
- `first_name` (CharField, 50) : Prénom
- `last_name` (CharField, 50) : Nom
- `date_of_birth` (DateField, nullable) : Date de naissance
- `classroom` (ForeignKey → Classroom, nullable) : Classe actuelle
- `parents` (ManyToManyField → CustomUser) : Parents de l'élève
- `photo` (ImageField) : Photo de profil

**Relations :**
- Appartient à une classe (N:1 avec Classroom)
- A plusieurs parents (N:N avec CustomUser)

---

#### Conversation
Représente une discussion, soit de groupe (classe entière), soit privée (entre utilisateurs).

**Champs :**
- `name` (CharField, 200) : Nom de la conversation
- `conversation_type` (CharField, choices) : 'group' ou 'private'
- `classroom` (ForeignKey → Classroom, nullable) : Classe associée (pour groupes)
- `participants` (ManyToManyField → CustomUser) : Utilisateurs participants
- `created_by` (ForeignKey → CustomUser, nullable) : Créateur
- `created_at` (DateTimeField) : Date de création
- `last_message_at` (DateTimeField) : Date du dernier message

**Relations :**
- Peut être liée à une classe (N:1 avec Classroom)
- A plusieurs participants (N:N avec CustomUser)
- A un créateur (N:1 avec CustomUser)
- Contient plusieurs publications (1:N avec Post)

**Logique métier :**
- Méthode `get_last_message()` pour récupérer le dernier message

---

#### Post (Publication)
Représente une publication (photo, message) dans une conversation.

**Champs :**
- `author` (ForeignKey → CustomUser) : Auteur de la publication
- `conversation` (ForeignKey → Conversation, nullable) : Conversation associée
- `classroom` (ForeignKey → Classroom, nullable) : *Déprécié* - pour compatibilité
- `title` (CharField, 200) : Titre optionnel
- `image` (ImageField) : Photo optionnelle
- `description` (TextField) : Contenu/description
- `created_at` (DateTimeField) : Date de publication
- `is_published` (Boolean) : Statut de publication

**Relations :**
- A un auteur (N:1 avec CustomUser)
- Appartient à une conversation (N:1 avec Conversation)

---

#### Message
Représente un message direct entre deux utilisateurs (système de messagerie privée).

**Champs :**
- `sender` (ForeignKey → CustomUser) : Expéditeur
- `recipient` (ForeignKey → CustomUser) : Destinataire
- `subject` (CharField, 200) : Sujet du message
- `content` (TextField) : Contenu du message
- `created_at` (DateTimeField) : Date d'envoi
- `is_read` (Boolean) : Statut de lecture

**Relations :**
- A un expéditeur (N:1 avec CustomUser)
- A un destinataire (N:1 avec CustomUser)

---

## Diagramme de Relations (ERD)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CustomUser                                 │
│  (hérite de AbstractUser)                                           │
├─────────────────────────────────────────────────────────────────────┤
│ - username (unique)                                                 │
│ - email                                                             │
│ - password                                                          │
│ - is_parent : Boolean                                               │
│ - is_teacher : Boolean                                              │
│ - is_director : Boolean                                             │
│ - is_staff : Boolean (auto si director)                             │
└─────────────────────────────────────────────────────────────────────┘
         │                    │                    │
         │ teacher (0..*)     │ parents (N:N)      │ participants (N:N)
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────────┐   ┌──────────────┐   ┌──────────────────┐
│   Classroom      │   │   Student    │   │  Conversation    │
├──────────────────┤   ├──────────────┤   ├──────────────────┤
│ - name           │   │ - first_name │   │ - name           │
│ - school_year    │◄──┤ - last_name  │   │ - type (choice)  │
│ - teacher (FK)   │   │ - birth_date │   │ - created_at     │
│ - level (FK)     │   │ - photo      │   │ - last_msg_at    │
└──────────────────┘   │ - classroom  │   │ - classroom (FK) │
         ▲             │ - parents    │   │ - created_by (FK)│
         │             └──────────────┘   │ - participants   │
         │                                └──────────────────┘
         │ level (FK)                             │
         │                                        │ conversation (FK)
┌──────────────────┐                              ▼
│  SchoolLevel     │                     ┌──────────────────┐
├──────────────────┤                     │      Post        │
│ - name (unique)  │                     ├──────────────────┤
│ - slug (unique)  │                     │ - title          │
│ - description    │                     │ - image          │
└──────────────────┘                     │ - description    │
                                         │ - created_at     │
                                         │ - is_published   │
                                         │ - author (FK)    │
                                         │ - conversation   │
                                         └──────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    Message (Messagerie privée)                      │
├─────────────────────────────────────────────────────────────────────┤
│ - subject                                                           │
│ - content                                                           │
│ - created_at                                                        │
│ - is_read                                                           │
│ - sender (FK → CustomUser)                                          │
│ - recipient (FK → CustomUser)                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Légende :
- **FK** : Foreign Key (Clé étrangère)
- **N:N** : Relation Many-to-Many
- **1:N** : Relation One-to-Many
- **▼** : Direction de la relation

---

## Relations Détaillées

### Relations CustomUser

| Relation | Type | Description |
|----------|------|-------------|
| `taught_classes` | 1:N | Classes enseignées par le professeur |
| `children` | N:N | Élèves dont l'utilisateur est parent |
| `conversations` | N:N | Conversations auxquelles l'utilisateur participe |
| `created_conversations` | 1:N | Conversations créées par l'utilisateur |
| `sent_messages` | 1:N | Messages envoyés |
| `received_messages` | 1:N | Messages reçus |

### Relations SchoolLevel

| Relation | Type | Description |
|----------|------|-------------|
| `classrooms` | 1:N | Classes appartenant au niveau |

### Relations Classroom

| Relation | Type | Description |
|----------|------|-------------|
| `level` | N:1 | Niveau scolaire de la classe |
| `teacher` | N:1 | Professeur principal |
| `students` | 1:N | Élèves de la classe |
| `conversations` | 1:N | Conversations de groupe de la classe |

### Relations Student

| Relation | Type | Description |
|----------|------|-------------|
| `classroom` | N:1 | Classe actuelle de l'élève |
| `parents` | N:N | Parents de l'élève |

### Relations Conversation

| Relation | Type | Description |
|----------|------|-------------|
| `classroom` | N:1 | Classe associée (si groupe) |
| `participants` | N:N | Utilisateurs participants |
| `created_by` | N:1 | Créateur de la conversation |
| `posts` | 1:N | Publications dans la conversation |

### Relations Post

| Relation | Type | Description |
|----------|------|-------------|
| `author` | N:1 | Auteur de la publication |
| `conversation` | N:1 | Conversation associée |

### Relations Message

| Relation | Type | Description |
|----------|------|-------------|
| `sender` | N:1 | Expéditeur du message |
| `recipient` | N:1 | Destinataire du message |

---

## Types de Données et Contraintes

### CustomUser
- **Contraintes** :
  - `username` doit être unique
  - Si `is_director = True`, alors `is_staff = True` et `is_teacher = True`

### SchoolLevel
- **Contraintes** :
  - `name` et `slug` doivent être uniques

### Classroom
- **Contraintes** :
  - `teacher` doit avoir `is_teacher = True`

### Student
- **Contraintes** :
  - Les `parents` doivent avoir `is_parent = True`

### Conversation
- **Choix pour `conversation_type`** :
  - `'group'` : Groupe Classe
  - `'private'` : Discussion Privée

### Post
- **Uploads** :
  - Images stockées dans `media/posts/{year}/{month}/`

### Message
- **Contraintes** :
  - `sender` et `recipient` doivent être différents (logique à implémenter)

---

## Indexes et Performances

### Indexes automatiques créés par Django :
- Toutes les ForeignKey créent automatiquement un index
- Les champs `unique=True` ont un index unique

### Optimisations recommandées :
```python
# Dans les modèles, ajouter des indexes pour les requêtes fréquentes
class Meta:
    indexes = [
        models.Index(fields=['-created_at']),  # Pour Post et Message
        models.Index(fields=['is_read', '-created_at']),  # Pour Message
        models.Index(fields=['-last_message_at']),  # Pour Conversation
    ]
```

---

## Migrations

### Migrations importantes :
1. **0001_initial.py** : Création initiale des modèles
2. **0002_alter_post_classroom_alter_post_image_conversation_and_more.py** : 
   - Ajout du modèle Conversation
   - Migration de la logique de Post vers les Conversations
3. **0003_remove_grades.py** : Suppression du modèle Grades

---

## Commandes de gestion personnalisées

L'application inclut plusieurs commandes Django personnalisées dans `school_core/management/commands/` :

1. **`create_admin.py`** : Créer un utilisateur administrateur
2. **`create_group_conversations.py`** : Créer des conversations de groupe pour toutes les classes
3. **`populate_db.py`** : Peupler la base avec des données de test
4. **`setup_director_permissions.py`** : Configurer les permissions pour les directeurs

### Utilisation :
```bash
python manage.py create_admin
python manage.py create_group_conversations
python manage.py populate_db
python manage.py setup_director_permissions
```

---

## Diagramme de Classes UML

```
@startuml
class CustomUser {
  +username: str
  +email: str
  +is_parent: bool
  +is_teacher: bool
  +is_director: bool
  +get_role_display(): str
}

class SchoolLevel {
  +name: str
  +slug: str
  +description: str
}

class Classroom {
  +name: str
  +school_year: str
  +level: SchoolLevel
  +teacher: CustomUser
}

class Student {
  +first_name: str
  +last_name: str
  +date_of_birth: date
  +photo: ImageField
  +classroom: Classroom
}

class Conversation {
  +name: str
  +conversation_type: str
  +created_at: datetime
  +last_message_at: datetime
  +get_last_message(): Post
}

class Post {
  +title: str
  +image: ImageField
  +description: str
  +created_at: datetime
  +is_published: bool
}

class Message {
  +subject: str
  +content: str
  +created_at: datetime
  +is_read: bool
}

SchoolLevel "1" -- "*" Classroom : contains
Classroom "*" -- "1" CustomUser : taught by
Classroom "1" -- "*" Student : has
Student "*" -- "*" CustomUser : parents
Classroom "1" -- "*" Conversation : has
Conversation "*" -- "*" CustomUser : participants
Conversation "1" -- "*" Post : contains
Post "*" -- "1" CustomUser : authored by
Message "*" -- "1" CustomUser : sent by
Message "*" -- "1" CustomUser : received by
@enduml
```

---

## Données d'exemple

### Niveaux scolaires typiques :
- **Maternelle** (slug: `maternelle`)
- **Primaire** (slug: `primaire`)
- **Collège** (slug: `college`)

### Classes typiques :
- Maternelle : "Petite Section A", "Moyenne Section B", "Grande Section"
- Primaire : "CP A", "CE1 B", "CE2", "CM1", "CM2"
- Collège : "6ème A", "5ème B", "4ème", "3ème"

---

## Considérations de sécurité

1. **Permissions** :
   - Les directeurs ont accès à tout (`is_staff = True`)
   - Les professeurs peuvent gérer leurs classes
   - Les parents ne voient que les infos de leurs enfants

2. **Validation** :
   - `limit_choices_to` utilisé pour contraindre les ForeignKey
   - Les rôles sont vérifiés au niveau du modèle

3. **Données sensibles** :
   - Photos stockées séparément dans `media/`
   - Dates de naissance des élèves (RGPD)