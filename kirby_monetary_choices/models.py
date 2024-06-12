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


class Constants(BaseConstants):
    name_in_url = 'kirby'
    players_per_group = None

    questions = [(54, 55, 117), (55, 75, 61), (19, 25, 53), (31, 85, 7), (14, 25, 19), (47, 50, 160),
                 (15, 35, 13), (25, 60, 14), (35, 20, 35), (78, 80, 162), (40, 55, 62), (11, 30, 7), (67, 75, 119),
                 (34, 35, 186), (27, 50, 21), (69, 85, 91), (49, 60, 89), (80, 54, 12), (80, 85, 157), (24, 35, 29),
                 (33, 80, 14), (28, 30, 179), (34, 50, 30), (25, 30, 80), (41, 75, 20), (77, 55, 61), (54, 60, 111),
                 (54, 80, 30), (22, 25, 136), (20, 55, 7)]
    num_questions = len(questions)

    # TODO: Convert to single round using live pages to be better compatible with full battery?
    num_rounds = num_questions


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    b_today = models.IntegerField()
    b_later = models.IntegerField()
    num_days = models.IntegerField()
    q = models.BooleanField()
