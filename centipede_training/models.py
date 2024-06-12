from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

from centipede_utils import set_centipede_payoff_structure as set_nodes


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'training'
    players_per_group = None

    num_nodes = [16, 8, 20]
    bot_stop_nodes = [4, 6, 16]
    num_rounds = sum([int(n/2) for n in bot_stop_nodes])

    num_nodes_to_display = 5
    
    practice_first = set_nodes(7, 3, num_nodes[0]+1, (-6, 10))
    practice_second = set_nodes(6, 1, num_nodes[1]+1, (-4, 7))
    practice_third = set_nodes(10, 1, num_nodes[2]+1, (-7, 11))
    
    nodes = [practice_first, practice_second, practice_third]

    max_seconds_to_decide = 15


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    game_num = models.IntegerField()
    go = models.BooleanField()
    stop_by_bot = models.BooleanField()
    timeout_happened = models.BooleanField()

    # This method assumes a set of three games
    def get_game_num(self, num_nodes):
        num_nodes = [n/2 for n in num_nodes]
        if self.round_number <= num_nodes[0]:
            game_num = 1
        elif num_nodes[0] < self.round_number <= num_nodes[0] + num_nodes[1]:
            game_num = 2
        else:
            game_num = 3
        return game_num

    # This method assumes a set of three games
    def get_nodes(self, num_nodes):
        game_num = self.get_game_num(num_nodes)
        num_nodes = [n/2 for n in num_nodes]
        if game_num == 1:
            curr_node = self.round_number
            nodes = Constants.nodes[0]
        elif game_num == 2:
            curr_node = self.round_number - num_nodes[0]
            nodes = Constants.nodes[1]
        else:
            curr_node = self.round_number - (num_nodes[0] + num_nodes[1])
            nodes = Constants.nodes[2]
        curr_node = (curr_node * 2) - 1
        return curr_node, nodes

    def set_nodes_for_curr_round(self, num_nodes, is_bot_turn):
        game_num = self.get_game_num(num_nodes)
        curr_node, nodes = self.get_nodes(num_nodes)
        if is_bot_turn:
            curr_node += 1
        is_stop_by_bot = curr_node == Constants.bot_stop_nodes[game_num-1] \
                           and Constants.bot_stop_nodes[game_num-1] < Constants.num_nodes[game_num-1]
        # TODO: check where curr_node becomes a float(!?)
        curr_node = int(curr_node)
        nodes_to_display = nodes[:curr_node+2] if curr_node <= int(Constants.num_nodes_to_display/2) else nodes[curr_node-3:curr_node+2]

        missing_nodes_for_display = max(Constants.num_nodes_to_display - len(nodes_to_display), 0)

        nodes_to_display = ['NA' for _ in range(missing_nodes_for_display)] + nodes_to_display if len(nodes) - curr_node > 1 else nodes_to_display
        display_last_node = False if len(nodes) - curr_node > 2 else True
        return dict(
            nodes_to_display=nodes_to_display,
            num_nodes=len(nodes),
            display_last_node=display_last_node,
            is_bot_turn=is_bot_turn,
            is_stop_by_bot=is_stop_by_bot
        )

    def set_stop_by_bot(self, num_nodes):
        game_num = self.game_num
        curr_node, nodes = self.get_nodes(num_nodes)
        curr_node += 1
        self.stop_by_bot = curr_node == Constants.bot_stop_nodes[game_num-1] \
                           and Constants.bot_stop_nodes[game_num-1] < Constants.num_nodes[game_num-1]

    def set_payoffs(self):
        curr_node, nodes = self.get_nodes(Constants.bot_stop_nodes)
        curr_node = int(curr_node)
        if self.stop_by_bot or (curr_node + 1 == len(nodes) - 1 and self.go):
            curr_node += 1
        payoff_node = nodes[-1] if curr_node == len(nodes) - 1 else nodes[curr_node - 1]
        self.participant.vars['game_' + str(self.game_num)] = payoff_node[1] \
            if self.stop_by_bot else payoff_node[0]
        stop_rounds = [n / 2 for n in Constants.bot_stop_nodes]
        is_last_node = self.round_number >= stop_rounds[0] + stop_rounds[1] + 1
        return dict(payoff_node=payoff_node, is_last_node=is_last_node, is_practice=True)


