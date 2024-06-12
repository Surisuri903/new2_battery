from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from time import time

class FirstRoundPage(Page):
    def is_displayed(self):
        return self.round_number == 1


class Welcome1(FirstRoundPage):
    pass


class Welcome2(FirstRoundPage):
    pass


class Instructions1(FirstRoundPage):
    def vars_for_template(self):
        return dict(bonus_with_one_extra_move=Constants.bonus_per_trial-Constants.loss_per_extra_move,
                    bonus_with_two_extra_moves=Constants.bonus_per_trial - (Constants.loss_per_extra_move * 2),
                    max_payment=Constants.participation_fee + (Constants.bonus_per_trial * Constants.num_rounds)/100,
                    max_bonus=c(4.8),
                    min_bonus=c(0))


class Instructions2(FirstRoundPage):
    def vars_for_template(self):
        config = Constants.configurations[self.round_number-1]
        start = {n+1: [i for i in l] for n, l in
                 enumerate(config['start'][self.player.start_state])}  # Transform to dict to better handle it in JS
        goal = {n + 1: [i for i in l] for n, l in
                 enumerate(config['goal'][self.player.goal_state])}  # Transform to dict to better handle it in JS
        min_moves = config['min_moves']
        return dict(start=start, goal=goal, min_moves=min_moves)


class Instructions3(FirstRoundPage):
    pass


class Instructions4(FirstRoundPage):
    pass


class Trial1(FirstRoundPage):
    def vars_for_template(self):
        config = Constants.practice_configurations[0]
        start = {n+1: [i for i in l] for n, l in
                 enumerate(config['start'][51])}   # Transform to dict to better handle it in JS
        goal = {n + 1: [i for i in l] for n, l in
                 enumerate(config['goal'][63])}     # Transform to dict to better handle it in JS
        min_moves = config['min_moves']
        return dict(start=start, goal=goal, min_moves=min_moves)


class Trial2(FirstRoundPage):
    def vars_for_template(self):
        config = Constants.practice_configurations[1]
        start = {n+1: [i for i in l] for n, l in
                 enumerate(config['start'][23])}   # Transform to dict to better handle it in JS
        goal = {n + 1: [i for i in l] for n, l in
                 enumerate(config['goal'][35])}     # Transform to dict to better handle it in JS
        min_moves = config['min_moves']
        return dict(start=start, goal=goal, min_moves=min_moves)


class Task(Page):

    timeout_seconds = 60 * Constants.time_limit
    timer_text = 'To complete the task you have:'

    form_model = 'player'
    form_fields = ['moves', 'states_path', 'config_solved', 'time_start_task', 'time_first_move', 'time_last_move']

    # TODO: add summary metrics (not average)

    def vars_for_template(self):

        if self.participant.vars.get(f'page_{self.round_number}_visited'):
            if "last_refreshed_time" in self.participant.vars:
                last_refreshed_time = self.participant.vars.get('last_refreshed_time')
                if time() - last_refreshed_time > 5:
                    self.player.page_refreshed = True
        self.participant.vars[f'page_{self.round_number}_visited'] = True
        self.participant.vars["last_refreshed_time"] = time()

        config = Constants.configurations[self.round_number-1]
        start = {n+1: [i for i in l] for n, l in
                 enumerate(config['start'][self.player.start_state])}  # Transform to dict to better handle it in JS
        goal = {n + 1: [i for i in l] for n, l in
                 enumerate(config['goal'][self.player.goal_state])}  # Transform to dict to better handle it in JS
        min_moves = config['min_moves']
        # if not self.player.time_start_task:
        #     t = time()
        #     self.player.time_start_task = t * 1000  # store time in millisecond to conform to JS
        return dict(start=start, goal=goal, min_moves=min_moves, page_refreshed=self.player.page_refreshed)

    def before_next_page(self):
        self.player.timeout_happened = self.timeout_happened
        self.player.set_performance_info()
        self.player.set_payoff()


class Feedback(Page):

    def before_next_page(self):
        if self.round_number == Constants.num_rounds:
            num_solved_config_per_diff_level = {
                0: sum(p.config_solved for p in self.player.in_all_rounds() if p.difficulty_level == 0),
                1: sum(p.config_solved for p in self.player.in_all_rounds() if p.difficulty_level == 1),
                2: sum(p.config_solved for p in self.player.in_all_rounds() if p.difficulty_level == 2),
                3: sum(p.config_solved for p in self.player.in_all_rounds() if p.difficulty_level == 3)
            }
            self.participant.vars["num_solved_config_per_diff_level"] = num_solved_config_per_diff_level
            self.participant.vars["num_solved_config"] = sum(num_solved_config_per_diff_level.values())
            num_solved_config_with_min_moves_per_diff_level = {
                0: sum(p.solved_with_min_moves for p in self.player.in_all_rounds() if p.difficulty_level == 0),
                1: sum(p.solved_with_min_moves for p in self.player.in_all_rounds() if p.difficulty_level == 1),
                2: sum(p.solved_with_min_moves for p in self.player.in_all_rounds() if p.difficulty_level == 2),
                3: sum(p.solved_with_min_moves for p in self.player.in_all_rounds() if p.difficulty_level == 3)
            }
            self.participant.vars["num_solved_config_with_min_moves_per_diff_level"] = num_solved_config_with_min_moves_per_diff_level
            self.participant.vars["num_solved_config_with_min_moves"] = sum(num_solved_config_with_min_moves_per_diff_level.values())


class EndofTask(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class Bonus(Page):
    form_model = 'player'

    def vars_for_template(self):
        return dict(bonus=self.participant.vars['tol_payoff'])

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class EndSession1(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Welcome1,
    Welcome2,
    Instructions1,
    Instructions2,
    Instructions3,
    Instructions4,
    Trial1,
    Trial2,
    Task,
    Feedback,
    EndofTask,
    Bonus,
    EndSession1
]
