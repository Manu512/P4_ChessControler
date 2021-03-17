""" Main launch """
# coding: utf-8

import logging

from controllers.controller import Controller


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    tournament = Controller()
    try:
        while True:
            tournament.menu_accueil()
    except Exception as exc:
        print(type(exc))  # the exception instance
        print(exc.args)  # arguments stored in .args
        print(exc)

    finally:
        print("\n" * 10)
        print("Merci d'etre passé ;o)")
