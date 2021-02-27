"""Controller"""
# coding:utf-8

from tinydb import TinyDB
from models.players import Player
from views.accueil import ViewMenu


class Controller:

    def __init__(self):
        Player.load_players()
        self.console = ViewMenu()
        self.menu_accueil()

    def menu_accueil(self):
        self.console.accueil()
        menu = [self.menu_tournament, self.menu_players,
                self.menu_rapport, exit]
        response = self.c_input()
        menu[int(response)-1]()

    def menu_players(self):
        self.console.players()
        menu = [self.add_player, self.update_player, self.add_player_tournament,
                self.remove_player_tournament, self.menu_accueil]
        response = self.c_input()
        menu[int(response)-1]()

    def menu_tournament(self):
        self.console.tournament()
        menu = [self.new_tournament, self.load_tournament,
                self.save_tournament, self.menu_accueil]
        response = self.c_input()
        menu[int(response)-1]()

    def menu_rapport(self):
        self.console.rapport()
        response = self.c_input()
        menu[int(response)-1]()

    def save_tournament(self):
        response = self.c_input()
        menu[int(response)-1]()

    def add_player(self):
        pass

    def update_player(self):
        pass

    def add_player_tournament(self):
        pass

    def remove_player_tournament(self):
        pass

    def new_tournament(self):
        pass

    def load_tournament(self):
        pass

    def c_input(self, ask_input="Votre choix : ") -> str:
        self.response = input(ask_input)
        return self.response
