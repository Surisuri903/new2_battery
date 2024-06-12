from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['q']

    def vars_for_template(self):
        q = Constants.questions[self.round_number-1]
        self.player.b_today, self.player.b_later, self.player.num_days = q[0], q[1], q[2]
        return dict(bonus_today=q[0], bonus_later=q[1], num_days=q[2], q_name='q')


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [Introduction, Decision, Results]
