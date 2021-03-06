# coding: utf-8

import logging
from controllers.control import Main_Controler


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    try:
        while True:
            tournament = Main_Controler()
    except Exception as e:
        logging.error(f"Problem with execution. Msg : {e}")
    finally:
        print("\n" * 120)
        print("Merci d'etre passé ;o)")
