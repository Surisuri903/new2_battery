from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class Task(Page):
    live_method = 'live_task'

    def vars_for_template(self):
        doors_params = self.session.vars['all_doors'][self.round_number-1][self.player.num_rep]
        pair_number, values, order = doors_params['pair'], doors_params['values'], doors_params['order']
        doors = [{'type': o, 'value': values[o], 'url': f'{Constants.imgs_base_url}{pair_number}_{o}.jpg'} for o in order]

        if not self.player.pair:
            self.player.pair = pair_number

        return dict(pair_number=pair_number, doors=doors)

    def before_next_page(self):
        self.player.set_payoff()
        self.player.reset_pvars()


class EndOfRound(Page):
    def is_displayed(self):
        return self.round_number < Constants.num_rounds


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Comments(Page):
    form_model = 'player'
    form_fields = ['comments']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class DebriefSheet(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [Welcome, Instructions, Task, EndOfRound, Results]
