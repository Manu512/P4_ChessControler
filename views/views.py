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

    def display_menu(self, title: str, subtitle: str="\n",  question: dict = None):
        print(f"{title}")
        print(f"{subtitle}\n")
        for key, value in question.items():
            print(f"\t{key} : {value[1]}")
        print("\n" * 2)

# ------------------------SubMeny Tournament-----------------------------------

    def new_tournament(self, **kwargs):
        self.clean()
        print("Bienvenue dans le gestionnaire de tournois d'échec."
              "\nParamétrage actuel du nouveau tournoi.\n")

        menu = list(zip(range(1,len(kwargs)+1),list(kwargs),list(kwargs.values())))
        self.view_menu(menu, True)
        return menu

    def sub_round(self, **kwargs):
        self.clean()
        print("Bienvenue dans le gestionnaire de tournois d'échec."
              "\nGestion des rounds du tournoi.\n")

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

# -----------------------SubMenu Round ---------------------------------------

    def view_matchs(self, rounds):
        self.clean()
        print(f"Bienvenue dans le gestionnaire de tournois d'échec.\nSuivi des "
              f"Matchs du tour N° {rounds.number}")
        print("Les rencontres : \n")
        for match in rounds.matches:
            if match.score:
                print("\t{} : {} vs {} : {}".format(match.players[0].fullname,
                                                    match.score[0],
                                                    match.players[1].fullname,
                                                    match.score[1]))
            else:
                print("\t{} vs {} : En attente du résultat".format(match.players[0].fullname,
                                                                   match.players[1].fullname))
        print("\n"*5)

    def select_match(self, rounds):
        self.clean()
        print(f"Bienvenue dans le gestionnaire de tournois d'échec.\nSuivi des "
              f"Matchs du rounds {rounds.number}")
        print("Selection de la rencontre : \n")
        for nb, match in enumerate(rounds.matches):
            if match.score:
                print("\t{} - {} : {} vs {} : {}".format(nb + 1, match.players[0].fullname,
                                                    match.score[0],
                                                    match.players[1].fullname,
                                                    match.score[1]))
            else:
                print("\t{} - {} vs {} : En attente du résultat".format(nb + 1, match.players[0].fullname,
                                                                   match.players[1].fullname))


        print("\n" * 5)

    def select_winner(self, match):
        self.clean()
        print(f"Bienvenue dans le gestionnaire de tournois d'échec.\nSuivi des "
              f"Matchs opposant : {match.players[0].fullname} à {match.players[1].fullname}")
        print("\n\tSelection du vainqueur : \n")

        print(f"\t1 : {match.players[0].fullname}")
        print(f"\t2 : {match.players[1].fullname}")
        print(f"\t3 : En cas d'égalité")



        print("\n" * 5)

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
