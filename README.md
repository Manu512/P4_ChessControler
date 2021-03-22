# __Suivi Tournoi Échec Projet P4__

## Prérequis
Une installation de Python 3.3 minimum pour pouvoir créer l'environnement virtuel avec cette méthode.

## Installation environnement virtuel
Se diriger sur le repertoire ou l'on souhaite installer l'environnement virtuel.
Executer la commande :
* `python3 -m venv 'env'` ('env' sera le repertoire où seront stocké les données de l'environnement 
python)

## Activation et installations des dépendances nécessaires au script dans l'environnement virtuel
### Sous Windows les commandes à exécuter :
* `env/Script/activate`
* `pip install -r requirements.txt`

### Sous Linux les commandes à exécuter : 
* `source env/bin/activate`
* `pip install -r requirements.txt`

## Génération d'un rapport html flake8
* `flake8 --format=html --htmldir=flake_rapport --max-line-length=119`


## Lancement et utilisation du Gestionnaire de tournoi.

Une fois l'environnement virtuel installé et activé, exécuter la commande suivante :
* `python tournament_launcher.py`

## Menu pour l'utilisation

# Écran d'accueil
* 1 : Gestion du tournoi
* 2 : Gestion des joueurs
* 3 : Affichage des rapports
* 9 : Fin / Sortie

# Écran Tournoi (Écran dynamique en fonction de la présence d'une instance Tournoi)
Cas Tournoi non actif :
* 1 : Créer un nouveau tournoi
* 2 : Charger un tournoi sauvegardé
  
Cas Tournoi actif/chargé :
* 1 : Arrêter le tournoi (attention sauvegarder avant !!!)
* 2 : Sauvegarder le tournoi en cours
* 3 : Gestion du tournoi

Dans tous les cas
* 9 : Retour accueil

# Écran de Gestion du tournoi
* 1 : Nom du Round
* 2 : Debut du Round
* 3 : Fin du Round
* 4 : Consulter les matches
* 5 : Saisir les scores des matchs du round en cours
* 6 : Démarrer round suivant / Afficher les résultats du tournoi
* 9 : Retour au menu

# Sous Menu Joueur
* 1 : Créer un joueur
* 2 : Modifier le classement ElO d'un joueur
* 9 : Retour au menu accueil

# Sous Menu Rapport
* 1 : Liste de tous les joueurs par ordre Alphabétique
* 2 : Liste de tous les joueurs par classement ELO
* 3 : Liste de tous les joueurs du tournoi par ordre Alphabétique
* 4 : Liste de tous les joueurs du tournoi par classement ELO
* 5 : Liste de tous les tournois
* 6 : Liste de tous les tours d'un tournoi
* 7 : Liste de tous les matchs d'un tournoi
* 9 : Retour au menu accueil

