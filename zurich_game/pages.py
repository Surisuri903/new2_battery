from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import randint
import json


class QuizPage(Page):
    template_name = 'zurich_game/QuizPage.html'

    def vars_for_template(self):
        q = self.form_fields[0]
        return dict(
            img=f'game/imgs/quiz/zpg_{q}.png',
            feedback=self.player.get_quiz_feedback(q)
        )

    def is_displayed(self):
        return self.round_number == 7

class InstructionsPage(Page):

    def vars_for_template(self):
        return dict(
            instructions = self.player.get_instructs(self.round_number-3)
        )

    def is_displayed(self):
        return self.round_number > 2 and self.round_number < 7


class Session3(Page):
    def is_displayed(self):
        return self.round_number == 1

class P1(Page):
    def is_displayed(self):
        return self.round_number == 1


class P2(Page):
    def is_displayed(self):
        return self.round_number == 3


class P3(Page):
    def is_displayed(self):
        return self.round_number == 7


class Q1(QuizPage):
    form_model = 'player'
    form_fields = ['q1']

    def before_next_page(self):
        self.player.set_quiz_correct_answer('q1')


class Q1Feedback(QuizPage):
    form_model = 'player'
    form_fields = ['q1']


class Q2(QuizPage):
    form_model = 'player'
    form_fields = ['q2']

    def before_next_page(self):
        self.player.set_quiz_correct_answer('q2')


class Q2Feedback(QuizPage):
    form_model = 'player'
    form_fields = ['q2']


class Q3(QuizPage):
    form_model = 'player'
    form_fields = ['q3']

    def before_next_page(self):
        self.player.set_quiz_correct_answer('q3')


class Q3Feedback(QuizPage):
    form_model = 'player'
    form_fields = ['q3']


class Q4(QuizPage):
    form_model = 'player'
    form_fields = ['q4']

    def before_next_page(self):
        self.player.set_quiz_correct_answer('q4')


class Q4Feedback(QuizPage):
    form_model = 'player'
    form_fields = ['q4']


class P8(Page):
    def is_displayed(self):
        return self.round_number == 7


class WaitingPartner(Page):
    def vars_for_template(self):
        player = self.player
        round_number = player.round_number

        return dict(
            curr_round=round_number
        )

    def get_timeout_seconds(self):
        return randint(5, 10)

    def is_displayed(self):
        return (self.round_number > 2 and self.round_number < 7) or (self.round_number > 7 and self.round_number < 17)


class Game(Page):
    live_method = 'live_game'

    def vars_for_template(self):
        const = Constants
        player = self.player
        participant = player.participant
        round_number = player.round_number
        game = self.session.vars['games'][participant.vars['trial_num']]
        player.trial_type, player.game_type = game['type'], game['help_other']
        game_status = json.loads(player.game_status)[-1]
        game.update(doors=game_status['doors'])
        game.update(is_solo_game=player.trial_type == 'instructions')
        doors = game['doors']
        doors_rows = [
            doors[n:n + game['n_doors_per_row']] for n in range(0, len(doors), game['n_doors_per_row'])
        ]

        return dict(
            game=game,
            game_status=game_status,
            doors_rows=doors_rows,
            curr_round=round_number if game['is_solo_game'] else round_number - 2 if game['type'] == 'practice' else round_number - 6,
            num_rounds=2 if game['type'] == 'instructions' else 4 if game['type'] == 'practice' else const.num_rounds - 6
        )

    def js_vars(self):
        player = self.player
        participant = player.participant
        game = self.session.vars['games'][participant.vars['trial_num']]
        game_status = json.loads(player.game_status)[-1]
        game.update(doors=game_status['doors'])
        game.update(is_solo_game=game['type'] == 'instructions')

        return dict(
            game=game,
            game_status=game_status,
            time_start=player.time_start
        )

    def before_next_page(self):
        player = self.player
        game_status = json.loads(player.game_status)[-1]

        for field in ['ego_helped', 'ego_lost', 'timeout']:
            setattr(player, field, game_status[field])
        player.participant.vars['trial_num'] += 1

        if game_status['timeout'] == False and game_status['ego_lost'] == False:
            player.set_payoff()


class P9(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.set_zpg_payoff()


class P10(Page):
    def vars_for_template(self):
        return dict(
            game_to_pay = self.player.round_to_pay - Constants.num_test_trial
            #game_to_pay=self.player.round_number - Constants.num_test_trial
        )

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

page_sequence = [
    Session3,
    P1, P2, P3,
    WaitingPartner,
    InstructionsPage,
    Q1, Q1Feedback,
    Q2, Q2Feedback,
    Q3, Q3Feedback,
    Q4, Q4Feedback,
    P8,
    Game, P9, P10
]
