from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1


class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
        r = self.round_number
        options = Constants.options
        probs = [(round(r/10, 1), round(1-r/10, 1)) for _ in range(len(options))]
        return dict(options=list(zip(options, probs)))


class LotteryDraw(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.set_payoff()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Comments(Page):
    form_model = 'player'
    form_fields = ['comments']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [Instructions1, Instructions2, Decision,  LotteryDraw, Results]
