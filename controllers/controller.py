"""Controller"""
# coding:utf-8

from controllers import BaseController
from controllers.round_controller import RoundController

from models.players import Player
from models.tournoi import Tournament


class Controller(BaseController):

    def __init__(self):
        super().__init__()
        Player.load_players()

    def menu_accueil(self):
        title = "Bienvenue dans le gestionnaire de tournois d'échec.\n"
        menu = {1: (self.menu_tournament, "Gestion tournoi"),
                2: (self.menu_players, "Gestion des joueurs"),
                3: (self.menu_rapport, "Affichage des rapports"),
                9: (exit, "Sortie")}

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
                9: (self.menu_accueil, "Retour")}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)

    def menu_tournament(self):
        """
        Menu qui permet le paramétrage du tournoi.
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
            del menu[6]
            menu[8] = (self.save_tournament, "Sauvegarder tournoi en cours")
        else:
            del menu[7]

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)
        self.ask_and_launch(menu=menu)
        self.menu_tournament()

    # def menu_tournament(self):
    #     title = "Bienvenue dans le gestionnaire de tournois d'échec."
    #     subtitle = "Page de gestion du tournoi."
    #
    #     menu = {1: (self.menu_tournament, "Configurer un nouveau tournoi"),
    #             2: (self.load_tournament, "Charger un tournoi sauvegardé"),
    #             3: (self.save_tournament, "Sauvegarder tournoi actuel"),
    #             9: (self.menu_accueil, "Retour Accueil")}
    #
    #     if self.tournament is None:    # Not possible to save without tournament
    #         del menu[3]
    #
    #     self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)
    #
    #     self.ask_and_launch(menu=menu)

    def menu_rapport(self):
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page d'édition des rapports"
        menu = {1: (self.list_all_players, "Liste de tous les joueurs"),
                2: (self.list_tournament_players, "Liste de tous les joueurs d'un tournoi"),
                3: (self.list_tournaments, "Liste de tous les tournois"),
                4: (self.list_all_rounds, "Liste de tous les tours du tournoi"),
                5: (self.list_all_matchs, "Liste de tous les matches du tournoi"),
                9: (self.menu_accueil, "Retour")}

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
            player.update_player()

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
                return player

        self.view_menu.error_msg("Joueur introuvable !\n"
                                 "Recherché à nouveau ou créer le joueur")

    # --------------------------TOURNAMENTS METHODS--------------------------------

    def change_name_tournament(self):
        """
        Methode qui change le nom du tournoi.
        """
        valid = self.ask_and_store_text('Saisir le nom du tournoi : ')
        if valid[0]:
            Tournament.NAME = valid[1]
        else:
            self.change_name_tournament()

    def change_number_round_tournament(self):
        """
        Methode qui change le nombre de rounds du tournoi.
        """
        valid = self.ask_and_store_number('Saisir le nombre de tours du tournoi : ')
        if valid[0]:
            Tournament.NB_ROUND = valid[1]
        else:
            self.change_number_round_tournament()

    def change_timer_rules(self):
        """
                Menu qui permet le paramétrage du timer.
                """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page de paramétrage du timer du tournoi."
        menu = {1: (Tournament.set_timer_bullet, "BULLET"),
                2: (Tournament.set_timer_blitz, "BLITZ"),
                3: (Tournament.set_timer_fast, "COUP RAPIDE"),
                9: (self.menu_tournament, 'Retour Accueil Tournament')}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        self.ask_and_launch(menu=menu)

    def change_location(self):
        """
        Methode qui change la localisation du tournoi.
        """
        valid = self.ask_and_store_text('Saisir la localisation du tournoi : ')
        if valid[0]:
            Tournament.LOCATION = valid[1]
        else:
            self.change_location()

    def add_description(self):
        """
        Methode qui ajoute une description au niveau du tournoi.
        """
        valid = input("Saisir la description du tournoi : ")
        if self._control_user_input('sentence', valid):
            Tournament.DESCRIPTION = valid
        else:
            self.add_description()

    def create_tournament(self):
        Player.initialise_players_data()
        self.tournament = Tournament()
        self.tournament.add_round()
        self.round = self.tournament.rounds[-1]
        self.switch_rctournament()

    def switch_rctournament(self):
        RoundController(self.tournament)

    def load_tournament(self):
        self.tournament = Tournament.load()
        self.round = self.tournament.rounds[-1]
        self.switch_rctournament()

    def save_tournament(self):
        self.tournament.save()

    # --------------------------RAPPORT METHODS------------------------------------

    def list_all_players(self):
        """
        Fonction qui va lancer le print de la liste des joueurs connus
        """
        # TODO : A metre en forme et dans le module VUE
        response = Player.list_all_player()
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
