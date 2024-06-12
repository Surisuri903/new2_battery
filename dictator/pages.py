from ._builtin import Page, WaitPage
from .models import Constants
from random import randint


class Introduction(Page):
    pass


class Instructions1(Page):
    pass


class Instructions2(Page):
    def vars_for_template(self):
        const = Constants
        half_endowment = round(const.endowment / 2, 2)
        return dict(
            half_endowment=half_endowment, tripled=half_endowment * const.multiplier
        )


class WaitingPage(Page):
    def get_timeout_seconds(self):
        return randint(*Constants.waiting_page_seconds_range)


class WaitingPageChoice(Page):
    def get_timeout_seconds(self):
        range=[4,7]
        return randint(*range)


class Decision(Page):
    form_model = 'player'
    form_fields = ['sent']

    def before_next_page(self):
        self.player.set_payoff()


class Results(Page):
    def vars_for_template(self):
        return dict(
            other_payoff=self.player.sent * Constants.multiplier - 0.0
        )


page_sequence = [Introduction, Instructions1, Instructions2, WaitingPage, Decision, Results]
