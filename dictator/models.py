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


doc = """
One player decides how to divide a certain amount between himself and the other
player.

See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.

"""


class Constants(BaseConstants):
    name_in_url = 'dictator'
    players_per_group = None
    num_rounds = 1

    endowment = c(5)
    multiplier = 3

    waiting_page_seconds_range = [8, 18]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sent = models.CurrencyField(label="I will send", min=0, max=Constants.endowment)

    def set_payoff(self):
        self.payoff = Constants.endowment - self.sent
