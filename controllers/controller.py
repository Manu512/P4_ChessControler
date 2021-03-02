"""Controller"""
# coding:utf-8

import re
from datetime import datetime as dt
from models.players import Player
from views.views import Display


class Controller:

    def __init__(self):
        Player.load_players()
        self.view_menu = Display()
        self.menu_accueil()

    def menu_accueil(self):
        self.view_menu.accueil()
        menu = {"1": self.menu_tournament,
                "2": self.menu_players,
                "3": self.menu_rapport,
                "4": exit}

        response = self.c_input()
        if self.__check_choice(menu, response):
            menu[response]()
        else:
            self.menu_accueil()
        
    def menu_players(self):
        self.view_menu.players()
        menu = {"1": self.add_player,
                "2": self.update_player_elo,
                "3": self.add_player_tournament,
                "4": self.remove_player_tournament,
                "5": self.menu_accueil}

        response = self.c_input()
        if self.__check_choice(menu, response):
            menu[response]()
        else:
            self.menu_players()

    def menu_tournament(self):
        self.view_menu.tournament()
        menu = {"1": self.new_tournament,
                "2": self.load_tournament,
                "3": self.save_tournament,
                "4": self.menu_accueil}

        response = self.c_input()
        if self.__check_choice(menu, response):
            menu[response]()
        else:
            self.menu_tournament()

    def menu_rapport(self):
        self.view_menu.rapport()
        menu = {"1": self.list_all_players,
                "2": self.list_tournament_players,
                "3": self.list_tournaments,
                "4": self.list_all_rounds,
                "5": self.list_all_matchs,
                "6": self.menu_accueil}

        response = self.c_input()
        if self.__check_choice(menu, response):
            menu[response]()
        else:
            self.menu_rapport()

# --------------------------_PLAYERS METHODS------------------------------------

    def add_player(self):
        """
        Affiche le menu add_player
        Boucle pour chaque information à récupérer
        Nom (name), Prénom (firstname), Date de Naissance (dob), sexe (_genre)
        Puis crée un nouveau joueur et sauvegarde la liste.
        """
        choice = ('name', 'first_name', 'dob', '_genre')
        response = []
        menu = self.view_menu.add_player()
        for m in range(len(choice)):
            res = self.c_input(menu[m][2:] + ' : ')
            while not self.__controle_data_input(choice[m], res):
                res = self.c_input(menu[m][2:] + ' : ')
            response.append(res)
            res = dict(zip(choice, response))
        Player(**res)
        Player._save_players()
        self.menu_players()

    def update_player_elo(self):
        """
        1° Demande du nom et du prenom du joueur
        2° Recherche du joueur
        3° Affichage du classement actuel
        4° Input pour le nouveau classement
        """
        player = self.found_specific_player()
        res = self.c_input("Veuillez renseigner le nouveau ELO : ")
        while not self.__controle_data_input('elo', res):
            res = self.c_input("Veuillez renseigner le nouveau ELO : ")
        player.elo = res
        Player._save_players()


    def add_player_tournament(self):
        """
        1° Demande du nom et du Prenom du joueur
        2° Recherche du joueur s'il n'est pas déjà actif dans le tournoi
        3° Demande validation quant au passage du status à 1
        """
        pass

    def remove_player_tournament(self):
        """
        1° Demande du nom et du Prenom du joueur
        2° Recherche du joueur s'il n'est pas déjà inactif dans le tournoi
        3° Demande validation quant au passage du status à 1
        """
        pass

    def found_specific_player(self):
        search_question = ('Nom du joueur recherché : ',
                           'Prénom du joueur recherché : ')
        search_response = []
        for question in search_question:
            res = self.c_input(question)
            while not self.__controle_data_input('text', res):
                res = self.c_input(question)
            search_response.append(res)

        for player in Player._PLAYERS:
            if player.name == search_response[0] and\
                    player.first_name == search_response[1]:
                return player
            else:
                self.found_specific_player()

# --------------------------TOURNAMENTS METHODS--------------------------------

    def new_tournament(self):
        pass

    def load_tournament(self):
        pass

    def save_tournament(self):
        pass

# --------------------------RAPPORT METHODS------------------------------------

    def list_all_players(self):
        """
        Fonction qui va lancer le print de la liste des joueurs connus
        """
        Player._list_all_player()

    def list_tournament_players(self):
        """
        Fonction qui va lancer le print de la liste des joueurs du tournois
        """
        pass

    def list_tournaments(self):
        """
        Fonction qui va lancer le print de la liste des tournois
        """
        pass

    def list_all_rounds(self):
        """
        Fonction qui va lancer le print de tous les rounds du tournois
        """
        pass

    def list_all_matchs(self):
        """
        Fonction qui va lancer le print de la liste des matchs du tournois
        """
        pass

# --------------------------GENERAL METHODS------------------------------------

    def c_input(self, ask_input="Votre choix : "):
        response = input(ask_input)
        return response

# -------------------------CONTROL METHODS-------------------------------------
    def __controle_data_input(self, question, response) -> bool:
        # Controle presence de chiffre dans le name/firstname
        if question in ['name', 'first_name', 'text']:
            if self.__check_number_in_word(response):
                Display.error_msg('Nom/Prénom saisi non valide !'
                                  '\nVeuillez resaissir !')
                return False

        if question == 'dob':
            # Controle le format de la date de naissance
            try:
                dt.strptime(response, '%d/%m/%Y')
            except ValueError:
                Display.error_msg('Veuillez saisir une date de naissance'
                                  ' valide !\nVeuillez resaissir !')
                return False
        elif question == '_genre':
            if response not in ['H', 'F']:
                Display.error_msg('Genre saisi non valide !'
                                  '\nVeuillez resaissir !')
                return False
        elif question == 'elo':
            try:
                int(response)
            except ValueError:
                Display.error_msg('Veuillez saisir un entier pour le elo !'
                                  '\nVeuillez resaissir !')
                return False
            else:
                if int(response) < 0:
                    Display.error_msg('Veuillez saisir un entier positif pour'
                                      ' le elo !\nVeuillez resaissir !')
                    return False
        return True

    def __check_choice(self, menu: dict, response: str) -> bool:
        if len(response) != 1:
            Display.error_msg("Choix incorrect. Un chiffre demandé."
                              " Veuillez ressaisir !")
            self.c_input("Pressez une touche pour continuer...")
            return False
        elif response not in list(menu):
            Display.error_msg("Choix incorrect !! Veuillez ressaisir")
            self.c_input("Pressez une touche pour continuer...")
            return False
        else:
            return True

    @staticmethod
    def __check_number_in_word(string):
        """ Verification d'absence de chiffre dans
         la variable passé en paramètre """
        chiffre_pattern = re.compile('\d')
        return re.search(chiffre_pattern, string)


if __name__ == '__main__':
    d = Controller()
    d.menu_accueil()