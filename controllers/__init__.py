"""Base Class"""
# coding: utf-8

import re
from typing import Union
from datetime import datetime as dt

from views.views import Display


class BaseController:
    """
    Base Class
    """
    def __init__(self, tournament=None):
        self.view_menu = Display()
        self.tournament = tournament
        self.round = None

    # --------------------------GENERAL METHODS------------------------------------

    @staticmethod
    def back_menu():
        """
        Method that returns True
        """
        return True

    def ask_and_launch(self, ask_input="Votre choix : ", *, menu: dict) -> bool:
        """
        Method for interacting with the user, controlling their response
        and define the sequence of events. According to the menus that are
        presented.

        Methode Arguments :
        self : instance
        ask_input : Text that will be asked
        menu : named argument that contains a dictionary
        dict{int(x):(tuple(Method to be launched, Choice to be displayed)}
        """
        user_input = self.view_menu.input(ask_input)

        if dict is not None:
            menu_to_analyse = menu
            try:
                user_input = int(user_input)
            except ValueError:
                self.ask_and_launch(ask_input, menu=menu)
            if menu[user_input][0] == "back":
                return True
            elif self.check_choice(list(menu.keys()), user_input):
                menu[user_input][0]()
            else:
                self.ask_and_launch(ask_input, menu=menu_to_analyse)

    def check_choice(self, menu: list, response: int) -> bool:
        """
        Control method for the choice entered by the user
        Args:
            menu: list
            response: str : user entry

        Returns: bool True if valid else False
        """
        if response not in list(menu):
            self.view_menu.stand_by_msg("Choix incorrect !! Veuillez ressaisir")
            ret = False
        else:
            ret = True
        return ret

    def ask_and_store_text(self, ask_input='Votre saisie : ') -> tuple[bool, str]:
        """
        Validation method when entering text.
        Args:
            ask_input:

        Returns: tuple(bool, user_entry)
        """
        user_input = self.view_menu.input(ask_input)

        ret = bool(self._control_user_input('text', user_input))

        return ret, user_input

    def ask_and_store_number(self, ask_input='Votre saisie : ') -> Union[tuple[bool, int], tuple[bool, str]]:
        """
        Validation method when entering number.
        Args:
            ask_input:

        Returns: Union[tuple[bool, int], tuple[bool, str]]
        tuple[bool, int] if valid input
        tuple[bool, str] if invalid input
        """
        user_input = self.view_menu.input(ask_input)

        if self._control_user_input('number', user_input):
            ret = True, int(user_input)
        else:
            ret = False, user_input

        return ret

    # -------------------------CONTROL METHODS---------------------------------

    def _control_user_input(self, question, response) -> bool:

        if question in ['name', 'first_name', 'text']:  # Checking for numbers in name/firstname
            if self.__check_number_in_word(response):
                self.view_menu.stand_by_msg('Saisi non valide !\nVeuillez ressaisir !')
                return False
        elif question == 'sentence':    # Check if more than one word is present
            if self.__check_sentence(response) < 2:
                self.view_menu.stand_by_msg('Saisie non valide !\nVeuillez ressaisir !')
                return False
        elif question == 'dob':     # Check the date of birth
            try:
                dt.strptime(response, '%d/%m/%Y')
            except ValueError:
                self.view_menu.stand_by_msg('Veuillez saisir une date de naissance'
                                            ' valide !\nVeuillez ressaisir !')
                return False
        elif question == '_genre':  # Checks whether the gender entry is correct.
            if response not in ['H', 'F']:
                self.view_menu.stand_by_msg('Genre saisi non valide !\nVeuillez ressaisir !')
                return False
        elif question == 'bool':
            if response not in ['O', 'N']:  # Checks whether the Y/N entry is correct.
                self.view_menu.stand_by_msg('Réponse non valide !\nVeuillez ressaisir !')
                return False
        elif question == 'number':  # Checks the number entered when entering the Elo ranking
            try:
                int(response)
            except ValueError:
                self.view_menu.stand_by_msg('Veuillez saisir un nombre entier !\nVeuillez ressaisir !')
                return False
            else:
                if int(response) < 0:
                    self.view_menu.stand_by_msg('Veuillez saisir un nombre positif !'
                                                '\nVeuillez ressaisir !')
                    return False
        return True

    @staticmethod
    def __check_number_in_word(string: str):
        """ Verification of the absence of a number in the variable passed in parameter """
        chiffre_pattern = re.compile('[0-9]')
        return re.search(chiffre_pattern, string)

    @staticmethod
    def __check_sentence(string: str) -> int:
        """Counting the number of words in the argument variable"""
        sentence_pattern = re.compile('[a-z]+')
        return len([*re.finditer(sentence_pattern, string)])
