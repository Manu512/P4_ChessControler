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

