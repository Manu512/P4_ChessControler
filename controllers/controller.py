"""Controller"""
# coding:utf-8

from controllers import BaseController
from controllers.round_controller import RoundController
from controllers.report_controller import ReportController
from controllers.player_controller import PlayerController

from models.players import Player
from models.tournament import Tournament


class Controller(BaseController):
    """
    Object Central controller for basic menus
    """
    def __init__(self):
        super().__init__()
        Player.load_players()

    def menu_accueil(self):
        """
        Method for displaying the home menu
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec.\n"
        menu = {1: (self.menu_tournament, "Gestion tournoi"),
                2: (self.launch_menu_players, "Gestion des joueurs"),
                3: (self.launch_menu_report, "Affichage des rapports"),
                9: (str('back'), "Fin")}

        self.view_menu.display_menu(title=title, question=menu)

        r = self.ask_and_launch(menu=menu)

        return self.back_menu(r)

    def menu_tournament(self):
        """
        Menu which allows the setting of the tournament.
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page de gestion du tournoi."
        menu = {1: (self.menu_config_tournament, 'Créer un nouveau tournoi'),
                2: (self.load_tournament, "Charger un tournoi sauvegardé"),
                3: (self.launch_menu_round, "Gestion du tournoi en cours"),
                4: (),
                5: (),
                9: (str('back'), 'Retour Accueil')}

        if self.tournament is not None:
            menu[4] = (self.stop_tournament, "Arrêter le tournoi (attention sauvegarder avant !!!)")
            menu[5] = (self.save_tournament, "Sauvegarder tournoi en cours")
        else:
            del menu[3]
            del menu[4]
            del menu[5]

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)

    def menu_config_tournament(self):
        """
        Menu which allows the setting of the tournament.
        """
        player_control = PlayerController()

        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page de gestion du tournoi."

        menu = {1: (self.change_name_tournament, f"Nom : {Tournament.NAME}"),
                2: (self.change_number_round_tournament, f"Nombre de rounds : {Tournament.NB_ROUND}"),
                3: (self.change_timer_rules, f"Règle de temps : {Tournament.TIMER}"),
                4: (self.change_location, f"Localisation : {Tournament.LOCATION}"),
                5: (self.add_description, f"Description : {Tournament.DESCRIPTION}"),
                6: (player_control.add_player_tournament, "Ajouter un participant au tournoi"),
                7: (player_control.remove_player_tournament, "Retirer un participant du tournoi"),
                'Info': ("None", f'Nombre de joueurs sélectionné : {Player.NB_ACTIVE_PLAYERS} '
                                 f'| Places disponibles {Tournament.NB_DEFAULT_PLAYERS - Player.NB_ACTIVE_PLAYERS}'),
                8: (self.create_tournament, 'Initialiser un nouveau tournoi avec ces valeurs'),
                9: (str('back'), 'Retour Accueil')}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)
        r = self.ask_and_launch(menu=menu)
        if self.back_menu(r):
            self.menu_config_tournament()

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
        self.launch_menu_round()

    def launch_menu_round(self):
        """
        Method for calling the Tournament Controller
        """
        ret = True
        while ret:
            ret = RoundController(self.tournament).menu_round()

    def launch_menu_report(self):
        """
        Method for calling the report controller
        """
        ret = True
        while ret:
            ret = ReportController().menu_rapport()

    def launch_menu_players(self):
        """
        Method for calling the Player Controller
        """
        ret = True
        while ret:
            ret = PlayerController().menu_players()

    def load_tournament(self):
        """
        Method to load a tournament
        """
        self.tournament = Tournament.load()
        self.round = self.tournament.rounds[-1]
        self.launch_menu_round()

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
