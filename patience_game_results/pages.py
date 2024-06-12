from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Results(Page):
    pass


class Comments(Page):
    form_model = 'player'
    form_fields = ['feedback_1', 'feedback_2', 'feedback_3', 'feedback_4', 'feedback_5']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class DebriefSheet(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


#page_sequence = [Comments, DebriefSheet]
page_sequence = [Results, DebriefSheet]
