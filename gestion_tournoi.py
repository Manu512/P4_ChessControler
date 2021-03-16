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
        logging.error(f"Problem with execution. Msg : {exc}")
    finally:
        print("\n" * 10)
        print("Merci d'etre passé ;o)")
