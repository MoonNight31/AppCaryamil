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

## 🎯 Principe de l'Architecture

### 1️⃣ UNE SEULE BASE DE DONNÉES (`school_core`)
- **SchoolLevel** : Maternelle, Primaire, Collège
- **Classroom** : Toutes les classes de tous les niveaux
- **Student** : Tous les élèves (avec `classroom.level` pour savoir le niveau)
- **Conversation** : Conversations de groupe (classe entière) et discussions privées (enseignant + parents sélectionnés)
- **Post** : Publications/photos dans les conversations
- **Message** : Messagerie directe enseignant ↔ parent

### 2️⃣ SYSTÈME DE CONVERSATIONS
- **Conversations de groupe** : Une par classe, inclut tous les parents + l'enseignant
- **Discussions privées** : Créées par les enseignants en sélectionnant des élèves (leurs parents sont automatiquement ajoutés)
- **Posts** : Photos et messages texte partagés dans les conversations
- **Messages flexibles** : Possibilité d'envoyer des messages avec photo, texte seul, ou les deux
- **Liste des participants** : Affichage déroulant de tous les participants d'une conversation avec leur rôle
- **Filtrage** : Chaque utilisateur ne voit que ses conversations

### 3️⃣ INTERFACE MESSENGER UNIFIÉE
Tous les niveaux utilisent la même interface Messenger :
- Sidebar avec liste des conversations (groupe/privé)
- Zone de chat avec timeline des photos et messages
- Upload de photos avec preview (optionnel)
- Messages texte seuls sans photo
- Liste déroulante des participants (cliquable depuis le header)
- Modal pour créer des discussions privées (enseignants - sélection d'élèves)
- Design moderne type Facebook Messenger

### 4️⃣ PAGE D'ACCUEIL PARENTS
Interface dédiée aux parents pour voir toutes leurs photos :
- Vue d'ensemble avec statistiques (messages, conversations, enfants)
- Grille de toutes les photos reçues dans toutes les conversations
- Filtres par conversation et date
- Photos cliquables en grand format
- Information sur l'auteur et la date de chaque publication

## 🚀 URLs Disponibles

### Authentification
- `/` - Redirige vers la sélection de niveaux
- `/accounts/login/` - Page de connexion
- `/accounts/logout/` - Déconnexion

### Sélection de niveau
- `/niveaux/` - Sélection du niveau (filtré par accès utilisateur)

### Page d'accueil Parents
- `/niveaux/parents/` - Vue d'ensemble de toutes les photos reçues

### Interfaces Messenger par niveau
- `/niveaux/maternelle/` - Messenger Maternelle
- `/niveaux/maternelle/create-conversation/` - Créer une discussion privée (enseignants)
- `/niveaux/primaire/` - Messenger Primaire
- `/niveaux/primaire/create-conversation/` - Créer une discussion privée (enseignants)
- `/niveaux/college/` - Messenger Collège
- `/niveaux/college/create-conversation/` - Créer une discussion privée (enseignants)

### API
- `/niveaux/api/classroom/<id>/parents/` - Liste des élèves d'une classe avec nombre de parents (JSON)

### Administration
- `/admin/` - Interface d'administration Django

## 💡 Avantages de cette Architecture

### ✅ Base de données unique
- Pas de duplication des données
- Relations cohérentes entre niveaux
- Migrations simplifiées

### ✅ Interface unifiée
- Même expérience Messenger pour tous les niveaux
- Messages flexibles (photo, texte, ou les deux)
- Liste des participants visible dans chaque conversation
- Code réutilisable et maintenable
- Facilite la formation des utilisateurs

### ✅ Système de conversations flexible
- Groupes automatiques par classe
- Discussions privées à la demande (sélection d'élèves)
- Partage de photos et messages texte dans toutes les conversations
- Parents automatiquement ajoutés via leurs enfants

### ✅ Contrôle d'accès
- Parents : accès uniquement aux niveaux de leurs enfants + page d'accueil avec toutes leurs photos
- Enseignants : accès uniquement aux niveaux qu'ils enseignent
- Filtrage automatique des conversations
- Liste des participants visible avec rôles (enseignant/parent)

### ✅ Évolutif
- Facile d'ajouter un nouveau niveau
- Facile d'ajouter des fonctionnalités
- Architecture modulaire et claire

## 🛠️ Commandes Utiles

```bash
# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Remplir la base de données avec des données de test
python manage.py populate_db

# Créer les conversations de groupe automatiquement
python manage.py create_group_conversations

# Lancer le serveur
python manage.py runserver
```

## 📊 Modèles de Données

### SchoolLevel (Niveau)
- name: Nom du niveau (Maternelle, Primaire, Collège)
- slug: Pour les URLs (maternelle, primaire, college)
- description: Description du niveau

### Classroom (Classe)
- level: Lien vers SchoolLevel
- name: Nom de la classe (ex: PS-A, CP-B, 6ème-C)
- teacher: Enseignant assigné
- school_year: Année scolaire

### Student (Élève)
- first_name, last_name: Nom et prénom
- date_of_birth: Date de naissance
- classroom: Classe actuelle
- parents: Liens vers les comptes parents (ManyToMany)
- photo: Photo de l'élève

### Conversation (Groupe ou Discussion privée)
- name: Nom de la conversation
- conversation_type: 'group' (classe entière) ou 'private' (discussion privée)
- classroom: Classe associée
- participants: Utilisateurs participants (ManyToMany)
- created_by: Créateur (enseignant)
- created_at: Date de création
- last_message_at: Date du dernier message

### Post (Publication/Photo)
- author: Qui a publié
- conversation: Conversation associée
- title: Titre (optionnel)
- image: Photo (optionnelle - blank=True)
- description: Description/message texte
- created_at: Date de publication
- is_published: Publié ou non

**Note** : Les posts peuvent contenir uniquement du texte, uniquement une photo, ou les deux.

### Message (Messagerie directe)
- sender: Expéditeur
- recipient: Destinataire
- subject: Sujet
- content: Contenu
- created_at: Date d'envoi
- is_read: Lu ou non

## 🎨 Interface Messenger

### Design Unifié
Tous les niveaux (Maternelle, Primaire, Collège) partagent la même interface :

**Sidebar (Gauche)**
- Liste des conversations avec icônes
- Badge "Groupe Classe" ou "Discussion Privée"
- Nombre de participants (cliquable pour voir la liste)
- Date du dernier message
- Bouton "+" pour créer une discussion (enseignants)

**Zone Principale (Centre)**
- En-tête avec nom de la conversation et participants
- Clic sur "X participants" pour voir la liste déroulante avec rôles
- Timeline des photos et messages partagés
- Icône enseignant/parent pour identifier l'auteur
- Photos cliquables avec modal en plein écran
- Messages texte avec ou sans photo

**Zone d'Upload (Bas)**
- Preview de la photo avant envoi (optionnel)
- Champ de message texte (requis si pas de photo)
- Bouton d'envoi activé si texte OU photo présent
- Indication de la taille du fichier

**Fonctionnalités**
- Auto-scroll vers le bas de la conversation
- Upload de photos avec preview instantané (optionnel)
- Envoi de messages texte seuls sans photo
- Modal pour créer des discussions privées (enseignants)
- Chargement dynamique des élèves par classe (AJAX)
- Sélection d'élèves (leurs parents sont auto-ajoutés)
- Liste déroulante des participants avec icônes et rôles
- Messages de succès/erreur avec Django messages

## 🏠 Page d'Accueil Parents

### Vue d'Ensemble
Page dédiée aux parents pour centraliser toutes leurs photos :

**En-tête**
- Icône famille et nom du parent
- Boutons "Niveaux" et "Déconnexion"

**Cartes Statistiques**
- Nombre total de messages reçus
- Nombre de conversations actives
- Nombre d'enfants inscrits

**Section Enfants**
- Liste des enfants avec leurs classes respectives
- Badges colorés avec niveau scolaire

**Grille de Photos**
- Toutes les photos/messages de toutes les conversations
- Carte par publication avec :
  - Photo de l'auteur (enseignant/parent)
  - Nom et date de publication
  - Badge de la conversation
  - Photo (si présente)
  - Message texte (si présent)
- Clic sur photo pour agrandissement en modal

**Accès**
- Bouton "📸 Mes Photos" sur la page de sélection des niveaux
- URL : `/niveaux/parents/`

## 👥 Comptes de Démonstration

### Enseignante
- **Username**: marie.dubois
- **Password**: prof123
- **Accès**: Maternelle (PS-A, MS-A)
- **Fonctions**: 
  - Voir toutes conversations de ses classes
  - Créer discussions privées en sélectionnant des élèves
  - Partager photos et messages texte
  - Voir la liste complète des participants avec leurs rôles

### Parent
- **Username**: amelie.dupont
- **Password**: parent123
- **Accès**: Maternelle (enfant: Léo Dupont en PS-A)
- **Fonctions**: 
  - Voir conversations de la classe de son enfant
  - Partager photos et messages
  - Accès à la page "Mes Photos" avec toutes les publications reçues
  - Voir la liste des participants de chaque conversation

## 🔐 Sécurité et Permissions

- Login requis pour toutes les vues (`@login_required`)
- Parents : 
  - Accès uniquement aux niveaux où ils ont des enfants inscrits
  - Page "Mes Photos" personnalisée avec leurs publications
  - Visualisation des participants de leurs conversations
- Enseignants : 
  - Accès uniquement aux niveaux où ils enseignent
  - Création de discussions privées réservée aux enseignants
  - Sélection d'élèves (leurs parents sont auto-invités)
- Conversations : filtrées automatiquement par participant
- Upload de photos : tous les participants d'une conversation
- Messages texte : possibilité d'envoyer sans photo

## 🆕 Fonctionnalités Récentes

### Messages Texte Sans Photo
- Les utilisateurs peuvent envoyer des messages texte seuls
- Le bouton d'envoi s'active si texte OU photo est présent
- Champ photo devenu optionnel dans le formulaire

### Liste des Participants
- Clic sur "X participants" dans le header de conversation
- Affichage déroulant avec icônes et rôles
- Fermeture automatique en cliquant à l'extérieur

### Création de Discussions par Élèves
- Les enseignants sélectionnent des élèves (non plus des parents)
- Les parents des élèves sélectionnés sont automatiquement ajoutés
- Affichage du nombre de parents par élève dans la sélection

### Page d'Accueil Parents
- Vue centralisée de toutes les photos/messages reçus
- Statistiques : messages, conversations, enfants
- Grille de cartes avec photos et informations
- Accès direct depuis le bouton "📸 Mes Photos"
