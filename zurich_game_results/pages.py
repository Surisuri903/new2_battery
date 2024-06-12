from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Results(Page):
    form_model = 'player'
    form_fields = ['q_yr_planet', 'q_gb_planet']

    def vars_for_template(self):
        self.player.payoff = self.participant.vars.get('game_bonus')
        return dict(bonus=self.participant.vars.get('game_bonus'))


class Comments(Page):
    form_model = 'player'
    form_fields = ['feedback_1', 'feedback_2', 'feedback_3', 'feedback_4', 'feedback_5']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class DebriefSheet(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [Comments, DebriefSheet]
