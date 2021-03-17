"""Round Controller"""
# coding: utf-8

from controllers import BaseController

from models.tournament import Tournament


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
        self.menu_round()

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
                6: (self.start_new_round, 'Démarrer nouveau Round'),
                9: (str("back"), 'Retour au menu')}

        if self.round.end is None:
            menu[6] = (self.stop_round, f'Le round {self.round.number} est fini')
        else:
            result = [match.score for match in self.round.matches if match.score is None]
            if result:
                menu[6] = (self.add_score, f'{len(result)} score reste à saisir pour démarrer le prochain round')

        self.view_menu.display_menu(title=title, subtitle=subtitle, question=menu)

        r = self.ask_and_launch(menu=menu)

        if r:
            pass
        else:
            self.menu_round()

    def display_list_round_matchs(self):
        """
        Method that calls up the view displaying the matches of the current round
        """
        self.view_menu.view_matchs(self.round)
        self.menu_round()

    def add_score(self):
        """
        Method that calls up the view that informs the winners of the different matches
        """
        self.view_menu.select_match(self.round)
        response = self.ask_and_store_number("Choisissez le match pour renseigner le vainqueur :")

        if response[0]:     # response = tuple(False/True if valid input, input value)
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

                # We add to the has_met attribute of the player the opponent he has just faced.
                match_played.players[0].add_meet(match_played.players[1].uuid)
                match_played.players[1].add_meet(match_played.players[0].uuid)

            else:   # Si le match a déjà un résultat d'enregistré => Alerter l'utilisateur
                self.view_menu.stand_by_msg("Le match sélectionné à déjà été clos")

    def start_new_round(self):
        """
        Method to start a new round.
        """
        # TODO : Lors du démarrage du nouveau Round, on doit clôturer l'actuel et initialiser le nouveau
        # Il faut aussi vérifier que les résultats de tous les matchs ont bien été renseigné

        if self.round.start != "" and self.round.end == "":     # If the old round is not finished ==> Error
            self.view_menu.stand_by_msg("Attention, le précédent round n'est pas fini !")
        else:
            self.tournament.add_round()
            self.round = self.tournament.rounds[-1]

    def stop_round(self):
        """
        Method of informing the end of the round.
        """
        # TODO : Lors de l'appel a cette fonction, on pourrait
        #  controller l'état des matchs. Si non renseigné => On test
        if self.round.start != "":
            self.round.end_round()
        else:
            self.view_menu.stand_by_msg("Commencer par démarrer un round !!!!")

        self.menu_round()
