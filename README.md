# 🎓 AppCaryamil - Plateforme de Gestion Scolaire

Application web complète pour la gestion d'établissements scolaires (Maternelle, Primaire, Collège) avec messagerie instantanée, partage de photos, et panel d'administration avancé.

## ✨ Fonctionnalités Principales

### 👥 Gestion des Utilisateurs
- **Directeurs** : Accès complet au panel d'administration
- **Enseignants** : Gestion de leurs classes et communications avec parents
- **Parents** : Suivi de leurs enfants et réception des actualités

### 💬 Messagerie Unifiée
- Interface type Messenger moderne et responsive
- Conversations de groupe par classe
- Discussions privées personnalisées
- Partage de photos et messages texte
- Liste des participants avec rôles

### 🖼️ Page d'Accueil Parents
- Vue centralisée de toutes les photos reçues
- Statistiques des messages et conversations
- Filtres par conversation et date
- Grille interactive avec aperçu des publications

### 🎛️ Panel d'Administration Personnalisé
- Interface moderne avec sidebar de navigation
- Gestion complète des niveaux, classes et élèves
- Création et édition de professeurs et parents
- Attribution du rôle de directeur
- Assignment automatique des classes aux enseignants
- Liaison des enfants aux comptes parents

## 📁 Structure du Projet

```
AppCaryamil/
│
├── accounts/              # Gestion des utilisateurs
│   ├── models.py         # CustomUser avec is_parent, is_teacher, is_director
│   ├── views.py          # Login/Logout
│   ├── urls.py
│   ├── admin.py          # Configuration admin Django
│   └── templates/
│       └── accounts/
│           └── login.html
│
├── school_core/          # ⭐ CŒUR DE L'APPLICATION - Logique BDD
│   ├── models.py         # TOUS LES MODÈLES :
│   │                     #   - SchoolLevel (Maternelle, Primaire, Collège)
│   │                     #   - Classroom (Classes)
│   │                     #   - Student (Élèves)
│   │                     #   - Conversation (Groupes + Discussions privées)
│   │                     #   - Post (Publications/Photos dans conversations)
│   │                     #   - Message (Messagerie directe)
│   │                     #   - Grade (Notes - pour Collège)
│   ├── admin.py          # Configuration admin Django
│   └── management/
│       └── commands/
│           ├── populate_db.py                 # Données de test
│           ├── create_group_conversations.py  # Conversations de groupe
│           ├── create_admin.py                # Création administrateur
│           └── setup_director_permissions.py  # Permissions directeurs
│
├── interfaces/           # 🎨 VUES ET INTERFACES
│   ├── views_home.py         # Sélection de niveau (avec contrôle d'accès)
│   ├── views_maternelle.py   # Interface Messenger MATERNELLE
│   ├── views_primaire.py     # Interface Messenger PRIMAIRE
│   ├── views_college.py      # Interface Messenger COLLÈGE
│   ├── views_parents.py      # Page d'accueil parents
│   ├── views_admin.py        # 🆕 Panel d'administration personnalisé
│   ├── api_views.py          # API pour chargement dynamique
│   ├── urls.py               # Routes complètes de l'application
│   │
│   └── templates/        # 📱 TEMPLATES PAR SECTION
│       ├── home/
│       │   └── niveau_selector.html  # Sélection avec bouton admin
│       │
│       ├── parents/
│       │   └── home.html             # Vue d'ensemble photos
│       │
│       ├── maternelle/
│       │   ├── dashboard.html        # Tableau de bord
│       │   └── messenger.html        # Interface Messenger
│       │
│       ├── primaire/
│       │   ├── dashboard.html        # Tableau de bord
│       │   └── messenger.html        # Interface Messenger
│       │
│       ├── college/
│       │   └── messenger.html        # Interface Messenger
│       │
│       └── admin/           # 🆕 PANEL D'ADMINISTRATION
│           ├── base.html              # Layout avec sidebar
│           ├── dashboard.html         # Tableau de bord admin
│           ├── levels_list.html       # Liste des niveaux
│           ├── level_edit.html        # Édition niveau
│           ├── classes_list.html      # Liste des classes
│           ├── class_edit.html        # Édition classe
│           ├── students_list.html     # Liste des élèves
│           ├── student_edit.html      # Édition élève
│           ├── teachers_list.html     # Liste des professeurs
│           ├── teacher_edit.html      # Création/édition professeur
│           ├── parents_list.html      # Liste des parents
│           ├── parent_edit.html       # Création/édition parent
│           └── user_detail.html       # Détails utilisateur
│
└── config/               # Configuration Django
    ├── settings.py
    └── urls.py
```

## 🎯 Architecture de l'Application

### 1️⃣ BASE DE DONNÉES UNIFIÉE (`school_core`)
Tous les modèles sont centralisés dans une seule app Django :

- **SchoolLevel** : Maternelle, Primaire, Collège
- **Classroom** : Toutes les classes de tous les niveaux
- **Student** : Tous les élèves (liés à leur classe)
- **Conversation** : Conversations de groupe (classe entière) et discussions privées
- **Post** : Publications/photos dans les conversations
- **Message** : Messagerie directe enseignant ↔ parent
- **Grade** : Système de notes (utilisé pour le Collège)

### 2️⃣ SYSTÈME D'UTILISATEURS
Basé sur `CustomUser` (AbstractUser) avec 3 rôles principaux :

#### 👑 Directeurs (`is_director=True`)
- Automatiquement `is_staff` et `is_teacher`
- Accès complet au panel d'administration personnalisé
- Gestion de tous les niveaux, classes, élèves
- Création et modification de comptes professeurs/parents
- Attribution du rôle de directeur aux enseignants
- Visible dans l'interface avec badge "👑 Directeur"

#### 👨‍🏫 Enseignants (`is_teacher=True`)
- Accès aux classes qui leur sont assignées
- Peuvent être directeurs ou non
- Création de discussions privées avec parents
- Partage de photos et messages dans leurs conversations
- Badge "👨‍🏫 Professeur" dans l'interface

#### 👨‍👩‍👧 Parents (`is_parent=True`)
- Accès aux niveaux où leurs enfants sont inscrits
- Page d'accueil personnalisée avec toutes leurs photos
- Participation aux conversations de classe et discussions privées
- Badge "👨‍👩‍👧 Parent" dans l'interface

### 3️⃣ SYSTÈME DE CONVERSATIONS
Architecture flexible permettant deux types de conversations :

**Conversations de Groupe** 🏫
- Une par classe automatiquement
- Inclut tous les parents des élèves de la classe
- Inclut l'enseignant titulaire
- Badge "Groupe Classe" dans l'interface

**Discussions Privées** 💬
- Créées par les enseignants selon leurs besoins
- Sélection d'élèves spécifiques
- Parents automatiquement ajoutés via leurs enfants
- Badge "Discussion Privée" dans l'interface

**Contenu des Conversations**
- Posts avec photo (optionnelle) et/ou texte
- Timeline chronologique inversée
- Photos cliquables en plein écran
- Liste des participants consultable
- Indicateur de rôle pour chaque participant

### 4️⃣ PANEL D'ADMINISTRATION PERSONNALISÉ
Interface moderne remplaçant le Django admin par défaut :

**Dashboard** 📊
- Vue d'ensemble avec statistiques clés
- Accès rapide aux principales fonctions
- Boutons d'actions rapides (nouveau professeur, parent, etc.)

**Gestion des Niveaux** 📚
- Liste des 3 niveaux (Maternelle, Primaire, Collège)
- Édition des informations (nom, slug, description)
- Comptage des classes par niveau

**Gestion des Classes** 🏫
- Liste complète avec niveau et enseignant
- Création/édition avec :
  - Nom de la classe
  - Niveau scolaire (dropdown)
  - Enseignant assigné (autocomplete)
  - Année scolaire
- Comptage des élèves par classe

**Gestion des Élèves** 👶
- Liste complète avec classe et parents
- Création/édition avec :
  - Informations personnelles (nom, prénom, date de naissance)
  - Classe assignée
  - Sélection des parents (checkboxes multiples)
- Recherche par nom ou classe

**Gestion des Professeurs** 👨‍🏫
- Liste séparée des enseignants
- Création/édition avec :
  - Identifiants de connexion (username, password)
  - Informations personnelles (nom, prénom, email)
  - Case à cocher "Directeur" (accès admin)
  - Assignment des classes enseignées (checkboxes multiples groupées par niveau)
- Badge visuel du statut directeur

**Gestion des Parents** 👨‍👩‍👧
- Liste séparée des parents
- Création/édition avec :
  - Identifiants de connexion (username, password)
  - Informations personnelles (nom, prénom, email)
  - Sélection des enfants (checkboxes avec nom et classe)
- Comptage des enfants par parent

**Navigation** 🧭
- Sidebar permanente avec navigation rapide
- Icônes intuitives pour chaque section
- Design moderne avec dégradés et animations
- Responsive (adapté mobile/tablette)

### 5️⃣ CONTRÔLE D'ACCÈS ET SÉCURITÉ
Système de permissions à plusieurs niveaux :

**Directeurs**
- Accès total au panel d'administration (`/niveaux/administration/`)
- Visibilité de tous les niveaux dans le sélecteur
- Création/modification de tous les comptes
- Gestion complète des données

**Enseignants non-directeurs**
- Accès uniquement aux niveaux où ils enseignent
- Tableau de bord de leurs classes
- Création de discussions privées
- Partage dans leurs conversations

**Parents**
- Accès uniquement aux niveaux de leurs enfants
- Page d'accueil "Mes Photos" personnalisée
- Participation aux conversations les concernant
- Pas d'accès administratif

**Filtrage Automatique**
- Conversations filtrées par participant
- Classes filtrées par niveau/enseignant
- Messages personnalisés selon le rôle
- Redirections selon permissions

## 🚀 Routes Disponibles

### 🔐 Authentification
- `/` - Redirige vers la sélection de niveaux
- `/accounts/login/` - Page de connexion
- `/accounts/logout/` - Déconnexion

### 🏠 Pages Principales
- `/niveaux/` - Sélection du niveau (filtré par accès utilisateur)
- `/niveaux/parents/` - Page d'accueil parents avec toutes leurs photos

### 💬 Interfaces Messenger par Niveau
#### Maternelle
- `/niveaux/maternelle/` - Dashboard et Messenger Maternelle
- `/niveaux/maternelle/create-conversation/` - Créer une discussion privée (enseignants)

#### Primaire
- `/niveaux/primaire/` - Dashboard et Messenger Primaire
- `/niveaux/primaire/create-conversation/` - Créer une discussion privée (enseignants)

#### Collège
- `/niveaux/college/` - Dashboard et Messenger Collège
- `/niveaux/college/create-conversation/` - Créer une discussion privée (enseignants)

### 🎛️ Panel d'Administration (Directeurs uniquement)
- `/niveaux/administration/` - Dashboard administrateur
- `/niveaux/administration/niveaux/` - Gestion des niveaux scolaires
- `/niveaux/administration/niveau/<id>/` - Édition d'un niveau
- `/niveaux/administration/classes/` - Gestion des classes
- `/niveaux/administration/classe/nouveau/` - Création de classe
- `/niveaux/administration/classe/<id>/` - Édition de classe
- `/niveaux/administration/eleves/` - Gestion des élèves
- `/niveaux/administration/eleve/nouveau/` - Création d'élève
- `/niveaux/administration/eleve/<id>/` - Édition d'élève
- `/niveaux/administration/professeurs/` - Gestion des professeurs
- `/niveaux/administration/professeur/nouveau/` - Création de professeur
- `/niveaux/administration/professeur/<id>/` - Édition de professeur
- `/niveaux/administration/parents/` - Gestion des parents
- `/niveaux/administration/parent/nouveau/` - Création de parent
- `/niveaux/administration/parent/<id>/` - Édition de parent
- `/niveaux/administration/utilisateur/<id>/` - Détails d'un utilisateur

### 🔌 API
- `/niveaux/api/classroom/<id>/parents/` - Liste des élèves d'une classe avec nombre de parents (JSON)

### ⚙️ Administration Django (Backup)
- `/admin/` - Interface d'administration Django (disponible mais remplacée par le panel personnalisé)

## 💡 Avantages de cette Architecture

### ✅ Base de données unifiée
- Une seule app pour tous les modèles
- Pas de duplication des données
- Relations cohérentes entre niveaux
- Migrations simplifiées
- Requêtes optimisées

### ✅ Système de rôles flexible
- 3 rôles distincts : Directeur, Enseignant, Parent
- Permissions granulaires par rôle
- Directeurs = enseignants avec privilèges admin
- Assignment automatique des permissions
- Filtrage d'accès transparent

### ✅ Panel d'administration moderne
- Interface personnalisée remplaçant Django admin
- Design moderne avec sidebar et dégradés
- Navigation intuitive avec icônes
- Formulaires optimisés pour chaque entité
- Création rapide de comptes professeurs/parents
- Assignment facile des classes et enfants
- Responsive et accessible

### ✅ Interface Messenger unifiée
- Même expérience pour tous les niveaux
- Messages flexibles (photo, texte, ou les deux)
- Liste des participants visible avec rôles
- Code réutilisable et maintenable
- Facilite la formation des utilisateurs
- Design moderne type Facebook Messenger

### ✅ Système de conversations intelligent
- Groupes automatiques par classe
- Discussions privées à la demande
- Sélection d'élèves (parents auto-ajoutés)
- Partage de photos et messages dans toutes conversations
- Filtrage automatique par participant

### ✅ Page d'accueil parents centralisée
- Toutes les photos en un seul endroit
- Statistiques personnalisées
- Grille interactive avec modal d'aperçu
- Filtres par conversation et date
- Vue claire des informations enfants

### ✅ Contrôle d'accès robuste
- Directeurs : accès total
- Enseignants : leurs niveaux/classes uniquement
- Parents : niveaux de leurs enfants uniquement
- Filtrage automatique des conversations
- Redirections selon permissions
- Liste des participants consultable

### ✅ Évolutif et maintenable
- Architecture modulaire et claire
- Séparation des responsabilités (models/views/templates)
- Facile d'ajouter un nouveau niveau
- Facile d'ajouter des fonctionnalités
- Code documenté et structuré
- Templates réutilisables

## 🛠️ Installation et Configuration

### Prérequis
- Python 3.10+
- Django 6.0.1
- SQLite (base de données par défaut)

### Installation

```bash
# Cloner le projet
git clone <url-du-repo>
cd AppCaryamil

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement (Windows)
.venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur (directeur)
python manage.py createsuperuser

# Remplir la base avec des données de test (optionnel)
python manage.py populate_db

# Créer les conversations de groupe automatiquement
python manage.py create_group_conversations

# Lancer le serveur de développement
python manage.py runserver
```

### Commandes de Gestion

```bash
# Créer des migrations après modification des modèles
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un administrateur/directeur
python manage.py createsuperuser

# Remplir la BDD avec des données de démonstration
python manage.py populate_db

# Créer les conversations de groupe pour toutes les classes
python manage.py create_group_conversations

# Configurer les permissions pour les directeurs
python manage.py setup_director_permissions

# Créer un compte admin rapidement (script personnalisé)
python manage.py create_admin

# Lancer le serveur de développement
python manage.py runserver

# Accéder au shell Django
python manage.py shell

# Collecter les fichiers statiques (production)
python manage.py collectstatic
```

### Configuration Initiale

1. **Créer un directeur** : Première connexion avec le superutilisateur créé
2. **Définir les niveaux** : Maternelle, Primaire, Collège (créés par populate_db)
3. **Créer les classes** : Via le panel d'administration
4. **Ajouter les enseignants** : Panel admin → Professeurs → Nouveau
5. **Ajouter les parents** : Panel admin → Parents → Nouveau
6. **Ajouter les élèves** : Panel admin → Élèves → Nouveau
7. **Lier les parents aux élèves** : Édition d'élève → Sélection des parents
8. **Créer conversations de groupe** : `python manage.py create_group_conversations`

### Accès à l'Application

Une fois le serveur lancé, accéder à :
- **Application** : http://127.0.0.1:8000/
- **Panel Admin Personnalisé** : http://127.0.0.1:8000/niveaux/administration/
- **Django Admin (backup)** : http://127.0.0.1:8000/admin/

## 📊 Modèles de Données Détaillés

### CustomUser (accounts/models.py)
Extension d'AbstractUser avec champs personnalisés :
- **is_parent** : Booléen pour identifier les parents
- **is_teacher** : Booléen pour identifier les enseignants
- **is_director** : Booléen pour identifier les directeurs (auto is_staff)
- **first_name, last_name** : Nom et prénom
- **email** : Adresse email
- **username** : Identifiant de connexion
- **Méthode save()** : Auto-attribution de is_staff et is_teacher si is_director=True
- **Méthode get_role_display()** : Retourne le rôle principal pour affichage

### SchoolLevel (school_core/models.py)
Niveaux scolaires de l'établissement :
- **name** : Nom du niveau (Maternelle, Primaire, Collège)
- **slug** : Pour les URLs (maternelle, primaire, college)
- **description** : Description du niveau

### Classroom (school_core/models.py)
Classes par niveau :
- **level** : ForeignKey vers SchoolLevel
- **name** : Nom de la classe (ex: PS-A, CP-B, 6ème-C)
- **teacher** : ForeignKey vers CustomUser (limit_choices_to={'is_teacher': True})
- **school_year** : Année scolaire (ex: 2025-2026)

### Student (school_core/models.py)
Élèves de l'établissement :
- **first_name, last_name** : Nom et prénom
- **date_of_birth** : Date de naissance
- **classroom** : ForeignKey vers Classroom
- **parents** : ManyToManyField vers CustomUser (limit_choices_to={'is_parent': True})
- **photo** : Photo de l'élève (optionnelle)

### Conversation (school_core/models.py)
Conversations de groupe ou privées :
- **name** : Nom de la conversation
- **conversation_type** : 'group' (classe entière) ou 'private' (discussion privée)
- **classroom** : ForeignKey vers Classroom (optionnelle pour privées)
- **participants** : ManyToManyField vers CustomUser
- **created_by** : ForeignKey vers CustomUser (créateur - enseignant)
- **created_at** : Date de création
- **last_message_at** : Date du dernier message (mise à jour automatique)

### Post (school_core/models.py)
Publications/Photos dans les conversations :
- **author** : ForeignKey vers CustomUser (qui a publié)
- **conversation** : ForeignKey vers Conversation
- **title** : Titre de la publication (optionnel)
- **image** : Photo (optionnelle - blank=True)
- **description** : Description/message texte (obligatoire si pas de photo)
- **created_at** : Date de publication
- **is_published** : Publié ou non

**Note** : Les posts peuvent contenir uniquement du texte, uniquement une photo, ou les deux.

### Message (school_core/models.py)
Messagerie directe enseignant ↔ parent :
- **sender** : ForeignKey vers CustomUser (expéditeur)
- **recipient** : ForeignKey vers CustomUser (destinataire)
- **subject** : Sujet du message
- **content** : Contenu du message
- **created_at** : Date d'envoi
- **is_read** : Lu ou non (booléen)

### Grade (school_core/models.py)
Système de notes (utilisé pour le Collège) :
- **student** : ForeignKey vers Student
- **subject** : Matière (CharField)
- **grade** : Note obtenue (DecimalField)
- **max_grade** : Note maximale (par défaut 20)
- **date** : Date de l'évaluation
- **teacher** : ForeignKey vers CustomUser (enseignant ayant noté)
- **comment** : Commentaire de l'enseignant (optionnel)

## 🎨 Interfaces Utilisateur

### Interface Messenger (Tous Niveaux)
Design unifié pour Maternelle, Primaire et Collège :

**Sidebar (Gauche - 30%)**
- Liste des conversations avec icônes de type
- Badge "🏫 Groupe Classe" ou "💬 Discussion Privée"
- Nom de la conversation
- Nombre de participants (cliquable pour voir la liste)
- Date du dernier message
- Bouton "+" pour créer une discussion (enseignants uniquement)
- Indicateur de conversation active
- Scroll si nombreuses conversations

**Zone Principale (Centre - 70%)**
- **En-tête** :
  - Nom de la conversation
  - Badge du type de conversation
  - "X participants" cliquable → liste déroulante avec rôles
  - Icônes d'identification (enseignant/parent)
  
- **Timeline** :
  - Messages du plus récent au plus ancien
  - Photo de profil de l'auteur (icône enseignant/parent)
  - Nom, rôle et date de publication
  - Photo (si présente) - cliquable pour agrandissement en modal
  - Message texte (si présent)
  - Séparateur entre messages
  - Auto-scroll vers le bas

- **Zone d'Upload (Bas)** :
  - Input file pour sélection de photo (optionnel)
  - Preview de la photo sélectionnée avec taille
  - Champ textarea pour message texte
  - Bouton "Envoyer" activé si photo OU texte présent
  - Messages de validation en temps réel

**Modal Création Discussion** (Enseignants)
- Titre : "Créer une discussion privée"
- Nom de la discussion (champ texte)
- Sélection de classe (dropdown)
- Liste des élèves avec checkboxes (chargement AJAX)
- Indication du nombre de parents par élève
- Bouton "Créer la discussion"
- Messages de succès/erreur

**Modal Agrandissement Photo**
- Photo en plein écran
- Bouton fermeture (X)
- Fond semi-transparent
- Clic à l'extérieur pour fermer

### Page Sélection de Niveaux
**Pour Directeurs** :
- Tous les niveaux visibles (Maternelle, Primaire, Collège)
- Bouton "🎛️ Panel Administrateur" en haut à droite
- Badge "👑 Directeur" sur le nom d'utilisateur

**Pour Enseignants** :
- Uniquement niveaux où ils enseignent
- Badge "👨‍🏫 Professeur" sur le nom

**Pour Parents** :
- Uniquement niveaux de leurs enfants
- Bouton "📸 Mes Photos" pour page d'accueil parents
- Badge "👨‍👩‍👧 Parent" sur le nom

**Cartes de Niveau** :
- Icône du niveau (📚 Maternelle, 🎒 Primaire, 🎓 Collège)
- Nom du niveau
- Description courte
- Effet hover avec élévation
- Dégradé de couleur unique par niveau

### Page d'Accueil Parents

**En-tête**
- Icône famille (👨‍👩‍👧)
- Nom du parent connecté
- Boutons : "🏠 Niveaux" et "🚪 Déconnexion"

**Cartes Statistiques** (3 colonnes)
- 📊 Nombre total de messages reçus
- 💬 Nombre de conversations actives
- 👶 Nombre d'enfants inscrits
- Dégradés de couleur différents
- Icônes grandes et lisibles

**Section Enfants**
- Titre "👶 Mes Enfants"
- Liste horizontale (cartes flexbox)
- Nom de l'enfant
- Badge avec classe et niveau
- Photo de profil (si disponible)

**Grille de Photos** (3 colonnes responsive)
- Cartes pour chaque publication
- **En-tête de carte** :
  - Photo de profil auteur (icône)
  - Nom et rôle de l'auteur
  - Date de publication (format relatif)
- **Badge conversation** : Nom de la conversation
- **Photo** : Image cliquable (si présente)
- **Message** : Texte (si présent)
- Effet hover avec élévation
- Ombres douces pour profondeur

**Modal Aperçu Photo**
- Photo en grand format
- Fond semi-transparent noir
- Fermeture par clic ou bouton X

### Panel d'Administration

**Sidebar (Gauche - Permanente)**
- Logo/Titre "🎛️ Administration"
- Navigation avec icônes :
  - 📊 Dashboard
  - 📚 Niveaux
  - 🏫 Classes
  - 👶 Élèves
  - 👨‍🏫 Professeurs
  - 👨‍👩‍👧 Parents
- Dégradé de fond bleu/violet
- Icônes blanches
- Item actif surligné
- Section déconnexion en bas

**Zone Principale (Droite)**
- **En-tête** : Titre de la page avec icône
- **Barre d'actions** : Recherche + bouton "Nouveau"
- **Tableau/Grille** : Liste des éléments
- **Pagination** : Si nombreux éléments
- **Boutons d'action** : Éditer, Supprimer (avec confirmations)

**Formulaires d'Édition**
- Layout à deux colonnes (desktop)
- Labels clairs avec icônes
- Champs groupés logiquement
- Dropdowns pour sélections simples
- Checkboxes groupées pour multi-sélection (classes, enfants)
- Messages de validation en temps réel
- Boutons "Enregistrer" et "Annuler"
- Breadcrumb pour navigation

**Dashboard Admin**
- Cartes statistiques (4 colonnes)
- Compteurs animés
- Dégradés de couleur uniques
- Icônes grandes et expressives
- Section "Actions Rapides" avec boutons principaux
- Liste des activités récentes (optionnel)

## 👥 Comptes de Démonstration

Après avoir exécuté `python manage.py populate_db`, les comptes suivants sont disponibles :

### 👑 Directeur de Test
- **Username**: directeur_test
- **Password**: test123
- **Rôle**: Directeur (is_director=True, is_staff=True, is_teacher=True)
- **Accès**: 
  - Panel d'administration complet (`/niveaux/administration/`)
  - Tous les niveaux scolaires
  - Gestion de tous les utilisateurs, classes, élèves
  - Création de professeurs et parents
  - Attribution du rôle de directeur

### 👨‍🏫 Enseignante Maternelle
- **Username**: marie.dubois
- **Password**: prof123
- **Rôle**: Enseignante (is_teacher=True)
- **Classes**: Petite Section A, Grande Section C (Maternelle)
- **Accès**: 
  - Dashboard Maternelle
  - Conversations de groupe de ses classes
  - Création de discussions privées
  - Partage de photos et messages texte
  - Liste des participants de ses conversations

### 👨‍🏫 Enseignant Primaire
- **Username**: jean.martin
- **Password**: prof123
- **Rôle**: Enseignant (is_teacher=True)
- **Classes**: Moyenne Section B (Maternelle)
- **Accès**: 
  - Dashboard de ses niveaux
  - Conversations de ses classes
  - Création de discussions privées
  - Partage dans ses conversations

### 👨‍👩‍👧 Parent
- **Username**: amelie.dupont
- **Password**: parent123
- **Rôle**: Parent (is_parent=True)
- **Enfants**: 
  - Léa Dupont (Petite Section A - Maternelle)
  - Jade Dupont (CE1 B - Primaire)
  - Léonie Dupont (6ème A - Collège)
- **Accès**: 
  - Page "Mes Photos" (`/niveaux/parents/`)
  - Niveaux Maternelle, Primaire, Collège
  - Conversations de groupe des classes de ses enfants
  - Discussions privées le concernant
  - Partage de photos et messages

### 🔐 Administrateur Django
- **Username**: admin
- **Password**: (défini lors de createsuperuser)
- **Accès**: Interface Django admin (`/admin/`) et panel personnalisé

## 🔐 Sécurité et Permissions

### Authentification
- **Login requis** : Toutes les vues sont protégées par `@login_required`
- **Sessions Django** : Gestion sécurisée des sessions utilisateurs
- **CSRF Protection** : Tokens CSRF sur tous les formulaires
- **Passwords hachés** : Utilisation de `set_password()` pour le hachage

### Permissions par Rôle

#### 👑 Directeurs
- Accès complet au panel d'administration (`user_is_admin()`)
- Visibilité de tous les niveaux dans le sélecteur
- CRUD complet sur tous les modèles
- Création de comptes professeurs avec option "Directeur"
- Création de comptes parents avec liaison aux enfants
- Assignment des classes aux enseignants
- Permissions Django admin automatiques (is_staff=True)

#### 👨‍🏫 Enseignants
- Accès uniquement aux niveaux où ils enseignent
- Dashboards de leurs classes
- Création de discussions privées (sélection d'élèves)
- Partage de photos et messages dans leurs conversations
- Vue de la liste des participants
- Pas d'accès au panel d'administration (sauf si directeur)

#### 👨‍👩‍👧 Parents
- Accès uniquement aux niveaux de leurs enfants
- Page "Mes Photos" personnalisée avec leurs publications
- Participation aux conversations les concernant
- Partage dans leurs conversations
- Vue de la liste des participants
- Aucun accès administratif

### Filtrage Automatique

**Conversations**
- Filtrées par `request.user` dans `participants`
- Seules les conversations pertinentes sont affichées
- Redirection si accès non autorisé

**Classes**
- Enseignants : uniquement leurs classes assignées
- Directeurs : toutes les classes
- Parents : classes de leurs enfants uniquement

**Niveaux**
- Enseignants : niveaux où ils enseignent
- Directeurs : tous les niveaux
- Parents : niveaux de leurs enfants

**Panel d'Administration**
- Contrôle via `user_is_admin()` helper
- Redirection automatique vers `/niveaux/` si non autorisé
- Vérification sur toutes les vues admin

### Validation des Données

**Formulaires**
- Validation côté serveur (Django forms)
- Validation côté client (HTML5 required, patterns)
- Messages d'erreur explicites
- Prévention des doublons (contraintes BDD)

**Upload de Fichiers**
- Validation du type MIME
- Limite de taille (configurée dans settings)
- Stockage sécurisé dans MEDIA_ROOT
- Nommage unique des fichiers

### Bonnes Pratiques

- **Séparation des rôles** : Un utilisateur = un rôle principal (avec exceptions pour directeurs)
- **Principe du moindre privilège** : Accès minimal nécessaire
- **Traçabilité** : Tous les posts/messages ont un auteur
- **Intégrité des données** : Contraintes de clés étrangères
- **Messages utilisateur** : Retours clairs sur les actions (succès/erreur)

## 🆕 Fonctionnalités Principales

### 🎛️ Panel d'Administration Personnalisé
Interface moderne remplaçant le Django admin :
- **Design moderne** : Sidebar avec dégradés, icônes intuitives
- **Dashboard** : Vue d'ensemble avec statistiques clés
- **Gestion complète** : Niveaux, Classes, Élèves, Professeurs, Parents
- **Création de comptes** : Formulaires optimisés pour professeurs et parents
- **Assignment rapide** : Classes aux enseignants, enfants aux parents
- **Rôle directeur** : Case à cocher pour donner accès admin
- **Responsive** : Adapté mobile, tablette, desktop
- **Navigation intuitive** : Sidebar permanente avec icônes

### 💬 Système de Messagerie Moderne
Interface type Facebook Messenger :
- **Deux types de conversations** : Groupe (classe entière) et Privée (sélection d'élèves)
- **Messages flexibles** : Photo seule, texte seul, ou les deux
- **Upload avec preview** : Aperçu instantané avant envoi
- **Timeline chronologique** : Messages triés du plus récent au plus ancien
- **Photos cliquables** : Modal plein écran pour agrandissement
- **Liste des participants** : Déroulant avec rôles (enseignant/parent)
- **Badges intuitifs** : Icônes pour différencier groupe/privé
- **Auto-scroll** : Défilement automatique vers nouveaux messages

### 🖼️ Page d'Accueil Parents
Vue centralisée de toutes les publications :
- **Statistiques personnalisées** : Messages, conversations, enfants
- **Grille interactive** : Toutes les photos reçues dans toutes conversations
- **Cartes détaillées** : Auteur, date, conversation, photo, message
- **Modal d'aperçu** : Agrandissement des photos en un clic
- **Informations enfants** : Liste avec classe et niveau
- **Design moderne** : Layout responsive avec badges colorés

### 👥 Gestion des Rôles
Système flexible à trois niveaux :
- **Directeurs** : Accès total administration, toutes classes/niveaux
- **Enseignants** : Gestion de leurs classes, création discussions privées
- **Parents** : Suivi de leurs enfants, réception actualités
- **Assignment automatique** : is_staff auto pour directeurs
- **Badges visuels** : Identification rapide du rôle dans l'interface

### 🔒 Contrôle d'Accès Granulaire
Filtrage automatique selon le rôle :
- **Niveaux visibles** : Selon classes enseignées ou enfants inscrits
- **Conversations filtrées** : Uniquement celles où l'utilisateur participe
- **Panel admin** : Réservé aux directeurs uniquement
- **Redirections intelligentes** : Selon permissions de l'utilisateur
- **Messages contextuels** : Explications claires des restrictions

### 📱 Interface Responsive
Design adaptatif pour tous les écrans :
- **Mobile-first** : Optimisé pour smartphones
- **Tablette** : Layout ajusté pour tablettes
- **Desktop** : Interface complète avec sidebar
- **Sidebar escamotable** : Navigation adaptée selon la taille d'écran
- **Grilles flexibles** : Photos et cartes s'adaptent automatiquement

### 🎨 Design Moderne
Interface visuelle attractive :
- **Dégradés colorés** : Différenciation visuelle des sections
- **Icônes intuitives** : Émojis et icônes FontAwesome
- **Badges colorés** : Identification rapide des rôles et types
- **Animations** : Transitions fluides et effets hover
- **Typographie** : Police Inter pour lisibilité optimale
- **Couleurs cohérentes** : Palette harmonieuse à travers l'app
