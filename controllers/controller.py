"""Controller"""
# coding:utf-8

import re

from typing import Union

from controllers.round_controller import *
from models.players import Player
from models.rounds import Round
from models.tournoi import Tournoi
from views.views import Display


class BaseController:
    """
    Base Class
    """
    def __init__(self):
        self.view_menu = Display()
        self.tournament = None
        self.round = None

    # --------------------------GENERAL METHODS------------------------------------

    def ask_and_launch(self, ask_input="Votre choix : ", *, menu: dict):
        """
        Methode pour interagir avec l'utilisateur, contrôler sa réponse
        et définir la suite des évènements. En fonction des menus qui lui sont
        présenté.

        Methode Arguments :
        self : instance
        ask_input : Texte qui sera demandé
        menu : argument nommé qui contient un dictionnaire
        dict{int(x):(tuple(Methode à lancer, Choix à afficher)}
        """
        user_input = input(ask_input)

        if dict is not None:
            menu_to_analyse = menu
            try:
                user_input = int(user_input)
            except ValueError:
                self.ask_and_launch(ask_input, menu=menu)

            if self._check_choice(list(menu.keys()), user_input):
                menu[user_input][0]()
            else:
                self.ask_and_launch(ask_input, menu=menu_to_analyse)

    def _check_choice(self, menu: list, response: int) -> bool:
        if response not in list(menu):
            self.view_menu.error_msg("Choix incorrect !! Veuillez ressaisir")
            self.input_press_continue()
            return False
        else:
            return True

    def ask_and_store_text(self, ask_input='Votre saisie : ') -> tuple[bool, str]:
        user_input = input(ask_input)

        if self._control_user_input('text', user_input):
            return True, user_input
        else:
            return False, user_input

    def ask_and_store_number(self, ask_input='Votre saisie : ') -> Union[tuple[bool, int], tuple[bool, str]]:
        user_input = input(ask_input)

        if self._control_user_input('number', user_input):
            return True, int(user_input)
        else:
            return False, user_input

    # -------------------------CONTROL METHODS---------------------------------

    def _control_user_input(self, question, response) -> bool:
        # Controle presence de chiffre dans le name/firstname
        if question in ['name', 'first_name', 'text']:
            if self.__check_number_in_word(response):
                self.view_menu.error_msg('Saisi non valide !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
        if question == 'sentence':
            if self.__check_sentence(response) < 2:
                self.view_menu.error_msg('Saisie non valide !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
        elif question == 'dob':
            # Controle le format de la date de naissance
            try:
                dt.strptime(response, '%d/%m/%Y')
            except ValueError:
                self.view_menu.error_msg('Veuillez saisir une date de naissance'
                                         ' valide !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
        elif question == '_genre':
            if response not in ['H', 'F']:
                self.view_menu.error_msg('Genre saisi non valide !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
        elif question == 'bool':
            if response not in ['O', 'N']:
                self.view_menu.error_msg('Réponse non valide !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
        elif question == 'number':
            try:
                int(response)
            except ValueError:
                self.view_menu.error_msg('Veuillez saisir un nombre entier !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
            else:
                if int(response) < 0:
                    self.view_menu.error_msg('Veuillez saisir un nombre entier !'
                                             '\nVeuillez ressaisir !')
                    self.input_press_continue()
                    return False
        return True

    @staticmethod
    def input_press_continue():
        input("Pressez une touche pour continuer...")

    @staticmethod
    def __check_number_in_word(string):
        """ Verification d'absence de chiffre dans
         la variable passé en paramètre """
        chiffre_pattern = re.compile('[0-9]')
        return re.search(chiffre_pattern, string)

    @staticmethod
    def __check_sentence(string):
        """ Verification d'absence de chiffre dans
         la variable passé en paramètre """
        sentence_pattern = re.compile('[a-z]+')
        return len([*re.finditer(sentence_pattern, string)])


class Controller(BaseController):

    def __init__(self):
        super().__init__()

    def menu_accueil(self):
        title = "Bienvenue dans le gestionnaire de tournois d'échec.\n"
        menu = {1: (self.menu_tournament, "Gestion tournoi"),
                2: (self.menu_players, "Gestion des joueurs"),
                3: (self.menu_rapport, "Affichage des rapports"),
                4: (exit, "Sortie")}

        self.view_menu.display_menu(title=title, question=menu)

        self.ask_and_launch(menu=menu)

    def menu_players(self):
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page de gestion des joueurs."

        menu = {1: (self.add_player, "Créer un joueur"),
                2: (self.update_player_elo, "Modifier le classement ELO d'un joueur"),
                3: (self.add_player_tournament, "Ajouter un joueur au tournoi actuel"),
                4: (self.remove_player_tournament, "Supprimer un joueur du tournoi actuel"),
                5: (Player.save_all_players, "Sauvegarder tous les joueurs"),
                6: (self.menu_accueil, "Retour")}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)

    def menu_tournament(self):
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page de gestion du tournoi."

        menu = {1: (self.menu_param_tournament, "Configurer un nouveau tournoi"),
                2: (self.load_tournament, "Charger un tournoi sauvegardé"),
                3: (self.save_tournament, "Sauvegarder tournoi actuel"),
                4: (self.switch_rctournament, "Gestion des rounds"),
                5: (self.menu_accueil, "Retour Accueil")}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)

    def menu_rapport(self):
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page d'édition des rapports"
        menu = {1: (self.list_all_players, "Liste de tous les joueurs"),
                2: (self.list_tournament_players, "Liste de tous les joueurs d'un tournoi"),
                3: (self.list_tournaments, "Liste de tous les tournois"),
                4: (self.list_all_rounds, "Liste de tous les tours du tournoi"),
                5: (self.list_all_matchs, "Liste de tous les matches du tournoi"),
                6: (self.menu_accueil, "Retour")}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)

    # --------------------------_PLAYERS METHODS------------------------------------

    def add_player(self):
        """
        Affiche le menu add_player
        Boucle pour chaque information à récupérer
        Nom (name), Prénom (firstname), Date de Naissance (dob), sexe (_genre)
        Puis crée un nouveau joueur et sauvegarde la liste.
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec.\nAjout d'un joueur"
        subtitle = "Saisir dans l'ordre :\n"

        menu = {1: ('', "Nom du joueur"),
                2: ('', "Prénom du joueur"),
                3: ('', "Date de naissance (Format dd/mm/aaaa)"),
                4: ('', "Sexe (H/F)")}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        choice = ('name', 'first_name', 'dob', '_genre')
        response = []

        for m in range(len(choice)):
            if choice[m] in ['name', 'first_name']:
                valid = self.ask_and_store_text(menu[m+1][1] + ' : ')
                while not valid[0]:
                    valid = self.ask_and_store_text(menu[m+1][1] + ' : ')
                response.append(valid[1])
            elif choice[m] == 'dob':
                valid = input(menu[m+1][1] + ' : ')
                while not self._control_user_input("dob", valid):
                    valid = input(menu[m+1][1] + ' : ')
                response.append(valid[1])
            elif choice[m] == '_genre':
                valid = input(menu[m+1][1] + ' : ')
                while not self._control_user_input("_genre", valid):
                    valid = input(menu[m+1][1] + ' : ')
                response.append(valid)
            res = dict(zip(choice, response))
        Player(**res)
        Player.save_all_players()
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
            valid = self.ask_and_store_number("Veuillez renseigner le nouveau ELO : ")
            while not valid[0]:
                valid = self.ask_and_store_number("Veuillez renseigner le nouveau ELO : ")
            player.update_classement(valid[1])
            Player.save_all_players()

    def add_player_tournament(self):
        """
        1° Demande du nom et du Prenom du joueur
        2° Recherche du joueur s'il n'est pas déjà actif dans le tournoi
        3° Demande validation quant au passage du status à 1
        """
        player = self.found_specific_player()
        if player is not None:
            if player.status:
                self.view_menu.error_msg("Attention {} {} est déjà "
                                         "inscrit au tournoi"
                                         .format(player.name, player.first_name))
            else:
                valid = self.ask_and_store_text("Confirmez vous que {} {} "
                                                "participe au tournoi ? "
                                                "(O/N)".format(player.name,
                                                               player.first_name))
                if valid[0]:
                    player.switch_player_tournament()
                    player.update_player()

    def remove_player_tournament(self):
        """
        1° Demande du nom et du Prenom du joueur
        2° Recherche du joueur s'il n'est pas déjà inactif dans le tournoi
        3° Demande validation quant au passage du status à 1
        """
        player = self.found_specific_player()
        if player is not None:
            if not player.status:
                self.view_menu.error_msg("Attention {} {} est déjà inscrit au "
                                         "tournoi".format(player.name, player.first_name))
            else:
                valid = self.ask_and_store_text("Confirmez vous que {} {} "
                                                "participe plus au tournoi ? (O/N)"
                                                .format(player.name, player.first_name))
                if valid[0]:
                    player.switch_player_tournament()
                    Player.save_all_players()

    def found_specific_player(self) -> Player:
        """
        Methode qui va rechercher un joueur d'après son Nom et son prénom.
        Renvoie un objet player
        """
        search_question = ('Nom du joueur recherché : ',
                           'Prénom du joueur recherché : ')
        search_response = []
        for question in search_question:
            valid = self.ask_and_store_text(question)
            while not valid[0]:
                valid = self.ask_and_store_text(question)
            search_response.append(valid[1])

        for player in Player._PLAYERS:
            if player.name.upper() == search_response[0].upper() and \
                    player.first_name.capitalize() == search_response[1].capitalize():
                print(player)
                return player

        self.view_menu.error_msg("Joueur introuvable !\n"
                                 "Recherché à nouveau ou créer le joueur")

    # --------------------------TOURNAMENTS METHODS--------------------------------

    def menu_param_tournament(self):
        """
        Menu qui permet le paramétrage du tournoi.
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page de paramétrage du tournoi."
        menu = {1: (self.change_name_tournament, f"Nom : {Tournoi.NAME}"),
                2: (self.change_number_round_tournament, f"Nombre de rounds : {Tournoi.NB_ROUND}"),
                3: (self.change_timer_rules, f"Règle de temps : {Tournoi.TIMER}"),
                4: (self.change_location, f"Localisation : {Tournoi.LOCATION}"),
                5: (self.add_description, f"Description : {Tournoi.DESCRIPTION}"),
                6: (self.create_tournament, 'Initialiser un nouveau tournoi'),
                7: (self.menu_accueil, 'Retour Accueil')}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)

    def change_name_tournament(self):
        """
        Methode qui change le nom du tournoi.
        """
        valid = self.ask_and_store_text('Saisir le nom du tournoi : ')
        if valid[0]:
            Tournoi.NAME = valid[1]
        else:
            self.change_name_tournament()

    def change_number_round_tournament(self):
        """
        Methode qui change le nombre de rounds du tournoi.
        """
        valid = self.ask_and_store_number('Saisir le nombre de tours du tournoi : ')
        if valid[0]:
            Tournoi.NB_ROUND = valid[1]
        else:
            self.change_number_round_tournament()

    def change_timer_rules(self):
        # TODO : Mettre en place l'input et le controle
        pass

    def change_location(self):
        """
        Methode qui change la localisation du tournoi.
        """
        valid = self.ask_and_store_text('Saisir la localisation du tournoi : ')
        if valid[0]:
            Tournoi.LOCATION = valid[1]
        else:
            self.change_location()

    def add_description(self):
        """
        Methode qui ajoute une description au niveau du tournoi.
        """
        valid = input("Saisir la description du tournoi : ")
        if self._control_user_input('sentence', valid):
            Tournoi.DESCRIPTION = valid
        else:
            self.add_description()

    def create_tournament(self):
        self.tournament = Tournoi()
        self.tournament.add_round()
        self.round = self.tournament.rounds[-1]
        self.switch_rctournament()

    def switch_rctournament(self):
        try:
            RoundController(self.tournament)
        except AttributeError:
            self.view_menu.error_msg("Commençons par initialiser le tournoi !")
            self.menu_param_tournament()

    def load_tournament(self):
        pass

    def save_tournament(self):
        self.tournament.save()

    # --------------------------RAPPORT METHODS------------------------------------

    @staticmethod
    def list_all_players(self):
        """
        Fonction qui va lancer le print de la liste des joueurs connus
        """
        # TODO : A metre en forme et dans le module VUE
        response = self._list_all_player()
        print(response)
        return

    def list_tournament_players(self):
        """
        Fonction qui va lancer le print de la liste des joueurs du tournois
        """
        # TODO : A metre en forme et dans le module VUE
        response = Player.list_player_tournament()
        print(response)
        return

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


if __name__ == '__main__':
    Player.load_players()
    main = Controller()
    while True:
        main.menu_accueil()
