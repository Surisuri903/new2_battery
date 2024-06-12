from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class GamesResults(Page):
    def vars_for_template(self):
        payoff = self.participant.vars.get('game_1')/10#,
         #          self.participant.vars.get('game_2')]
          #         self.participant.vars.get('game_3')]
        return dict(payoff=payoff)

    def before_next_page(self):
        self.player.game_repeated = self.participant.vars.get('repeat_game_num')
        self.player.set_payoffs()


class FinalResults(Page):
    def vars_for_template(self):
        return dict(payoff=self.participant.payoff.to_real_world_currency(self.session))


page_sequence = [GamesResults]#, FinalResults]
