from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Your name here'

doc = """
Your app description
"""

from random import randint


class Constants(BaseConstants):
    name_in_url = 'results'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    game_repeated = models.IntegerField()
    game_first_payoff = models.CurrencyField()
    #game_second_payoff = models.CurrencyField()
   # game_third_payoff = models.CurrencyField()
    game_for_payment = models.IntegerField()

    def set_payoffs(self):
        games = ['first'] #, 'second']
        for n, name in enumerate(games):
            setattr(self, f'game_{name}_payoff', self.participant.vars[f'game_{n+1}'])
        #i = randint(1, len(games))
        self.game_for_payment = 1#i
        self.participant.payoff = self.participant.vars[f'game_{1}']
