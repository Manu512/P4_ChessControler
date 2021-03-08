"""Base Class"""
# coding: utf-8

import re
from typing import Union
from views.views import Display


class BaseController:
    """
    Base Class
    """
    def __init__(self):
        self.view_menu = Display()
        self.tournament = None
        self.round = None

    # --------------------------GENERAL METHODS------------------------------------

    def ask_and_launch(self, ask_input="Votre choix : ", *, menu: dict):
        """
        Methode pour interagir avec l'utilisateur, contrôler sa réponse
        et définir la suite des évènements. En fonction des menus qui lui sont
        présenté.

        Methode Arguments :
        self : instance
        ask_input : Texte qui sera demandé
        menu : argument nommé qui contient un dictionnaire
        dict{int(x):(tuple(Methode à lancer, Choix à afficher)}
        """
        user_input = input(ask_input)

        if dict is not None:
            menu_to_analyse = menu
            try:
                user_input = int(user_input)
            except ValueError:
                self.ask_and_launch(ask_input, menu=menu)

            if self._check_choice(list(menu.keys()), user_input):
                menu[user_input][0]()
            else:
                self.ask_and_launch(ask_input, menu=menu_to_analyse)

    def _check_choice(self, menu: list, response: int) -> bool:
        if response not in list(menu):
            self.view_menu.error_msg("Choix incorrect !! Veuillez ressaisir")
            self.input_press_continue()
            return False
        else:
            return True

    def ask_and_store_text(self, ask_input='Votre saisie : ') -> tuple[bool, str]:
        user_input = input(ask_input)

        if self._control_user_input('text', user_input):
            return True, user_input
        else:
            return False, user_input

    def ask_and_store_number(self, ask_input='Votre saisie : ') -> Union[tuple[bool, int], tuple[bool, str]]:
        user_input = input(ask_input)

        if self._control_user_input('number', user_input):
            return True, int(user_input)
        else:
            return False, user_input

    # -------------------------CONTROL METHODS---------------------------------

    def _control_user_input(self, question, response) -> bool:
        # Controle presence de chiffre dans le name/firstname
        if question in ['name', 'first_name', 'text']:
            if self.__check_number_in_word(response):
                self.view_menu.error_msg('Saisi non valide !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
        if question == 'sentence':
            if self.__check_sentence(response) < 2:
                self.view_menu.error_msg('Saisie non valide !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
        elif question == 'dob':
            # Controle le format de la date de naissance
            try:
                dt.strptime(response, '%d/%m/%Y')
            except ValueError:
                self.view_menu.error_msg('Veuillez saisir une date de naissance'
                                         ' valide !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
        elif question == '_genre':
            if response not in ['H', 'F']:
                self.view_menu.error_msg('Genre saisi non valide !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
        elif question == 'bool':
            if response not in ['O', 'N']:
                self.view_menu.error_msg('Réponse non valide !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
        elif question == 'number':
            try:
                int(response)
            except ValueError:
                self.view_menu.error_msg('Veuillez saisir un nombre entier !\nVeuillez ressaisir !')
                self.input_press_continue()
                return False
            else:
                if int(response) < 0:
                    self.view_menu.error_msg('Veuillez saisir un nombre entier !'
                                             '\nVeuillez ressaisir !')
                    self.input_press_continue()
                    return False
        return True

    @staticmethod
    def input_press_continue():
        input("Pressez une touche pour continuer...")

    @staticmethod
    def __check_number_in_word(string):
        """ Verification d'absence de chiffre dans
         la variable passé en paramètre """
        chiffre_pattern = re.compile('[0-9]')
        return re.search(chiffre_pattern, string)

    @staticmethod
    def __check_sentence(string):
        """ Verification d'absence de chiffre dans
         la variable passé en paramètre """
        sentence_pattern = re.compile('[a-z]+')
        return len([*re.finditer(sentence_pattern, string)])