# coding: utf-8

from models import rounds


class Match:
    """ Classe pour instancier les matchs"""
    def __init__(self, **kwargs):
        self.players = [kwargs["player_a"], kwargs["player_b"]]
        self.score = [kwargs["score_a"], kwargs["score_b"]]

    def __repr__(self):
        """Retour un un tuple avec 2 listes celle des joueurs et celles des resultat"""
        return str((self.players, self.score))

if __name__ == '__main__':
    round = {'player_a': 'WALDNER', 'player_b': 'BREDERECK', 'score_a': 1, 'score_b': 0}
    m = Match(**round)
    print(m)
    t = rounds.Tour()
    t.add_match(m)
    print(t)