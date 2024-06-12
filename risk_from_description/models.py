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

from random import randint, choices


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'risk_from_description'
    players_per_group = None
    num_rounds = 10

    example = [((c(1), 0.1), (c(0.4), 0.9)), ((c(4.5), 0.2), (c(1), 0.8))]
    options = [(2, 1.6), (3.85, 0.10)]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision = models.BooleanField()
    decision_to_pay = models.IntegerField()
    risk_from_description_payoff = models.FloatField()

    def set_payoff(self):
        d = randint(1, Constants.num_rounds)
        self.decision_to_pay = d
        option = Constants.options[self.in_round(d).decision]
        payoff = choices(option, weights=[d/10, 1-d/10])[0]
        self.participant.vars['risk_from_description_payoff'] = payoff
        self.participant.payoff += payoff
        self.risk_from_description_payoff = payoff


    comments = models.LongStringField(
        label="This is a pilot run of the task. We would appreciate any feedback you have for us "
              "(did everything work alright, were instructions clear, … anything you think could be improved):",
        blank=True
    )
