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

from centipede_utils import set_centipede_payoff_structure as set_nodes


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'intro'
    players_per_group = None
    num_rounds = 1

    num_nodes = 9
    nodes_example = set_nodes(4, 0, num_nodes, (-3, 7))

    pounds_per_point = c(0.1)
    max_seconds_per_decision = 15


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
