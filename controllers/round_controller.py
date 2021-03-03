"""Round Controller"""
# coding: utf-8

import datetime as dt
from views.views import Display
from models.tournoi import Tournoi
from models.rounds import Round


class RoundController:

	def __init__(self, players: list, maincontrol):
		self.view_menu = Display()
		self.maincontrol = maincontrol
		self.round = Round(players)
		self.menu_round()

	def menu_round(self):
		info = {"Nom":                           self.round.name,
				"Début du Round":                self.round.start,
				"Fin du Round": self.round.end,
				"Consulter les matchs en cours": "",
				"Saisir les scores du Round {}".format(self.round.N_ROUND):            "",
				"Démarrer nouveau Round":                 "",
				"Terminer le round N°": self.round.N_ROUND,
				"Retour au menu":                ""}

		choice = {1: self.menu_round,
				  2: self.menu_round,
				  3: self.menu_round,
				  4: self.menu_round,
				  5: self.menu_round,
				  6: self.start_new_round,
				  7: self.stop_round,
				  8: self.maincontrol.menu_tournament}

		Display.sub_round(Display, **info)

		response = self.maincontrol.c_input()

		if self.maincontrol._check_choice(list(range(1, len(info) + 1)), response):
			choice[int(response)]()

		self.menu_round()

	def nothing(self):
		pass

	def start_new_round(self):
		"""Si l'ancien round n'est pas fini ==> Erreur"""
		if self.round.start != "" and self.round.end == "":
			Display.error_msg("Attention, le précédent round n'est pas fini !")
			self.maincontrol.input_press_continue()
		else:
			self.round.new_round()

	def stop_round(self):
		self.round.end_round()