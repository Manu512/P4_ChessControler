""" Objet View"""
# coding: utf-8

import os
from platform import system

from models.matchs import Match


class Display:
    """
    Class for displaying the menu
    """

    def __init__(self):
        self.clean()

    @staticmethod
    def clean():
        """
        Method to reset/clear the console window
        """
        if system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def display_menu(self, title: str, subtitle: str = "\n", question: dict = None):
        """
        Method to display a menu.

        Args:
            title: str: Main title of the console
            subtitle: str: Subtitle of the console
            question: dict{ int(Choice) : Tuple( method to launch, Text to display )}
        """
        self.clean()
        print(f"{title}")
        print(f"{subtitle}\n")
        for key, value in question.items():
            print(f"\t{key} : {value[1]}")
        print("\n" * 2)

# -----------------------SubMenu Round ---------------------------------------

    def view_matchs(self, rounds):
        """

        Args:
            rounds:
        """
        self.clean()
        print(f"Bienvenue dans le gestionnaire de tournois d'échec.\n"
              f"Suivi des Matchs du tour N° {rounds.number}")
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
        print("\n" * 5)

    def select_match(self, rounds):
        """
        A method of displaying and selecting a match.
        Args:
            rounds:
        """
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

    def select_winner(self, match: Match):
        """
        Method to display and select the winner of the match.
        Args:
            match: obj(Match)
        """
        self.clean()
        print(f"Bienvenue dans le gestionnaire de tournois d'échec.\nSuivi des "
              f"Matchs opposant : {match.players[0].fullname} à {match.players[1].fullname}")
        print("\n\tSelection du vainqueur : \n")

        print(f"\t1 : {match.players[0].fullname}")
        print(f"\t2 : {match.players[1].fullname}")
        print("\t3 : En cas d'égalité")

        print("\n" * 5)

    @staticmethod
    def error_msg(msg: str):
        """
        Call method to display an error message and request a keystroke to continue.
        Args:
            msg: str : Error message
        """
        print(msg)
        input("Pressez une touche pour continuer...")
