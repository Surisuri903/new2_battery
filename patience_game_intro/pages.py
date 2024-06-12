from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):
    pass

class Instructions(Page):
    def is_displayed(self):
        return self.player.round_number == 1

class Instructions2(Page):
    def is_displayed(self):
        return self.player.round_number == 1

class Practice(Page):
    def vars_for_template(self):
        if self.player.round_number == 1:
            dir = 1
        elif self.player.round_number == 2:
            dir = 0
        return dict (
            round=self.player.round_number,
            dir=dir
        )

    def is_displayed(self):
        return self.player.round_number <= 1


page_sequence = [ Instructions, Instructions2, Practice]
