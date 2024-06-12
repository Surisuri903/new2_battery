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

import random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'bart'
    players_per_group = None
    num_blocks = 2
    num_balloons_per_block = 10
    num_rounds = num_balloons_per_block * num_blocks

    max_num_pumps = 128
    break_points_array = list(range(1, 128+1))
    points_per_pump = 1

    sec_delay_submit = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            arrays = []
            for n in range(Constants.num_blocks):
                random.seed(n)
                array = [1]
                while sum(array) / len(array) != 64:
                    array = random.sample(Constants.break_points_array, Constants.num_balloons_per_block)
                arrays.extend(array)
            self.session.vars['breakpoints'] = arrays


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_pumps = models.IntegerField()
    is_exploded = models.BooleanField()
    points = models.CurrencyField(initial=0)
    
    def set_payoff(self):
        if self.round_number == Constants.num_rounds:
            self.participant.vars['bart_payoff'] = sum(p.points for p in self.in_all_rounds()) * 0.01
            self.participant.payoff = self.participant.vars['bart_payoff']
