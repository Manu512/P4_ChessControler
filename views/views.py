# coding: utf-8
import os
from platform import system


class Display:
    """
    Classe pour la gestion du menu propose à l'utilisateur

    """
    def __init__(self):
        self.clean()

    @staticmethod
    def clean():
        if system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def accueil(self):
        self.clean()
        print("Bienvenue dans le gestionnaire de tournois d'échec.\n\n")

        menu = {"1": "Gestion tournoi",
                "2": "Gestion des joueurs",
                "3": "Affichage des rapports",
                "4": "Sortie"}

        self.view_menu(menu)
        return menu

    def tournament(self):
        self.clean()
        print("Bienvenue dans le gestionnaire de tournois d'échec."
              "\nPage de gestion du tournoi.\n")

        menu = {"1": "Configurer un nouveau tournoi",
                "2": "Charger un tournoi sauvegardé",
                "3": "Sauvegarder tournoi actuel",
                "4": "Retour Accueil"}

        self.view_menu(menu)
        return menu

    def players(self):
        self.clean()
        print("Bienvenue dans le gestionnaire de tournois d'échec."
              "\nPage de gestion des joueurs.\n")

        menu = {"1": "Créer un joueur",
                "2": "Modifier le classement ELO d'un joueur",
                "3": "Ajouter un joueur au tournoi actuel",
                "4": "Supprimer un joueur du tournoi actuel",
                "5": "Retour"}

        self.view_menu(menu)
        return menu

    def rapport(self):
        self.clean()
        print("Bienvenue dans le gestionnaire de tournois d'échec."
              "\nPage d'édition des rapports.\n")

        menu = {"1": "Liste de tous les joueurs",
                "2": "Liste de tous les joueurs d'un tournoi",
                "3": "Liste de tous les tournois",
                "4": "Liste de tous les tours du tournoi",
                "5": "Liste de tous les matchs du tournoi",
                "6": "Retour"}

        self.view_menu(menu)
        return menu

# ------------------------SubMeny Tournament-----------------------------------

    def new_tournament(self, **kwargs):
        self.clean()
        print("Bienvenue dans le gestionnaire de tournois d'échec."
              "\nParamétrage actuel du nouveau tournoi.\n")

        menu = list(zip(range(1,len(kwargs)+1),list(kwargs),list(kwargs.values())))
        self.view_menu(menu, True)
        return menu




# -------------------------SubMenu Player--------------------------------------

    def add_player(self):
        self.clean()
        print("Bienvenue dans le gestionnaire de tournois d'échec.\nAjout "
              "d'un joueur \n")
        print("Saisir dans l'ordre :\n")

        menu = ["- Nom du joueur",
                "- Prénom du joueur",
                "- Date de naissance (Format dd/mm/aaaa)",
                "- Sexe (H/F)"]

        self.view_menu(menu)
        return menu

# -----------------------------------------------------------------------------

    @staticmethod
    def error_msg(msg):
        print(msg)

    @classmethod
    def view_menu(cls, menu, special=False):
        """Method permettant d'afficher les menus ou les informations
         contenues dans une liste ou un dictionnaire"""
        if special:
            for choice, text, param in menu:
                if param:
                    print("\t{} : {} = {}".format(choice, text, param))
                else:
                    print("\t{} : {}".format(choice, text))

        elif type(menu) is list:
            for info in menu:
                print("\t", info)

        else:
            for choice, text in menu.items():
                print("\t", choice, ":", text)

        print("\n")


if __name__ == '__main__':
    d = Display()
    d.accueil()
