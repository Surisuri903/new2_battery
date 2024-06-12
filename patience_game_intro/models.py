from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as cu,
    currency_range,
)

author = 'Kathy Lau'

doc = """
On Prolific Academy, add ?participant_label={{%PROLIFIC_PID%}} to session wide link
"""

class Constants(BaseConstants):
    name_in_url = 'boat_intro'
    players_per_group = None
    exchange_rate = 0.05
    num_rounds = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    direction = models.BooleanField(label='Direction', initial=0, choices=[(1, 'Left'), (0, 'Right')])
    points = models.IntegerField(initial=0)
    bonus = models.CurrencyField()

    def set_direction(self, dir):
        self.direction = dir

    def set_points(self, num_points):
        self.points = num_points

    def set_payoff(self, new_points):
        self.payoff += cu(new_points/10)
