from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from random import randint


class Introduction(Page):
    def is_displayed(self):
        return True if self.round_number == 1 else False


class Instructions(Page):

    def vars_for_template(self):
        game_num, first_round, stop_round = self.player.get_game_params(Constants.bot_stop_nodes)
        self.participant.vars['timeout_happened'] = False
        self.participant.vars['go'] = True
        curr_node, nodes = self.player.get_nodes(Constants.bot_stop_nodes)
        return dict(nodes=nodes, num_nodes=len(nodes)-1, game_num=game_num, is_practice=False)
        #return dict(nodes=nodes, num_nodes=len(nodes)-1, game_num=game_num, is_practice=False)

    def is_displayed(self):
        game_num, first_round, stop_round = self.player.get_game_params(Constants.bot_stop_nodes)
        return self.round_number == first_round

    def before_next_page(self):
        game_num, first_round, stop_round = self.player.get_game_params(Constants.bot_stop_nodes)
        self.player.game_num = game_num


class WaitingPage(Page):
    def get_timeout_seconds(self):
        return randint(8, 18)

    def is_displayed(self):
        game_num, first_round, stop_round = self.player.get_game_params(Constants.bot_stop_nodes)
        return self.round_number == first_round


class YourTurn(Page):
    form_model = 'player'
    form_fields = ['go']

    template_name = 'centipede_training/Practice.html'

    timeout_seconds = Constants.max_seconds_to_decide

    def vars_for_template(self):
        return self.player.set_nodes_for_curr_round(Constants.bot_stop_nodes, False)

    def is_displayed(self):
        game_num, first_round, stop_round = self.player.get_game_params(Constants.bot_stop_nodes)
        return False if self.participant.vars['timeout_happened'] or self.participant.vars['go'] is False or self.round_number < first_round else True

    def before_next_page(self):
        game_num, first_round, stop_round = self.player.get_game_params(Constants.bot_stop_nodes)
        if self.round_number > first_round:
            self.player.game_num = self.player.in_round(self.round_number-1).game_num
        if self.timeout_happened:
            self.player.timeout_happened = True
            self.participant.vars['timeout_happened'] = True
            self.participant.vars[f'game_{game_num}'] = 0
            if not self.participant.vars.get('repeat_game_num'):
                self.participant.vars['repeat_game_num'] = game_num
        else:
            self.participant.vars['go'] = self.player.go


class FeedbackTimeout(Page):
    template_name = 'centipede_training/FeedbackTimeout.html'

    def vars_for_template(self):
        game_num, first_round, stop_round = self.player.get_game_params(Constants.bot_stop_nodes)
        num_games = len(Constants.num_nodes)
        game_rep = self.participant.vars.get('repeat_game_num', 0)
        is_last_node = (game_num == num_games and game_rep < num_games) or (game_rep == num_games and self.round_number > sum(Constants.bot_stop_nodes) / 2)
        return dict(is_practice=False, is_last_node=is_last_node)

    def is_displayed(self):
        return True if self.player.timeout_happened else False


class OtherTurn(Page):
    template_name = 'centipede_training/Practice.html'

    def get_timeout_seconds(self):
        return randint(4, 8)

    def vars_for_template(self):
        return self.player.set_nodes_for_curr_round(Constants.bot_stop_nodes, True)

    def is_displayed(self):
        game_num, first_round, stop_round = self.player.get_game_params(Constants.bot_stop_nodes)
        return False if self.participant.vars['timeout_happened'] or self.participant.vars['go'] is False or \
                        self.round_number < first_round else True

    def before_next_page(self):
        self.player.set_stop_by_bot(Constants.bot_stop_nodes)


class FeedbackEndGame(Page):
    template_name = 'centipede_training/FeedbackEndGame.html'

    def vars_for_template(self):
        return self.player.set_payoffs(Constants.bot_stop_nodes)

    def is_displayed(self):
        curr_node, nodes = self.player.get_nodes(Constants.bot_stop_nodes)
        curr_node += 1
        player = self.player
        is_end_game = self.participant.vars['timeout_happened'] is False and \
                      player.go is False or player.stop_by_bot \
                      or (curr_node == len(nodes)-1 and player.go)
        return True if is_end_game else False

    def app_after_this_page(self, upcoming_apps):
        if self.player.game_num == len(Constants.num_nodes):
            return upcoming_apps[0]


page_sequence = [Instructions, WaitingPage, YourTurn, FeedbackTimeout, OtherTurn, FeedbackEndGame]
