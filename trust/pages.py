from otree.api import Currency as c, currency_range
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


class Quiz1(Page):
    form_model = 'player'
    form_fields = ['q1']


class QuizFeedback1(Page):
    form_model = 'player'
    form_fields = ['q1']

class Quiz2(Page):
    form_model = 'player'
    form_fields = ['q2']


class QuizFeedback2(Page):
    form_model = 'player'
    form_fields = ['q2']


class Quiz3(Page):
    form_model = 'player'
    form_fields = ['q3']


class QuizFeedback3(Page):
    form_model = 'player'
    form_fields = ['q3']


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
            other_payoff=self.player.sent * Constants.multiplier - self.player.returned
        )


page_sequence = [
    Introduction,
    Instructions1,
    Instructions2,
    Quiz1,
    QuizFeedback1,
    Quiz2,
    QuizFeedback2,
    Quiz3,
    QuizFeedback3,
    WaitingPage,
    Decision,
    WaitingPageChoice,
    Results
]
