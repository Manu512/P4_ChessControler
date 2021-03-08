# coding: utf-8

import logging
from controllers.controller import Controller


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    tournament = Controller()
    try:
        while True:
            tournament.menu_accueil()
    except Exception as e:
        logging.error(f"Problem with execution. Msg : {e}")
    finally:
        print("\n" * 10)
        print("Merci d'etre passé ;o)")
