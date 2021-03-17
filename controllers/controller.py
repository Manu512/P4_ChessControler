"""Controller"""
# coding:utf-8

from controllers import BaseController
from controllers.round_controller import RoundController
from controllers.report_controller import ReportController

from models.players import Player
from models.tournament import Tournament


class Controller(BaseController):
    """
    Object Central controller for basic menus
    """
    def __init__(self):
        super().__init__()
        Player.load_players()
        self.report = ReportController()

    def menu_accueil(self):
        """
        Method for displaying the home menu
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec.\n"
        menu = {1: (self.menu_tournament, "Gestion tournoi"),
                2: (self.menu_players, "Gestion des joueurs"),
                3: (self.report.menu_rapport, "Affichage des rapports"),
                9: (exit, "Sortie")}

        self.view_menu.display_menu(title=title, question=menu)

        self.ask_and_launch(menu=menu)

    def menu_players(self):
        """
        Method to display the player management menu
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page de gestion des joueurs."

        menu = {1: (self.add_player, "Créer un joueur"),
                2: (self.update_player_elo, "Modifier le classement ELO d'un joueur"),
                3: (self.add_player_tournament, "Ajouter un joueur au tournoi actuel"),
                4: (self.remove_player_tournament, "Supprimer un joueur du tournoi actuel"),
                9: (self.menu_accueil, "Retour")}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)

    def menu_tournament(self):
        """
        Menu which allows the setting of the tournament.
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page de gestion du tournoi."

        menu = {1: (self.change_name_tournament, f"Nom : {Tournament.NAME}"),
                2: (self.change_number_round_tournament, f"Nombre de rounds : {Tournament.NB_ROUND}"),
                3: (self.change_timer_rules, f"Règle de temps : {Tournament.TIMER}"),
                4: (self.change_location, f"Localisation : {Tournament.LOCATION}"),
                5: (self.add_description, f"Description : {Tournament.DESCRIPTION}"),
                6: (self.create_tournament, 'Initialiser un nouveau tournoi avec ces valeurs'),
                7: (self.switch_rctournament, "Gestion des rounds"),
                8: (self.load_tournament, "Charger un tournoi sauvegardé"),
                9: (self.menu_accueil, 'Retour Accueil')}

        if self.tournament is not None:
            menu[6] = (self.stop_tournament, "Arrêter le tournoi (attention sauvegarder avant !!!)")
            menu[8] = (self.save_tournament, "Sauvegarder tournoi en cours")
        else:
            del menu[7]

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)
        self.ask_and_launch(menu=menu)
        self.menu_tournament()

    # --------------------------_PLAYERS METHODS------------------------------------

    def add_player(self):
        """
        Display the add_player menu
        Loop for each information to retrieve
        Name (name), Firstname (firstname), Date of Birth (dob), Sex (_genre)
        Then create a new player and save the list.
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
                valid = self.view_menu.input(menu[m+1][1] + ' : ')
                while not self._control_user_input("dob", valid):
                    valid = self.view_menu.input(menu[m+1][1] + ' : ')
                response.append(valid[1])
            elif choice[m] == '_genre':
                valid = self.view_menu.input(menu[m+1][1] + ' : ')
                while not self._control_user_input("_genre", valid):
                    valid = self.view_menu.input(menu[m+1][1] + ' : ')
                response.append(valid)
            res = dict(zip(choice, response))
        Player(**res)
        Player.save_all_players()
        self.menu_players()

    def update_player_elo(self):
        """

        Method to update the player's data.

        1° Request of the player's name and firstname
        2° Search for the player
        3° Display of the current ranking
        4° Input of the new ranking

        """
        player = self.found_specific_player()
        if player is not None:
            valid = self.ask_and_store_number("Veuillez renseigner le nouveau ELO : ")
            while not valid[0]:
                valid = self.ask_and_store_number("Veuillez renseigner le nouveau ELO : ")
            player.update_classement(valid[1])
            player.update_player()

    def add_player_tournament(self):
        """
        Method to assign a player to the tournament.

        1° Request the name and firstname of the player
        2° Search for the player if he is not already active in the tournament
        3° Request validation of the active status for the tournament
        """
        player = self.found_specific_player()
        if player is not None:
            if player.status:
                self.view_menu.stand_by_msg("Attention {} {} est déjà "
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
        Method to remove the active status from the tournament

        1° Request the name and firstname of the player
        2° Search for the player if he is not already inactive in the tournament
        3° Request validation of the inactive status for the tournament
        """
        player = self.found_specific_player()
        if player is not None:
            if not player.status:
                self.view_menu.stand_by_msg("Attention {} {} est déjà inscrit au "
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
        Method that will search for a player based on his Last Name and First Name.
        Returns a player object
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
                return player

        self.view_menu.stand_by_msg("Joueur introuvable !\n"
                                    "Rechercher à nouveau ou créer le joueur")

    # --------------------------TOURNAMENTS METHODS--------------------------------

    def change_name_tournament(self):
        """
        Method that changes the name of the tournament.
        """
        valid = self.ask_and_store_text('Saisir le nom du tournoi : ')
        if valid[0]:
            Tournament.NAME = valid[1]
        else:
            self.change_name_tournament()

    def change_number_round_tournament(self):
        """
        Method that changes the number of rounds in the tournament.
        """
        valid = self.ask_and_store_number('Saisir le nombre de tours du tournoi : ')
        if valid[0]:
            Tournament.NB_ROUND = valid[1]
        else:
            self.change_number_round_tournament()

    def change_timer_rules(self):
        """
        Menu that allows the timer to be set.
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page de paramétrage du timer du tournoi."
        menu = {1: (self.set_timer_bullet, "BULLET"),
                2: (self.set_timer_blitz, "BLITZ"),
                3: (self.set_timer_fast, "COUP RAPIDE"),
                9: (self.menu_tournament, 'Retour Accueil Tournament')}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)

    def set_timer_bullet(self):
        """
        Method to set the timer attribute to Bullet.
        """
        if self.tournament is None:
            Tournament.TIMER = "Bullet"
        else:
            self.tournament.set_timer_bullet()

    def set_timer_blitz(self):
        """
        Method to set the timer attribute to Blitz.
        """
        if self.tournament is None:
            Tournament.TIMER = "Blitz"
        else:
            self.tournament.set_timer_blitz()

    def set_timer_fast(self):
        """
        Method to set the timer attribute to Fast.
        """
        if self.tournament is None:
            Tournament.TIMER = "Coup Rapide"
        else:
            self.tournament.set_timer_fast()

    def change_location(self):
        """
        Method that changes the location of the tournament.
        """
        valid = self.ask_and_store_text('Saisir la localisation du tournoi : ')
        if valid[0]:
            Tournament.LOCATION = valid[1]
        else:
            self.change_location()

    def add_description(self):
        """
        Method that adds a description at the tournament level.
        """
        valid = self.view_menu.input("Saisir la description du tournoi : ")
        if self._control_user_input('sentence', valid):
            Tournament.DESCRIPTION = valid
        else:
            self.add_description()

    def create_tournament(self):
        """
        Method for initiating a new tournament
        """
        Player.initialise_players_data()
        super().__init__(Tournament())
        self.tournament.add_round()
        self.round = self.tournament.rounds[-1]
        self.switch_rctournament()

    def switch_rctournament(self):
        ret = True
        while ret:
            ret = RoundController(self.tournament).menu_round()

    def load_tournament(self):
        """
        Method to load a tournament
        """
        self.tournament = Tournament.load()
        self.round = self.tournament.rounds[-1]
        self.switch_rctournament()

    def save_tournament(self):
        """
        Method to save the tournament
        """
        self.tournament.save()

    def stop_tournament(self):
        """
        Method for deleting the tournament attribute
        """
        self.tournament = None
