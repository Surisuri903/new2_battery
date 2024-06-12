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

from json import loads


author = 'Tommaso Batistoni - t.batistoni@ucl.ac.uk'

doc = """
Tower of London Test
"""


class Constants(BaseConstants):
    name_in_url = 'tower_of_london'
    players_per_group = None

    # Configurations for Practice rounds
    practice_starts = [{51: [['Y'], ['R', 'B'], []]}, {23: [['R', 'B'], ['Y'], []]}]
    practice_goals = [{63: [['B', 'R', 'Y'], [], []]}, {35: [['B'], ['Y'], ['R']]}]
    practice_min_moves = [4, 3]
    practice_configurations = [{'start': s, 'goal': g, 'min_moves': m} for s, g, m in
                               zip(practice_starts, practice_goals, practice_min_moves)]

    # Configurations for Task rounds
    starts = [{54: [['Y'], ['R', 'B'], []]}, {42: [['B', 'Y'], [], ['R']]}, {34: [['B'], ['Y', 'R'], []]},
              {12: [['R', 'Y'], [], ['B']]}, {55: [['Y'], ['R'], ['B']]}, {16: [[], ['B', 'R'], ['Y']]},
              {25: [['R'], ['Y'], ['B']]}, {36: [[], ['Y', 'B'], ['R']]}, {33: [['B', 'R'], [], ['Y']]},
              {53: [['Y', 'B'], ['R'], []]}, {23: [['R'], ['B'], ['Y']]}, {55: [['Y'], ['R'], ['B']]},
              {42: [['Y', 'B'], [], ['R']]}, {54: [['Y'], ['R', 'B'], []]}, {52: [['Y', 'B'], [], ['R']]},
              {55: [['Y'], ['R'], ['B']]}, {22: [['R', 'B'], [], ['Y']]}, {34: [['B'], ['Y', 'R'], []]},
              {42: [['B', 'Y'], [], ['R']]}, {46: [[''], ['R', 'B'], ['Y']]}, {23: [['R', 'B'], ['Y'], []]},
              {43: [['B', 'Y'], ['R'], []]}, {13: [['R', 'Y'], ['B'], []]}, {22: [['R', 'B'], [], ['Y']]}
              ]
    goals = [{31: [['B', 'R', 'Y'], [], []]}, {23: [['R', 'B'], ['Y'], []]}, {13: [['R', 'Y'], ['B'], []]},
             {65: [['Y'], ['B'], ['R']]}, {41: [['B', 'Y', 'R'], [], []]}, {24: [['R'], ['Y', 'B'], []]},
             {32: [['B', 'R'], [], ['Y']]}, {15: [['R'], ['B'], ['Y']]}, {11: [['R', 'Y', 'B'], [], []]},
             {13: [['R', 'Y'], ['B'], []]}, {43: [['B', 'Y'], ['R'], []]}, {15: [['R'], ['B'], ['Y']]},
             {21: [['R', 'B', 'Y'], [], []]}, {34: [['B'], ['Y', 'R'], []]}, {12: [['R', 'Y'], [], ['B']]},
             {35: [['B'], ['Y'], ['R']]}, {41: [['B', 'Y', 'R'], [], []]}, {53: [['Y', 'B'], ['R'], []]},
             {63: [['Y', 'R'], ['B'], []]}, {25: [['R'], ['Y'], ['B']]}, {61: [['Y', 'R', 'B'], [], []]},
             {64: [['Y'], ['B', 'R'], []]}, {32: [['B', 'R'], [], ['Y']]}, {55: [['Y'], ['R'], ['B']]}
             ]
    min_moves = [4 for _ in range(8)] + [5 for _ in range(8)] + [6 for _ in range(8)]
    difficulty_level = [1, 0, 1, 0, 1, 0, 1, 0, 2, 1, 2, 1, 2, 1, 2, 1, 3, 2, 3, 2, 3, 2, 3, 2]

    configurations = [{'start': s, 'goal': g, 'min_moves': m, 'diff_level': l} for s, g, m, l in
                      zip(starts, goals, min_moves, difficulty_level)]
    num_rounds = len(configurations)

    # Bonus and loss are expressed in pences
    bonus_per_trial = 20
    loss_per_extra_move = 2

    time_limit = 1

    participation_fee = c(3.75)


class Subsession(BaseSubsession):
    def creating_session(self):
        curr_config = Constants.configurations[self.round_number - 1]
        for p in self.get_players():
            p.config_num = self.round_number
            p.start_state = list(curr_config['start'].keys())[0]
            p.goal_state = list(curr_config['goal'].keys())[0]
            p.min_moves = curr_config['min_moves']
            p.difficulty_level = curr_config['diff_level']
            p.participant.vars['tol_payoff'] = 0


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Background information for each configuration
    config_num = models.IntegerField()
    start_state = models.IntegerField()
    goal_state = models.IntegerField()
    min_moves = models.IntegerField()
    difficulty_level = models.IntegerField()

    # Participant's performance information for each configuration
    moves = models.LongStringField()
    states_path = models.LongStringField()
    num_moves = models.IntegerField()
    config_solved = models.BooleanField(initial=False)
    solved_with_min_moves = models.BooleanField(initial=False)
    time_start_task = models.FloatField()
    time_first_move = models.FloatField()
    time_last_move = models.FloatField()
    timeout_happened = models.BooleanField()
    page_refreshed = models.BooleanField()

    def set_performance_info(self):
        self.num_moves = len(loads(self.moves)) if self.moves else 0
        self.solved_with_min_moves = True if self.num_moves == self.min_moves else False

    def set_payoff(self):
        if self.config_solved:
            payoff = (Constants.bonus_per_trial/100) - (Constants.loss_per_extra_move/100) * (self.num_moves - self.min_moves)
            self.payoff = 0 if payoff <= 0 else payoff
            self.participant.vars['tol_payoff'] += self.payoff
            #print(self.participant.payoff)

