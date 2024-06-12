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
    name_in_url = 'game_results'
    players_per_group = None
    num_rounds = 1

    comments = [
        'Where the instructions clear enough? If not,  where did you struggle?',
        'Did you find the practice rounds and comprehension questions helpful? Would you have needed more or less practice?',
        'What do you think the game was about?',
        'Did everything work well? Did you experience any technical problems?',
        'Anything else we can improve?'
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q_yr_planet = models.StringField()
    q_gb_planet = models.StringField()

    for n, c in enumerate(Constants.comments):
        locals()[f'feedback_{n+1}'] = models.LongStringField(label=c, blank=True)
    del n, c
