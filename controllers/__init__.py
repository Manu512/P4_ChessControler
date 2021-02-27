# coding: utf-8
import models
import views
import re
import datetime as dt


def main():
    conf_tournoi = views.lancement()
    print(conf_tournoi)


def liste_joueur():
    pass


def add_player():
    player = views.joueurs.add_new_player()
    return models.Player(**player)


def controle_player_data(question: str, response: str) -> bool:
    # Controle presence de chiffre dans le nom/fname
    if question in ['Nom','Prenom']:
        if check_number_in_word(response):
            print('Nom/Prénom saisi non valide !\nVeuillez resaissir !')
            return False

    if question == 'Date de Naissance':
    # Controle le format de la date de naissance
        try:
            dt.datetime.strptime(response, '%d/%m/%Y')
        except ValueError:
            print('Veuillez saisir une date de naissance valide !\nVeuillez resaissir !')
            return False
    # if question == 'Sexe':
    #     if response not in ['M', 'F']:
    #         print('Genre saisi non valide !\nVeuillez resaissir !')
    #         return False
    if question == 'Classement':
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
    chiffre_pattern = re.compile("\d")
    return re.search(chiffre_pattern, string)


if __name__ == '__main__':
    p = []
    print("Debut du tournoi ....")
    p.append(add_player())
    print("")
    p[0].age

