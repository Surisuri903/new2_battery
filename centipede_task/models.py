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
    name_in_url = 'centipede-task'
    players_per_group = None

    num_nodes = [20]
    bot_stop_nodes = [20]
    num_rounds = sum([n // 2 for n in bot_stop_nodes]) + max(num_nodes) // 2

    num_nodes_to_display = 5

    practice_first = [(5, 0), (1, 5), (10, 1), (2, 10), (15, 2), (3, 15), (20, 3), (4, 20), (25, 4), (5, 25), (30, 5), (6, 30), (35, 6), (7, 35), (40, 7), (8, 40), (45, 8), (9, 45), (50, 9), (10, 50), (15, 20)]
    # practice_first = set_nodes(7, 0, num_nodes[0]+1, (-6, 12))
    # practice_second = set_nodes(5, 0, num_nodes[1]+1, (-5, 10))
    # practice_third = set_nodes(8, 5, num_nodes[2]+1, (-8, 10))

    nodes = [practice_first] #, practice_second, practice_third]

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

    # This method assumes a set of games with equal length
    def get_game_params(self, nums_nodes):
        num_games = len(nums_nodes)
        nums_rounds = [n // 2 for n in nums_nodes]
        repeat_game_num = self.participant.vars.get('repeat_game_num', -1)
        r = self.round_number
        for n, num_rounds in enumerate(nums_rounds):
            game_num = n + 1
            e = num_rounds
            if game_num == 1:
                is_repeated = repeat_game_num == game_num
                if r <= num_rounds + e * is_repeated:
                    first_round = 1 + e * is_repeated
                    stop_round = first_round + e - 1
                    return game_num, first_round, stop_round
            elif game_num < num_games:
                prev_rounds = sum(nums_rounds[:n])
                prev_is_repeated = 1 <= repeat_game_num < game_num
                is_repeated = repeat_game_num == game_num
                if prev_rounds + e * prev_is_repeated < r <= prev_rounds + e * prev_is_repeated + num_rounds + e * is_repeated:
                    first_round = 1 + prev_rounds + e * prev_is_repeated + e * is_repeated
                    stop_round = first_round + e - 1
                    return game_num, first_round, stop_round
            elif game_num == num_games:
                first_round = 1 + sum(nums_rounds[:n])
                if repeat_game_num >= 1:
                    first_round += num_rounds
                stop_round = first_round - 1 + num_rounds
                return game_num, first_round, stop_round

    def get_nodes(self, nums_nodes):
        game_num, first_round, stop_round = self.get_game_params(nums_nodes)
        nodes = Constants.nodes[game_num-1]
        curr_node = 1 + self.round_number - first_round
        curr_node = (curr_node * 2) - 1
        return curr_node, nodes

    def set_nodes_for_curr_round(self, nums_nodes, is_bot_turn):
        game_num, first_round, stop_round = self.get_game_params(nums_nodes)
        curr_node, nodes = self.get_nodes(nums_nodes)
        if is_bot_turn:
            curr_node += 1
        is_stop_by_bot = curr_node == Constants.bot_stop_nodes[game_num - 1]
                         #and Constants.bot_stop_nodes[game_num - 1] < Constants.num_nodes[game_num - 1]
        nodes_to_display = nodes[:curr_node + 2] if curr_node <= int(Constants.num_nodes_to_display / 2) else \
            nodes[curr_node - 3:curr_node + 2]

        missing_nodes_for_display = max(Constants.num_nodes_to_display - len(nodes_to_display), 0)

        nodes_to_display = ['NA' for _ in range(missing_nodes_for_display)] + nodes_to_display if len(
            nodes) - curr_node > 1 else nodes_to_display
        display_last_node = False if len(nodes) - curr_node > 2 else True
        return dict(
            nodes_to_display=nodes_to_display,
            num_nodes=len(nodes),
            display_last_node=display_last_node,
            is_bot_turn=is_bot_turn,
            is_stop_by_bot=is_stop_by_bot
        )

    def set_stop_by_bot(self, nums_nodes):
        game_num, first_round, stop_round = self.get_game_params(nums_nodes)
        self.game_num = game_num
        curr_node, nodes = self.get_nodes(nums_nodes)
        curr_node += 1
        self.stop_by_bot = curr_node == Constants.bot_stop_nodes[game_num - 1] #\
                          # and Constants.bot_stop_nodes[game_num - 1] < Constants.num_nodes[game_num - 1]

    def set_payoffs(self, nums_nodes):
        curr_node, nodes = self.get_nodes(nums_nodes)
        curr_node = int(curr_node)
        if self.stop_by_bot or (curr_node + 1 == len(nodes) - 1 and self.go):
            curr_node += 1
        payoff_node = nodes[-1] if curr_node == len(nodes) else nodes[curr_node - 1]

        self.participant.vars['game_' + str(self.game_num)] = payoff_node[0] #\
         #   if self.stop_by_bot else payoff_node[0]
        game_num, first_round, stop_round = self.get_game_params(nums_nodes)
        is_last_node = game_num == len(Constants.nodes)
        return dict(payoff_node=payoff_node, is_last_node=is_last_node, is_practice=False)
