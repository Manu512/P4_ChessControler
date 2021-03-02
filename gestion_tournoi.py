# coding: utf-8

import logging
from controllers.controller import Controller


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    try:
        tournament = Controller()
        print("\n" * 120)
        print("Merci d'etre passé ;o)")
    except Exception as e:
        logging.error(f"Probleme lors d'execution. Msg : {e}")
