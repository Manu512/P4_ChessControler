# coding: utf-8

import logging
from controllers.controller import Controller


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    try:
        while True:
            tournament = Controller()
    except Exception as e:
        logging.error(f"Problem with execution. Msg : {e}")
    finally:
        print("\n" * 120)
        print("Merci d'etre passé ;o)")