# Cas d'Utilisation - AppCaryamil

## Vue d'ensemble

Ce document décrit les cas d'utilisation de l'application AppCaryamil, un système de gestion et de communication scolaire pour une école avec trois niveaux : Maternelle, Primaire et Collège.

---

## Acteurs du système

### 1. Directeur
- Rôle : Administration complète de l'école
- Permissions : Accès total au système
- Droits : `is_director = True`, `is_staff = True`, `is_teacher = True`

### 2. Professeur
- Rôle : Gestion de classe et communication avec les parents
- Permissions : Gestion de leurs classes assignées
- Droits : `is_teacher = True`

### 3. Parent
- Rôle : Suivi de leurs enfants et communication avec l'école
- Permissions : Accès limité aux informations de leurs enfants
- Droits : `is_parent = True`

---

## Cas d'Utilisation par Acteur

## 🏫 CAS D'UTILISATION - DIRECTEUR

### CU-D01 : Gérer les niveaux scolaires

**Acteur principal** : Directeur

**Préconditions** :
- L'utilisateur est authentifié comme directeur
- Accès à l'interface d'administration

**Scénario principal** :
1. Le directeur accède à la section "Niveaux scolaires"
2. Le système affiche la liste des niveaux (Maternelle, Primaire, Collège)
3. Le directeur peut :
   - Créer un nouveau niveau avec nom, slug et description
   - Modifier un niveau existant
   - Supprimer un niveau (si aucune classe associée)
   - Voir les classes associées à chaque niveau

**Postconditions** :
- Les modifications sont enregistrées dans `SchoolLevel`
- Les professeurs et parents voient les changements

**Scénarios alternatifs** :
- **3a** : Tentative de suppression d'un niveau avec des classes → Erreur affichée
- **3b** : Slug déjà existant → Message d'erreur

---

### CU-D02 : Gérer les classes

**Acteur principal** : Directeur

**Préconditions** :
- Au moins un niveau scolaire existe
- Des professeurs sont enregistrés dans le système

**Scénario principal** :
1. Le directeur accède à la section "Classes"
2. Le système affiche la liste de toutes les classes
3. Le directeur peut :
   - Créer une nouvelle classe (nom, niveau, année scolaire)
   - Assigner un professeur principal à la classe
   - Modifier les informations d'une classe
   - Supprimer une classe
   - Voir les élèves de chaque classe

**Postconditions** :
- La classe est créée/modifiée dans `Classroom`
- Le professeur assigné peut accéder à la classe
- Les conversations de groupe sont créées automatiquement

**Scénarios alternatifs** :
- **3a** : Aucun professeur disponible → Option de créer un professeur d'abord
- **3b** : Suppression d'une classe avec élèves → Confirmation requise

**Règles métier** :
- Une classe ne peut avoir qu'un seul professeur principal
- Le professeur doit avoir `is_teacher = True`

---

### CU-D03 : Gérer les élèves

**Acteur principal** : Directeur

**Préconditions** :
- Au moins une classe existe
- Des parents peuvent être associés (optionnel)

**Scénario principal** :
1. Le directeur accède à la section "Élèves"
2. Le système affiche la liste de tous les élèves
3. Le directeur peut :
   - Ajouter un nouvel élève (prénom, nom, date de naissance, photo)
   - Assigner l'élève à une classe
   - Associer un ou plusieurs parents à l'élève
   - Modifier les informations d'un élève
   - Supprimer un élève
   - Changer l'élève de classe

**Postconditions** :
- L'élève est enregistré dans `Student`
- Les parents associés peuvent voir l'élève dans leur interface
- L'élève apparaît dans la liste de sa classe

**Scénarios alternatifs** :
- **3a** : Parent non existant → Option de créer le compte parent d'abord
- **3b** : Photo trop volumineuse → Message d'erreur

**Règles métier** :
- Un élève peut avoir plusieurs parents (garde partagée)
- Un élève ne peut être que dans une seule classe à la fois
- Les parents doivent avoir `is_parent = True`

---

### CU-D04 : Gérer les utilisateurs

**Acteur principal** : Directeur

**Préconditions** :
- Accès à l'interface d'administration

**Scénario principal** :
1. Le directeur accède à la section "Utilisateurs"
2. Le système affiche la liste de tous les utilisateurs
3. Le directeur peut :
   - Créer un nouveau compte (professeur, parent, directeur)
   - Définir les rôles : `is_parent`, `is_teacher`, `is_director`
   - Modifier les informations d'un utilisateur
   - Activer/désactiver un compte
   - Réinitialiser le mot de passe
   - Supprimer un compte utilisateur

**Postconditions** :
- Le compte est créé/modifié dans `CustomUser`
- Les permissions sont appliquées selon le rôle
- L'utilisateur peut se connecter avec ses identifiants

**Scénarios alternatifs** :
- **3a** : Username déjà existant → Message d'erreur
- **3b** : Suppression d'un professeur avec classes → Confirmation + réassignation

**Règles métier** :
- Un directeur est automatiquement professeur et staff
- Un utilisateur peut avoir plusieurs rôles simultanément
- Le username doit être unique

---

### CU-D05 : Créer des conversations de groupe

**Acteur principal** : Directeur

**Préconditions** :
- Au moins une classe avec un professeur existe
- Des parents sont associés aux élèves de la classe

**Scénario principal** :
1. Le directeur sélectionne une ou plusieurs classes
2. Le directeur choisit l'option "Créer conversation de groupe"
3. Le système crée automatiquement :
   - Une conversation de type 'group'
   - Ajoute le professeur comme participant
   - Ajoute tous les parents des élèves de la classe
4. Le système confirme la création

**Postconditions** :
- Une conversation de groupe est créée dans `Conversation`
- Tous les participants peuvent accéder à la conversation
- La conversation est liée à la classe via `classroom` FK

**Scénarios alternatifs** :
- **2a** : Conversation déjà existante pour cette classe → Message d'information
- **3a** : Aucun parent dans la classe → Conversation créée avec le professeur uniquement

**Règles métier** :
- Une classe ne peut avoir qu'une conversation de groupe principale
- Les participants sont automatiquement déterminés

---

### CU-D06 : Consulter les statistiques

**Acteur principal** : Directeur

**Préconditions** :
- Des données existent dans le système

**Scénario principal** :
1. Le directeur accède au tableau de bord
2. Le système affiche :
   - Nombre total d'élèves par niveau
   - Nombre de classes
   - Nombre de professeurs
   - Nombre de parents
   - Nombre de publications récentes
   - Activité des conversations
3. Le directeur peut filtrer par période ou niveau

**Postconditions** :
- Les statistiques sont affichées
- Aucune modification de données

---

## 👨‍🏫 CAS D'UTILISATION - PROFESSEUR

### CU-P01 : Consulter sa classe

**Acteur principal** : Professeur

**Préconditions** :
- Le professeur est authentifié
- Le professeur est assigné à au moins une classe

**Scénario principal** :
1. Le professeur accède à son tableau de bord
2. Le système affiche ses classes (via `taught_classes`)
3. Le professeur sélectionne une classe
4. Le système affiche :
   - Liste des élèves de la classe
   - Informations sur chaque élève (nom, prénom, photo)
   - Parents associés à chaque élève
   - Statistiques de la classe

**Postconditions** :
- Aucune modification de données
- Le professeur a consulté les informations

**Scénarios alternatifs** :
- **2a** : Aucune classe assignée → Message "Aucune classe assignée"

---

### CU-P02 : Publier du contenu dans une conversation de groupe

**Acteur principal** : Professeur

**Préconditions** :
- Une conversation de groupe existe pour la classe
- Le professeur est participant de la conversation

**Scénario principal** :
1. Le professeur accède à la conversation de sa classe
2. Le professeur clique sur "Nouvelle publication"
3. Le professeur remplit :
   - Titre (optionnel)
   - Description
   - Photo (optionnel)
4. Le professeur publie
5. Le système enregistre la publication
6. Tous les parents de la classe voient la publication

**Postconditions** :
- Un nouveau `Post` est créé
- `Post.author` = professeur
- `Post.conversation` = conversation de groupe
- `Post.is_published = True`
- La conversation est remontée dans la liste (last_message_at mis à jour)

**Scénarios alternatifs** :
- **3a** : Aucune description ni photo → Message d'erreur
- **4a** : Photo trop volumineuse → Message d'erreur

**Règles métier** :
- Seuls les professeurs peuvent publier dans les conversations de groupe de classe
- Les publications sont visibles par tous les participants

---

### CU-P03 : Répondre à un parent en message privé

**Acteur principal** : Professeur

**Préconditions** :
- Un parent a envoyé un message au professeur
- Le professeur a accès à sa messagerie

**Scénario principal** :
1. Le professeur accède à sa messagerie
2. Le système affiche les messages reçus (via `received_messages`)
3. Le professeur sélectionne un message non lu
4. Le professeur lit le message
5. Le système marque le message comme lu (`is_read = True`)
6. Le professeur clique sur "Répondre"
7. Le professeur rédige sa réponse (sujet, contenu)
8. Le professeur envoie le message

**Postconditions** :
- Un nouveau `Message` est créé
- `Message.sender` = professeur
- `Message.recipient` = parent
- Le parent reçoit une notification (si implémenté)

**Scénarios alternatifs** :
- **7a** : Contenu vide → Message d'erreur

---

### CU-P04 : Créer une conversation privée avec un ou plusieurs parents

**Acteur principal** : Professeur

**Préconditions** :
- Le professeur a des élèves dans sa classe
- Les élèves ont des parents associés

**Scénario principal** :
1. Le professeur accède à sa messagerie
2. Le professeur clique sur "Nouvelle conversation"
3. Le système affiche la liste des parents de ses élèves
4. Le professeur sélectionne un ou plusieurs parents
5. Le professeur donne un nom à la conversation
6. Le professeur crée la conversation
7. Le système crée une `Conversation` de type 'private'

**Postconditions** :
- Une nouvelle `Conversation` est créée
- `Conversation.conversation_type = 'private'`
- `Conversation.created_by` = professeur
- Les parents sélectionnés sont ajoutés aux participants
- La conversation apparaît dans la liste des participants

**Scénarios alternatifs** :
- **4a** : Aucun parent sélectionné → Message d'erreur

---

### CU-P05 : Consulter les publications de sa classe

**Acteur principal** : Professeur

**Préconditions** :
- Des publications existent pour les conversations de sa classe

**Scénario principal** :
1. Le professeur accède à la conversation de groupe de sa classe
2. Le système affiche toutes les publications (via `posts`)
3. Le professeur peut :
   - Voir ses publications
   - Modifier ses publications
   - Supprimer ses publications
   - Voir les publications d'autres professeurs (si applicable)

**Postconditions** :
- Aucune modification si consultation uniquement

**Scénarios alternatifs** :
- **2a** : Aucune publication → Message "Aucune publication"

---

## 👪 CAS D'UTILISATION - PARENT

### CU-PA01 : Consulter la page d'accueil

**Acteur principal** : Parent

**Préconditions** :
- Le parent est authentifié
- Le parent a au moins un enfant associé

**Scénario principal** :
1. Le parent se connecte
2. Le système affiche le sélecteur de niveau
3. Le parent voit les niveaux de ses enfants :
   - Si enfant en Maternelle → Bouton "Maternelle"
   - Si enfant en Primaire → Bouton "Primaire"
   - Si enfant en Collège → Bouton "Collège"
4. Le parent sélectionne un niveau
5. Le système redirige vers le tableau de bord du niveau

**Postconditions** :
- Le parent accède au tableau de bord approprié

**Scénarios alternatifs** :
- **2a** : Aucun enfant associé → Message "Aucun enfant trouvé"
- **4a** : Enfants dans plusieurs niveaux → Le parent peut choisir

**Règles métier** :
- Un parent ne voit que les niveaux où ses enfants sont inscrits

---

### CU-PA02 : Consulter les publications de la classe

**Acteur principal** : Parent

**Préconditions** :
- Le parent est participant d'une conversation de groupe
- Des publications existent dans la conversation

**Scénario principal** :
1. Le parent accède au tableau de bord du niveau
2. Le parent clique sur "Publications" ou "Photos"
3. Le système affiche les publications de la conversation de groupe
4. Les publications sont triées par date (plus récente en premier)
5. Le parent peut :
   - Voir les photos
   - Lire les descriptions
   - Voir l'auteur et la date

**Postconditions** :
- Aucune modification
- Le parent a consulté les publications

**Scénarios alternatifs** :
- **3a** : Aucune publication → Message "Aucune publication disponible"

**Règles métier** :
- Les parents ne peuvent pas publier dans les conversations de groupe de classe
- Les parents ne voient que les publications publiées (`is_published = True`)

---

### CU-PA03 : Envoyer un message au professeur

**Acteur principal** : Parent

**Préconditions** :
- L'enfant du parent a un professeur assigné
- Le parent est authentifié

**Scénario principal** :
1. Le parent accède à la messagerie
2. Le parent clique sur "Nouveau message"
3. Le système affiche les professeurs des classes de ses enfants
4. Le parent sélectionne un professeur
5. Le parent remplit :
   - Sujet du message
   - Contenu du message
6. Le parent envoie le message
7. Le système crée un `Message`

**Postconditions** :
- Un nouveau `Message` est créé
- `Message.sender` = parent
- `Message.recipient` = professeur
- `Message.is_read = False`
- Le professeur reçoit une notification (si implémenté)

**Scénarios alternatifs** :
- **5a** : Champs obligatoires vides → Message d'erreur

---

### CU-PA04 : Consulter ses enfants

**Acteur principal** : Parent

**Préconditions** :
- Le parent a au moins un enfant associé via la relation `parents`

**Scénario principal** :
1. Le parent accède à la section "Mes enfants"
2. Le système affiche la liste des enfants (via `children`)
3. Pour chaque enfant, le parent voit :
   - Prénom et nom
   - Photo
   - Classe actuelle
   - Niveau scolaire
   - Professeur principal

**Postconditions** :
- Aucune modification
- Le parent a consulté les informations

**Scénarios alternatifs** :
- **2a** : Aucun enfant associé → Message "Aucun enfant trouvé"

**Règles métier** :
- Un parent ne peut voir que ses propres enfants
- Les informations affichées sont en lecture seule

---

### CU-PA05 : Participer à une conversation privée

**Acteur principal** : Parent

**Préconditions** :
- Une conversation privée existe où le parent est participant
- La conversation a été initiée par un professeur ou le parent

**Scénario principal** :
1. Le parent accède à la messagerie
2. Le système affiche ses conversations (via `conversations`)
3. Le parent sélectionne une conversation privée
4. Le parent peut :
   - Voir l'historique des publications
   - Publier un nouveau message dans la conversation
   - Voir les autres participants
5. Le parent rédige un message et publie

**Postconditions** :
- Un nouveau `Post` est créé dans la conversation
- `Post.author` = parent
- `Post.conversation` = conversation privée
- Tous les participants voient le message

**Scénarios alternatifs** :
- **2a** : Aucune conversation → Message "Aucune conversation"

**Règles métier** :
- Les parents peuvent publier dans les conversations privées
- Les parents ne peuvent pas voir les conversations des autres parents

---

### CU-PA06 : Consulter les photos de l'enfant (Maternelle)

**Acteur principal** : Parent d'un enfant en Maternelle

**Préconditions** :
- L'enfant est en maternelle
- Des photos ont été publiées dans la conversation de groupe

**Scénario principal** :
1. Le parent accède au tableau de bord Maternelle
2. Le parent clique sur "Photos"
3. Le système affiche une galerie de photos
4. Les photos proviennent des publications avec images de la conversation
5. Le parent peut :
   - Voir les photos en grand format
   - Voir la date et description
   - Naviguer entre les photos

**Postconditions** :
- Aucune modification
- Le parent a consulté les photos

**Scénarios alternatifs** :
- **3a** : Aucune photo → Message "Aucune photo disponible"

**Règles métier** :
- Seules les publications avec images sont affichées
- Les photos doivent être publiées (`is_published = True`)

---

## 🔄 CAS D'UTILISATION TRANSVERSAUX

### CU-T01 : S'authentifier

**Acteurs** : Tous (Directeur, Professeur, Parent)

**Préconditions** :
- Le compte utilisateur existe
- Le compte est actif

**Scénario principal** :
1. L'utilisateur accède à la page de connexion
2. L'utilisateur saisit :
   - Username
   - Mot de passe
3. L'utilisateur clique sur "Se connecter"
4. Le système vérifie les identifiants
5. Le système crée une session
6. Le système redirige selon le rôle :
   - Directeur → Panel d'administration
   - Professeur → Tableau de bord professeur
   - Parent → Sélecteur de niveau

**Postconditions** :
- L'utilisateur est authentifié
- Une session est active
- L'utilisateur accède à son interface

**Scénarios alternatifs** :
- **4a** : Identifiants incorrects → Message d'erreur + retour au formulaire
- **4b** : Compte désactivé → Message "Compte désactivé"

---

### CU-T02 : Se déconnecter

**Acteurs** : Tous (Directeur, Professeur, Parent)

**Préconditions** :
- L'utilisateur est authentifié

**Scénario principal** :
1. L'utilisateur clique sur "Se déconnecter"
2. Le système termine la session
3. Le système redirige vers la page de connexion

**Postconditions** :
- La session est détruite
- L'utilisateur est déconnecté

---

### CU-T03 : Consulter une conversation

**Acteurs** : Professeur, Parent

**Préconditions** :
- L'utilisateur est participant de la conversation
- La conversation existe

**Scénario principal** :
1. L'utilisateur accède à la liste des conversations
2. Le système affiche les conversations où il est participant
3. L'utilisateur sélectionne une conversation
4. Le système affiche :
   - Le nom de la conversation
   - La liste des participants
   - L'historique des publications (via `posts`)
   - Le formulaire de nouvelle publication (si autorisé)
5. L'utilisateur peut publier un nouveau message

**Postconditions** :
- L'utilisateur a consulté la conversation
- Éventuellement, un nouveau message est publié

**Scénarios alternatifs** :
- **2a** : Aucune conversation → Message "Aucune conversation"

**Règles métier** :
- Seuls les participants peuvent voir la conversation
- Les messages sont triés par date de création

---

### CU-T04 : Rechercher une conversation/utilisateur

**Acteurs** : Professeur, Directeur

**Préconditions** :
- L'utilisateur est authentifié

**Scénario principal** :
1. L'utilisateur accède à la barre de recherche
2. L'utilisateur saisit un terme de recherche
3. Le système recherche dans :
   - Noms de conversations
   - Noms d'utilisateurs
   - Noms d'élèves (si professeur/directeur)
4. Le système affiche les résultats
5. L'utilisateur peut cliquer sur un résultat pour y accéder

**Postconditions** :
- Les résultats sont affichés
- L'utilisateur peut accéder aux éléments trouvés

---

## 📊 Diagrammes de Cas d'Utilisation

### Diagramme - Directeur

```
                    ┌──────────────────────────────────┐
                    │         DIRECTEUR                │
                    └──────────────────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┬────────────────┐
                │                 │                 │                │
                ▼                 ▼                 ▼                ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │ Gérer les    │  │ Gérer les    │  │ Gérer les    │  │ Gérer les    │
        │ niveaux      │  │ classes      │  │ élèves       │  │ utilisateurs │
        └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
                │
                ▼
        ┌──────────────┐
        │ Créer        │
        │ conversations│
        │ de groupe    │
        └──────────────┘
                │
                ▼
        ┌──────────────┐
        │ Consulter    │
        │ statistiques │
        └──────────────┘
```

### Diagramme - Professeur

```
                    ┌──────────────────────────────────┐
                    │         PROFESSEUR               │
                    └──────────────────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┬────────────────┐
                │                 │                 │                │
                ▼                 ▼                 ▼                ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │ Consulter    │  │ Publier du   │  │ Répondre à   │  │ Créer        │
        │ sa classe    │  │ contenu      │  │ un parent    │  │ conversation │
        └──────────────┘  └──────────────┘  └──────────────┘  │ privée       │
                                                              └──────────────┘
                                  │
                                  ▼
                          ┌──────────────┐
                          │ Consulter    │
                          │ publications │
                          └──────────────┘
```

### Diagramme - Parent

```
                    ┌──────────────────────────────────┐
                    │           PARENT                 │
                    └──────────────────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┬────────────────┐
                │                 │                 │                │
                ▼                 ▼                 ▼                ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │ Consulter    │  │ Consulter    │  │ Envoyer un   │  │ Consulter    │
        │ page accueil │  │ publications │  │ message au   │  │ ses enfants  │
        └──────────────┘  └──────────────┘  │ professeur   │  └──────────────┘
                                            └──────────────┘
                │                                 │
                ▼                                 ▼
        ┌──────────────┐                  ┌──────────────┐
        │ Participer à │                  │ Consulter    │
        │ conversation │                  │ photos       │
        │ privée       │                  │ (Maternelle) │
        └──────────────┘                  └──────────────┘
```

---

## 🔐 Matrice des Permissions

| Cas d'Utilisation | Directeur | Professeur | Parent |
|-------------------|-----------|------------|--------|
| Gérer niveaux scolaires | ✅ | ❌ | ❌ |
| Gérer classes | ✅ | ❌ | ❌ |
| Gérer élèves | ✅ | ❌ | ❌ |
| Gérer utilisateurs | ✅ | ❌ | ❌ |
| Créer conversations de groupe | ✅ | ✅ (limité) | ❌ |
| Consulter statistiques | ✅ | ✅ (limité) | ❌ |
| Consulter sa classe | ✅ | ✅ | ❌ |
| Publier dans groupe classe | ✅ | ✅ | ❌ |
| Publier dans conversation privée | ✅ | ✅ | ✅ |
| Répondre à messages | ✅ | ✅ | ✅ |
| Créer conversation privée | ✅ | ✅ | ✅ |
| Consulter publications | ✅ | ✅ | ✅ |
| Envoyer message professeur | ✅ | ✅ | ✅ |
| Consulter ses enfants | N/A | N/A | ✅ |
| Consulter photos | ✅ | ✅ | ✅ |

---

## 📝 Règles Métier Globales

### Authentification et Autorisation
1. Tous les utilisateurs doivent être authentifiés pour accéder au système
2. Les rôles sont cumulables (ex: un utilisateur peut être parent ET professeur)
3. Un directeur a automatiquement les droits de professeur et staff

### Gestion des Classes
4. Une classe ne peut avoir qu'un seul professeur principal
5. Un professeur peut enseigner plusieurs classes
6. Un élève ne peut être que dans une seule classe à la fois

### Gestion des Relations Parent-Enfant
7. Un élève peut avoir plusieurs parents (garde partagée)
8. Un parent peut avoir plusieurs enfants
9. Un parent ne voit que les informations de ses propres enfants

### Conversations et Publications
10. Les conversations de groupe sont automatiquement créées pour chaque classe
11. Seuls les professeurs peuvent publier dans les conversations de groupe de classe
12. Tout participant peut publier dans une conversation privée
13. Les publications doivent avoir au moins une description ou une photo
14. Les photos sont limitées en taille (à définir dans settings.py)

### Messagerie
15. Un message doit avoir un expéditeur et un destinataire différents
16. Les messages non lus sont marqués comme tels
17. Les parents peuvent uniquement envoyer des messages aux professeurs de leurs enfants

### Confidentialité
18. Les informations personnelles (dates de naissance, photos) sont protégées
19. Les parents ne peuvent pas voir les informations des autres élèves
20. Les professeurs ne voient que les élèves de leurs classes

---

## 🔄 Flux de Données Principaux

### Flux 1 : Création d'une classe avec communication

```
Directeur crée classe
        ↓
Directeur assigne professeur
        ↓
Directeur ajoute élèves
        ↓
Directeur associe parents aux élèves
        ↓
Système crée conversation de groupe automatiquement
        ↓
Professeur et parents peuvent communiquer
```

### Flux 2 : Publication de contenu par un professeur

```
Professeur se connecte
        ↓
Professeur accède à conversation de groupe
        ↓
Professeur crée publication (titre, photo, description)
        ↓
Système enregistre Post
        ↓
Système met à jour last_message_at de Conversation
        ↓
Parents voient publication dans leur fil
```

### Flux 3 : Communication parent-professeur

```
Parent se connecte
        ↓
Parent accède à messagerie
        ↓
Parent rédige message pour professeur
        ↓
Système crée Message (is_read = False)
        ↓
Professeur reçoit notification
        ↓
Professeur lit message (is_read = True)
        ↓
Professeur répond
        ↓
Parent reçoit réponse
```

---

## 📅 Scénarios de Vie Réels

### Scénario 1 : Rentrée scolaire
1. Le directeur crée les niveaux (Maternelle, Primaire, Collège) - **CU-D01**
2. Le directeur crée les classes pour l'année 2025-2026 - **CU-D02**
3. Le directeur crée les comptes professeurs - **CU-D04**
4. Le directeur assigne les professeurs aux classes - **CU-D02**
5. Le directeur inscrit les élèves - **CU-D03**
6. Le directeur crée les comptes parents - **CU-D04**
7. Le directeur associe les parents aux élèves - **CU-D03**
8. Le système crée automatiquement les conversations de groupe - **CU-D05**

### Scénario 2 : Journée type d'un professeur
1. Le professeur se connecte - **CU-T01**
2. Le professeur consulte sa classe et la liste des élèves - **CU-P01**
3. Le professeur prend des photos pendant une activité
4. Le professeur publie les photos dans la conversation de groupe - **CU-P02**
5. Un parent envoie un message concernant son enfant
6. Le professeur lit le message et répond - **CU-P03**
7. Le professeur se déconnecte - **CU-T02**

### Scénario 3 : Journée type d'un parent
1. Le parent se connecte - **CU-T01**
2. Le parent sélectionne le niveau de son enfant - **CU-PA01**
3. Le parent consulte les nouvelles photos publiées - **CU-PA02** / **CU-PA06**
4. Le parent veut poser une question sur les devoirs
5. Le parent envoie un message au professeur - **CU-PA03**
6. Le parent consulte les informations de son enfant - **CU-PA04**
7. Le parent se déconnecte - **CU-T02**

### Scénario 4 : Communication urgente
1. Le professeur doit communiquer une information urgente
2. Le professeur crée une conversation privée avec plusieurs parents - **CU-P04**
3. Le professeur publie le message dans la conversation privée
4. Les parents reçoivent des notifications
5. Les parents consultent la conversation et répondent - **CU-PA05**

---

### Extensions Possibles :
1. **Notifications en temps réel** : WebSocket pour notifications push
2. **Application mobile** : Version mobile native (iOS/Android)
3. **Visioconférence** : Intégration d'un système de visio pour réunions parents-professeurs
4. **Cahier de texte numérique** : Gestion des devoirs et leçons
5. **Gestion des absences** : Signalement et suivi des absences
6. **Bulletin de notes** : Évaluation et bulletins numériques
7. **Calendrier partagé** : Événements et sorties scolaires
8. **Paiement en ligne** : Cantine, sorties, fournitures
9. **Traduction multilingue** : Support de plusieurs langues
10. **Export PDF** : Génération de documents PDF (bulletins, attestations)

### Nouveaux Cas d'Utilisation Potentiels :
- **CU-EXT01** : Recevoir des notifications push
- **CU-EXT02** : Participer à une visioconférence
- **CU-EXT03** : Consulter les devoirs de son enfant
- **CU-EXT04** : Signaler une absence
- **CU-EXT05** : Consulter les notes et bulletins
- **CU-EXT06** : S'inscrire à un événement scolaire
- **CU-EXT07** : Effectuer un paiement en ligne