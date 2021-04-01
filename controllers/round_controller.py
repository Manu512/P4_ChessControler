"""Round Controller"""
# coding: utf-8

from controllers import BaseController

from models.tournament import Tournament

from models.players import Player


class RoundController(BaseController):
    """
    Purpose Enabling the control and monitoring of tournament rounds.

    """
    def __init__(self, tournament: Tournament):
        """

        Args:
            tournament: obj(Tournament)
        """
        super().__init__(tournament)
        self.round = tournament.rounds[-1]

    def menu_round(self):
        """
        Round management menu
        """
        title = "Bienvenue dans le gestionnaire de tournois d'échec.\n"
        subtitle = "Console de gestion des rounds du tournoi."
        menu = {1: (self.menu_round, f"Nom : {self.round.name}"),
                2: (self.menu_round, f"Début du Round : {self.round.start}"),
                3: (self.menu_round, f"Fin du Round : {self.round.end}"),
                4: (self.display_list_round_matchs, 'Consulter les matches en cours'),
                5: (self.add_score, f"Saisir les scores du Round {self.round.number}"),
                6: (self.start_new_round, 'Démarrer un nouveau Round'),
                9: (str('back'), 'Retour au menu')}

        if self.round.end is None:
            menu[6] = (self.stop_round, f'Déclarer le round {self.round.number} fini')
        elif self.round.number <= self.tournament.max_rounds_number:
            result = [match.score for match in self.round.matches if match.score is None]
            if len(result):
                menu[6] = (self.add_score, f'{len(result)} score reste à saisir '
                                           f'pour pouvoir démarrer le prochain round')
            elif len(result) == 0 and self.round.number == self.tournament.max_rounds_number:
                self.tournament.save()
                menu[6] = (self.view_result, "Tournoi terminé - Afficher les résultats")
            elif len(result) == 0 and self.round.number < self.tournament.max_rounds_number:
                menu[4] = (self.display_list_round_matchs, 'Consulter les résultats des matchs')
                del menu[5]

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        r = self.ask_and_launch(menu=menu)

        return self.back_menu(r)

    def display_list_round_matchs(self):
        """
        Method that calls up the view displaying the matches of the current round
        """
        self.view_menu.view_matchs(self.round)

    def add_score(self):
        """
        Method that calls up the view that informs the winners of the different matches
        """
        self.view_menu.select_match(self.round)

        response = self.ask_and_store_number("Choisissez le match pour renseigner le vainqueur :")
        if response[0]:
            if 1 <= response[1] <= 4:
                 # response = tuple(False/True if valid input, input value)
                match_played = self.round.matches[response[1]-1]

                if match_played.score is None:
                    self.view_menu.select_winner(match_played)
                    response = self.ask_and_store_number()

                    if response[1] in [1, 2]:   # One player won
                        match_played.players[response[1]-1].win()
                        match_played.win(match_played.players[response[1]-1])

                    elif response[1] == 3:       # Result = Equality
                        match_played.players[0].equality()
                        match_played.players[1].equality()
                        match_played.win()

                    # We add to the has_met attribute of the player the opponent he has just faced.
                    match_played.players[0].add_meet(match_played.players[1].uuid)
                    match_played.players[1].add_meet(match_played.players[0].uuid)

                else:   # Si le match a déjà un résultat d'enregistré => Alerter l'utilisateur
                    self.view_menu.stand_by_msg("Le match sélectionné à déjà été clos")

    def start_new_round(self):
        """
        Method to start a new round.
        """
        self.tournament.add_round()
        self.round = self.tournament.rounds[-1]
        self.tournament.save()

    def stop_round(self):
        """
        Method of informing the end of the round.
        """
        if self.round.start != "":
            self.round.end_round()

    def view_result(self):
        """
        Méthode qui affiche le résultat du tournoi.

        Returns:

        """

        p = Player.list_player_tournament()
        p.sort(reverse=True, key=lambda x: (int(x.point), int(x.elo)))
        data = []
        for n, player in enumerate(p):
            data.append(f"{n + 1} - {player.fullname} ({player.age} ans) avec {player.point} points,"
                        f" classement ELO : {player.elo}")

        title = "Bienvenue dans le gestionnaire de tournois d'échec.\n"
        subtitle = "Classement du tournoi."

        self.view_menu.display_data(title, subtitle, data)
