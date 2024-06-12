from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from random import randint


class Instructions(Page):
    def vars_for_template(self):
        game_num = self.player.get_game_num(Constants.bot_stop_nodes)
        self.participant.vars['timeout_happened'] = False
        self.participant.vars['go'] = True
        curr_node, nodes = self.player.get_nodes(Constants.bot_stop_nodes)
        return dict(nodes=nodes, num_nodes=len(nodes)-1, game_num=game_num, is_practice=True)

    def is_displayed(self):
        stop_rounds = [n/2 for n in Constants.bot_stop_nodes]
        return self.round_number in (1, stop_rounds[0]+1, stop_rounds[0]+stop_rounds[1]+1)


class PracticeYourTurn(Page):
    form_model = 'player'
    form_fields = ['go']

    template_name = 'centipede_training/Practice.html'

    timeout_seconds = Constants.max_seconds_to_decide

    def vars_for_template(self):
        return self.player.set_nodes_for_curr_round(Constants.bot_stop_nodes, False)

    def is_displayed(self):
        return False if self.participant.vars['timeout_happened'] or self.participant.vars['go'] is False else True

    def before_next_page(self):
        self.player.game_num = self.player.get_game_num(Constants.bot_stop_nodes)
        if self.timeout_happened:
            self.player.timeout_happened = True
            self.participant.vars['timeout_happened'] = True
        else:
            self.participant.vars['go'] = self.player.go


class FeedbackTimeout(Page):
    def vars_for_template(self):
        stop_rounds = [n / 2 for n in Constants.bot_stop_nodes]
        is_last_node = self.round_number >= stop_rounds[0] + stop_rounds[1] + 1
        return dict(is_practice=True, is_last_node=is_last_node)

    def is_displayed(self):
        return True if self.player.timeout_happened else False


class PracticeOtherTurn(Page):
    template_name = 'centipede_training/Practice.html'

    def get_timeout_seconds(self):
        return randint(4, 8)

    def vars_for_template(self):
        return self.player.set_nodes_for_curr_round(Constants.bot_stop_nodes, True)

    def is_displayed(self):
        return False if self.participant.vars['timeout_happened'] or self.participant.vars['go'] is False else True

    def before_next_page(self):
        self.player.set_stop_by_bot(Constants.bot_stop_nodes)


class FeedbackEndGame(Page):
    def vars_for_template(self):
        return self.player.set_payoffs()

    def is_displayed(self):
        curr_node, nodes = self.player.get_nodes(Constants.bot_stop_nodes)
        curr_node += 1
        is_end_game = self.participant.vars['timeout_happened'] is False \
                      and self.player.go is False or self.player.stop_by_bot \
                      or (curr_node == len(nodes)-1 and self.player.go)
        return True if is_end_game else False


page_sequence = [Instructions, PracticeYourTurn, FeedbackTimeout, PracticeOtherTurn, FeedbackEndGame]
