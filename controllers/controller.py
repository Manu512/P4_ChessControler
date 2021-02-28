"""Controller"""
# coding:utf-8

import re
from datetime import datetime as dt
from tinydb import TinyDB
from models.players import Player
from views.views import ViewMenu


class Controller:

    def __init__(self):
        Player.load_players()
        self.view_menu = ViewMenu()
        self.menu_accueil()

    def menu_accueil(self):
        self.view_menu.accueil()
        menu = [self.menu_tournament, self.menu_players,
                self.menu_rapport, exit]
        response = self.c_input()
        menu[int(response)-1]()
        self.menu_accueil()

    def menu_players(self):
        self.view_menu.players()
        menu = [self.add_player, self.update_player_elo,
                self.add_player_tournament,
                self.remove_player_tournament, self.menu_accueil]
        response = self.c_input()
        menu[int(response)-1]()
        self.menu_players()

    def menu_tournament(self):
        self.view_menu.tournament()
        menu = [self.new_tournament, self.load_tournament,
                self.save_tournament, self.menu_accueil]
        response = self.c_input()
        menu[int(response)-1]()
        self.menu_tournament()

    def menu_rapport(self):
        self.view_menu.rapport()
        menu = [self.list_all_players, self.list_tournament_players,
                self.list_tournaments, self.list_all_rounds,
                self.list_all_matchs, self.menu_accueil]
        response = self.c_input()
        menu[int(response)-1]()
        self.menu_rapport()

# --------------------------PLAYERS METHODS------------------------------------

    def add_player(self):
        """
        Affiche le menu add_player
        Boucle pour chaque information à récupérer
        Nom (name), Prénom (firstname), Date de Naissance (dob), sexe (_genre)
        Puis crée un nouveau joueur et sauvegarde la liste.
        """
        choice = ('name', 'first_name', 'dob', '_genre')
        response = []
        menu = self.view_menu.add_player()
        for m in range(len(choice)):
            res = self.c_input(menu[m][2:] + ' : ')
            while not controle_data_input(choice[m], res):
                res = self.c_input(menu[m][2:] + ' : ')
            response.append(res)
            res = dict(zip(choice, response))
        Player(**res)
        Player.save_players()
        self.menu_players()

    def update_player_elo(self):
        """
        1° Demande du nom et du prenom du joueur
        2° Recherche du joueur
        3° Affichage du classement actuel
        4° Input pour le nouveau classement
        """
        self.player = self.found_specific_player()
        res = self.c_input("Veuillez renseigner le nouveau classement ELO : ")
        while not controle_data_input('elo', res):
            res = self.c_input("Veuillez renseigner le nouveau classement ELO : ")
        self.player.elo = res
        Player.save_players()


    def add_player_tournament(self):
        """
        1° Demande du nom et du Prenom du joueur
        2° Recherche du joueur s'il n'est pas déjà actif dans le tournoi
        3° Demande validation quant au passage du status à 1
        """
        pass


    def remove_player_tournament(self):
        """
        1° Demande du nom et du Prenom du joueur
        2° Recherche du joueur s'il n'est pas déjà inactif dans le tournoi
        3° Demande validation quant au passage du status à 1
        """
        pass

    def found_specific_player(self):
        search_question = ('Nom du joueur recherché : ',
                           'Prénom du joueur recherché : ')
        search_response = []
        for question in search_question:
            res = self.c_input(question)
            while not controle_data_input('text', res):
                res = self.c_input(question)
            search_response.append(res)

        for player in Player.PLAYERS:
            if player.name == search_response[0] and player.first_name == search_response[1]:
                return player
            else:
                self.found_specific_player()

# --------------------------TOURNAMENTS METHODS--------------------------------

    def new_tournament(self):
        pass

    def load_tournament(self):
        pass

    def save_tournament(self):
        pass

# --------------------------RAPPORT METHODS------------------------------------

    def list_all_players(self):
        """
        Fonction qui va lancer le print de la liste des joueurs connus
        """
        Player.list_all_player()

    def list_tournament_players(self):
        """
        Fonction qui va lancer le print de la liste des joueurs du tournois
        """
        pass

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
        Fonction qui va lancer le print de la liste des matchs du tournois
        """
        pass

# --------------------------GENERAL METHODS------------------------------------

    def c_input(self, ask_input="Votre choix : "):
        self.response = input(ask_input)
        return self.response

def controle_data_input(question, response) -> bool:
    # Controle presence de chiffre dans le name/firstname
    if question in ['name', 'firstname', 'text']:
        if check_number_in_word(response):
            print('Nom/Prénom saisi non valide !\nVeuillez resaissir !')
            return False

    if question == 'dob':
        # Controle le format de la date de naissance
        try:
            dt.strptime(response, '%d/%m/%Y')
        except ValueError:
            print('Veuillez saisir une date de naissance valide !\nVeuillez resaissir !')
            return False
    if question == '_genre':
        if response not in ['H', 'F']:
            print('Genre saisi non valide !\nVeuillez resaissir !')
            return False
    if question == 'elo':
        try:
            int(response)
        except ValueError:
            print('Veuillez saisir un entier pour le elo !\nVeuillez resaissir !')
            return False
        else:
            if int(response) < 0:
                print('Veuillez saisir un entier positif pour le elo ! \nVeuillez resaissir !')
                return False
    return True


def check_number_in_word(string):
    """ Verification d'absence de chiffre dans la variable passé en parametre """
    chiffre_pattern = re.compile('\d')
    return re.search(chiffre_pattern, string)
