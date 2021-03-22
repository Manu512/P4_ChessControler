""" Player Menu Controller"""
# coding:utf-8

from controllers import BaseController
from models.players import Player


class PlayerController(BaseController):
    """
    Purpose Enabling the control and monitoring players

    """

    def __init__(self):
        super().__init__()

    def menu_players(self):
        """
        Method to display the player management menu
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec."
        subtitle = "Page de gestion des joueurs."

        menu = {1: (self.add_player, "Créer un joueur"),
                2: (self.update_player_elo, "Modifier le classement ELO d'un joueur"),
                9: (str('back'), 'Retour au menu')}

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        r = self.ask_and_launch(menu=menu)

        return self.back_menu(r)

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

        for i in range(4):
            if 0 <= i <= 1:  # pour les question nom et prénom

                valid = self.ask_and_store_text(menu[i + 1][1] + ' : ')
                while not valid[0]:
                    valid = self.ask_and_store_text(menu[i + 1][1] + ' : ')
                response.append(valid[1])

            elif i == 2:  # pour la date de naissance
                valid = self.view_menu.input(menu[i + 1][1] + ' : ')
                while not self._control_user_input("dob", valid):
                    valid = self.view_menu.input(menu[i + 1][1] + ' : ')
                response.append(valid)

            elif i == 3:  # pour la saisie du genre
                valid = self.view_menu.input(menu[i + 1][1] + ' : ')
                while not self._control_user_input("_genre", valid):
                    valid = self.view_menu.input(menu[i + 1][1] + ' : ')
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
                self.view_menu.stand_by_msg("Attention {} {} n'est pas inscrit au "
                                            "tournoi".format(player.name, player.first_name))
            else:
                valid = self.ask_and_store_text("Confirmez vous que {} {} "
                                                "ne participe plus au tournoi ? (O/N)"
                                                .format(player.name, player.first_name))
                if valid[0]:
                    player.switch_player_tournament()
                    Player.save_all_players()

    @staticmethod
    def remove_all_player_tournament():
        """
        Appel de la methode pour désinscrire tout les joueurs.
        """
        Player.all_players_inactive()
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

        for player in Player.PLAYERS:
            if player.name.upper() == search_response[0].upper() and \
                    player.first_name.capitalize() == search_response[1].capitalize():
                return player

        self.view_menu.stand_by_msg("Joueur introuvable !\n"
                                    "Rechercher à nouveau ou créer le joueur")
