from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1

class Instructions(Page):
    def vars_for_template(self):
        return dict(nodes=Constants.nodes_example)


page_sequence = [Welcome, Instructions]
