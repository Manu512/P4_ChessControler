"""Controller"""
# coding:utf-8

import re
from datetime import datetime as dt
from models.players import Player
from views.views import Display
from models.tournoi import Tournoi
from controllers.round_controller import RoundController as rc


class Controller:

    def __init__(self):
        Player.load_players()
        self.control_tournament = ''
        self.view_menu = Display()
        self.control_round = ''
        self.menu_accueil()

    def menu_accueil(self):
        self.view_menu.accueil()
        menu = {1: self.menu_tournament,
                2: self.menu_players,
                3: self.menu_rapport,
                4: exit}

        response = self.c_input()
        if self._check_choice(menu, response):
            menu[int(response)]()

        self.menu_accueil()

    def menu_players(self):
        self.view_menu.players()
        menu = {1: self.add_player,
                2: self.update_player_elo,
                3: self.add_player_tournament,
                4: self.remove_player_tournament,
                5: Player.save_players,
                6: self.menu_accueil}

        response = self.c_input()
        if self._check_choice(menu, response):
            menu[int(response)]()

        self.menu_players()

    def menu_tournament(self):
        self.view_menu.tournament()
        menu = {1: self.new_tournament,
                2: self.load_tournament,
                3: self.save_tournament,
                4: self.call_round_controller,
                5: self.menu_accueil}

        response = self.c_input()
        if self._check_choice(menu, response):
            menu[int(response)]()

        self.menu_tournament()

    def menu_rapport(self):
        self.view_menu.rapport()
        menu = {1: self.list_all_players,
                2: self.list_tournament_players,
                3: self.list_tournaments,
                4: self.list_all_rounds,
                5: self.list_all_matchs,
                6: self.menu_accueil}

        response = self.c_input()
        if self._check_choice(menu, response):
            menu[int(response)]()

    def call_round_controller(self):
        self.control_round = rc(Player.list_player_tournament(), self)
        self.control_round.menu_round()
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
            while not self._controle_data_input(choice[m], res):
                res = self.c_input(menu[m][2:] + ' : ')
            response.append(res)
            res = dict(zip(choice, response))
        Player(**res)
        Player.save_players()
        self.menu_players()

    def update_player_elo(self):
        """
        1° Demande du nom et du prenom du joueur
        2° Recherche du joueur
        3° Affichage du classement actuel
        4° Input pour le nouveau classement
        """
        player = self.found_specific_player()
        if player is not None:
            res = self.c_input("Veuillez renseigner le nouveau ELO : ")
            while not self._controle_data_input('elo', res):
                res = self.c_input("Veuillez renseigner le nouveau ELO : ")
            player.elo = res
            Player.save_players()

    def add_player_tournament(self):
        """
        1° Demande du nom et du Prenom du joueur
        2° Recherche du joueur s'il n'est pas déjà actif dans le tournoi
        3° Demande validation quant au passage du status à 1
        """
        player = self.found_specific_player()
        if player is not None:
            if player.status:
                Display.error_msg("Attention {} {} est déjà "
                                  "inscrit au tournoi"
                                  .format(player.name, player.first_name))
            else:
                res = self.c_input("Confirmez vous que {} {} "
                                   "participe au tournoi ? "
                                   "(O/N)".format(player.name,
                                                  player.first_name))
                if self._controle_data_input("bool", res):
                    player.switch_player_tournament()
                    Player.save_players()

    def remove_player_tournament(self):
        """
        1° Demande du nom et du Prenom du joueur
        2° Recherche du joueur s'il n'est pas déjà inactif dans le tournoi
        3° Demande validation quant au passage du status à 1
        """
        player = self.found_specific_player()
        if player is not None:
            if not player.status:
                Display.error_msg("Attention {} {} est déjà "
                                  "inscrit au tournoi"
                                  .format(player.name, player.first_name))
            else:
                res = self.c_input("Confirmez vous que {} {} "
                                   "participe plus au tournoi ? "
                                   "(O/N)".format(player.name,
                                                  player.first_name))
                if self._controle_data_input("bool", res):
                    player.switch_player_tournament()
                    Player.save_players()

    def found_specific_player(self):
        search_question = ('Nom du joueur recherché : ',
                           'Prénom du joueur recherché : ')
        search_response = []
        for question in search_question:
            res = self.c_input(question)
            while not self._controle_data_input('text', res):
                res = self.c_input(question)
            search_response.append(res)

        for player in Player._PLAYERS:
            if player.name.upper() == search_response[0].upper() and\
                    player.first_name.capitalize() == search_response[1].capitalize():
                print(player)
                return player

        Display.error_msg("Joueur introuvable !\n"
                          "Recherché à nouveau ou créer le joueur")
        return None

# --------------------------TOURNAMENTS METHODS--------------------------------

    def new_tournament(self):
        info = {"Nom": Tournoi.NAME,
                "Nombre de rounds": Tournoi.NB_ROUND,
                "Règle de temps": Tournoi.TIMER,
                "Description": Tournoi.DESCRIPTION,
                "Initialiser le tournoi": "",
                "Retour au menu": ""}

        choice = {1: self.change_name_tournament,
                  2: self.change_number_round_tournament,
                  3: self.change_timer_rules,
                  4: self.add_description,
                  5: self.create_tournament,
                  6: self.menu_accueil
                  }

        Display.new_tournament(Display, **info)

        response = self.c_input()

        if self._check_choice(list(range(1, len(info) + 1)), response):
            choice[int(response)]()

        self.new_tournament()

    def change_name_tournament(self):
        response = self.c_input("Saisir le nom du tournoi : ")
        if self._controle_data_input("sentence", response):
            Tournoi.NAME = response
        else:
            self.change_name_tournament()

    def change_number_round_tournament(self):
        response = self.c_input("Saisir le nombre de tours du tournoi : ")
        if self._controle_data_input("number", response):
            Tournoi.NB_ROUND = response
        else:
            self.change_number_round_tournament()

    def change_timer_rules(self):
        #TODO : Mettre en place l'input et le controle
        pass

    def add_description(self):
        response = self.c_input("Saisir la description du tournoi : ")
        if self._controle_data_input("sentence", response):
            Tournoi.DESCRIPTION = response
        else:
            self.add_description()

    def create_tournament(self):
        self.control_tournament = Tournoi()

    def load_tournament(self):
        pass

    def save_tournament(self):
        pass

# --------------------------RAPPORT METHODS------------------------------------

    def list_all_players(self):
        """
        Fonction qui va lancer le print de la liste des joueurs connus
        """
        # TODO : A metre en forme et dans le module VUE
        response = Player._list_all_player()
        print(response)

    def list_tournament_players(self):
        """
        Fonction qui va lancer le print de la liste des joueurs du tournois
        """
        # TODO : A metre en forme et dans le module VUE
        response = Player.list_player_tournament()
        print(response)

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
        Fonction qui va lancer le print de la liste des matches du tournois
        """
        pass

# --------------------------GENERAL METHODS------------------------------------
    @staticmethod
    def c_input(ask_input="Votre choix : "):
        response = input(ask_input)
        return response

# -------------------------CONTROL METHODS-------------------------------------
    def _controle_data_input(self, question, response) -> bool:
        # Controle presence de chiffre dans le name/firstname
        if question in ['name', 'first_name', 'text']:
            if self.__check_number_in_word(response):
                Display.error_msg('Nom/Prénom saisi non valide !'
                                  '\nVeuillez resaissir !')
                self.input_press_continue()
                return False
        if question == 'sentence':
            if self.__check_sentence(response) < 2:
                Display.error_msg('Saisie non valide !'
                                  '\nVeuillez resaissir !')
                self.input_press_continue()
                return False
        elif question == 'dob':
            # Controle le format de la date de naissance
            try:
                dt.strptime(response, '%d/%m/%Y')
            except ValueError:
                Display.error_msg('Veuillez saisir une date de naissance'
                                  ' valide !\nVeuillez resaissir !')
                self.input_press_continue()
                return False
        elif question == '_genre':
            if response not in ['H', 'F']:
                Display.error_msg('Genre saisi non valide !'
                                  '\nVeuillez resaissir !')
                self.input_press_continue()
                return False
        elif question == 'bool':
            if response not in ['O', 'N']:
                Display.error_msg('Réponse non valide !'
                                  '\nVeuillez resaissir !')
                self.input_press_continue()
                return False
        elif question == 'number':
            try:
                int(response)
            except ValueError:
                Display.error_msg('Veuillez saisir un nombre entier !'
                                  '\nVeuillez resaissir !')
                self.input_press_continue()
                return False
            else:
                if int(response) < 0:
                    Display.error_msg('Veuillez saisir un nombre entier !'
                                      '\nVeuillez resaissir !')
                    self.input_press_continue()
                    return False
        return True

    def _check_choice(self, menu, response: int) -> bool:
        if len(str(response)) != 1:
            Display.error_msg("Choix incorrect. Un chiffre demandé."
                              " Veuillez ressaisir !")
            self.input_press_continue()
            return False
        elif int(response) not in list(menu):
            Display.error_msg("Choix incorrect !! Veuillez ressaisir")
            self.input_press_continue()
            return False
        else:
            return True

    def input_press_continue(self):
        self.c_input("Pressez une touche pour continuer...")

    @staticmethod
    def __check_number_in_word(string):
        """ Verification d'absence de chiffre dans
         la variable passé en paramètre """
        chiffre_pattern = re.compile('\d')
        return re.search(chiffre_pattern, string)

    @staticmethod
    def __check_sentence(string):
        """ Verification d'absence de chiffre dans
         la variable passé en paramètre """
        sentence_pattern = re.compile('[a-z]+')
        return len([*re.finditer(sentence_pattern, string)])


if __name__ == '__main__':
    pass