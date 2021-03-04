"""Round Controller"""
# coding: utf-8

from views.views import Display
from models.rounds import Round


class RoundController:

    def __init__(self, players: list, main_control):
        self.view_menu = Display()
        self.main_control = main_control
        self.round = Round(players)

    def menu_round(self):
        info = {'Nom':                                              self.round.name,
                'Début du Round':                                   self.round.start,
                'Fin du Round':                                     self.round.end,
                'Consulter les matches en cours':                    "",
                f'Saisir les scores du Round {self.round.N_ROUND}': "",
                'Démarrer nouveau Round':                           "",
                'Retour au menu':                                   ""}

        choice = {1: self.menu_round,
                  2: self.menu_round,
                  3: self.stop_round,
                  4: self.list_round_matchs,
                  5: self.add_score,
                  6: self.start_new_round,
                  7: self.main_control.menu_tournament}

        self.view_menu.sub_round(**info)

        response = self.main_control.c_input()

        if self.main_control._check_choice(list(range(1, len(info) + 1)), response):
            choice[int(response)]()

        self.menu_round()

    def list_round_matchs(self):
        if self.round.N_ROUND != 0:
            self.view_menu.view_matchs(self.round)
        else:
            self.view_menu.error_msg("Commencer par démarrer un round !!!!")

        self.main_control.input_press_continue()

    def add_score(self):
        if self.round.N_ROUND != 0:
            self.view_menu.select_match(self.round)
            response = self.main_control.c_input("Choisissez le match pour renseigner le résultat :")

            if self.check_match_choice(self.round.matches, response):
                match_played = self.round.matches[int(response) - 1]
                self.view_menu.select_winner(match_played)
                response = self.main_control.c_input()

                if int(response) in [1, 2]:
                    match_played.players[int(response) - 1].win()
                    match_played.win(match_played.players[int(response) - 1])
                    print(f"Le gagnant est !!!! {match_played.players[int(response)-1]}")
                else:
                    match_played.players[0].equality()
                    match_played.players[1].equality()
                    match_played.win()
                    print(f"Equality !!!!!")

                match_played.players[0].has_met.append(match_played.players[1].id)
                match_played.players[1].has_met.append(match_played.players[0].id)

                return

        else:
            self.view_menu.error_msg("Commencer par démarrer un round !!!!")

    def start_new_round(self):
        """Si l'ancien round n'est pas fini ==> Erreur"""
        if self.round.start != "" and self.round.end == "":
            self.view_menu.error_msg("Attention, le précédent round n'est pas fini !")
            self.main_control.input_press_continue()
        else:
            self.round.new_round()

    def stop_round(self):
        if self.round.start != "":
            self.round.end_round()
        else:
            self.view_menu.error_msg("Commencer par démarrer un round !!!!")
            self.main_control.input_press_continue()

    def check_match_choice(self, matchs, response: int) -> bool:
        if len(str(response)) != 1:
            Display.error_msg("Choix incorrect. Un chiffre demandé."
                              " Veuillez ressaisir !")
            self.main_control.input_press_continue()
            return False
        elif int(response) not in [1, 2, 3, 4]:
            Display.error_msg("Choix incorrect !! Veuillez ressaisir")
            self.main_control.input_press_continue()
            return False
        else:
            return True
