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

from .parameters import *
from .utils import get_zurich_prosocial_game
from random import randint, Random
from math import ceil
from time import time
from copy import deepcopy
import json

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'game'
    players_per_group = None

    quiz = dict(
        q1=dict(
            label="1. Can you open the door that is blocking your character in this example "
                  "(remember, you are always the yellow character)?",
            choices=['yes', 'no'],
            correct='yes',
            feedback="Correct answer is ‘Yes’. You are the yellow character and you have "
                     "a red key left to open the door."
        ),
        q2=dict(
            label="2. Can the other player (in blue) open the door for themselves?",
            choices=['yes', 'no'],
            correct='no',
            feedback="Correct answer is ‘No’. The other player only has a red key left but no blue key."
        ),
        q3=dict(
            label="3. How many more doors will fall onto the playing field?",
            choices=['none', 'two', 'four'],
            correct='two',
            feedback="Correct answer is ‘two’. One blue door and one red door are still about "
                     "to fall onto the playing field."
        ),
        q4=dict(
            label="4. Can you still reach your treasure if you open the blue door for the other player? "
                  "(You are the yellow player and the other player is blue)",
            choices=['yes', 'no', 'maybe'],
            correct='maybe',
            feedback="Correct answer is 'Maybe'. It depends where the last blue door will fall."
        ),
    )

    instructs = [
       "Trial 1: You are Player A. In the following practice game, Player A will be short one blue key. Player B, you have the option to open the door for Player A with your last blue key",
        "Trial 2: You are Player A. In the following practice game, Player B will be short one red key. Player A, you have the option to open the door for Player B with your last red key, which may be risky since there are still more red doors left.",
        "Trial 3: You are Player A. In the following practice game, Player B will be short one red key. Player A, you have the option to open the door for Player B with your last red key, which won’t cost you anything since there aren’t any more red doors left.",
        "Trial 4: You are Player A. In the following practice game, Player A will be short one red key. Player B, you have the option to open the door for Player A, which will not cost you anything since there aren’t any more red doors left."
    ]

    rnd = Random(0)
    num_rounds = len(trials)
    num_test_trial = 6

    bonus_for_treasure = c(4)


class Subsession(BaseSubsession):
    def creating_session(self):
        const = Constants
        if self.round_number == 1:
            session = self.session
            config = session.config
            session.vars['games'] = list()

            params = game_parameters.copy()
            params.update(config)

            for r in range(Constants.num_rounds):
                self.session.vars['games'].append(
                    get_zurich_prosocial_game(params, trials, r, const.rnd)
                )

            for p in session.get_participants():
                p.vars['trial_num'] = 0

        self.set_game_status()

        for p in self.get_players():
            p.time_left = self.session.vars['games'][self.round_number - 1]['sec_per_trial']

    def set_game_status(self):
        game = self.session.vars['games'][self.round_number - 1]
        game_status = deepcopy(game_status_default)
        game_status.update(
            doors=game['doors'], keys=game['keys'], is_solo_game=game['type'] == 'instructions'
        )
        game_status_json = json.dumps([game_status])
        for p in self.get_players():
            p.game_status = game_status_json


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    for field, q in Constants.quiz.items():
        locals()[field] = models.StringField(label=q['label'], choices=q['choices'], widget=widgets.RadioSelect)
        locals()[field + '_correct'] = models.BooleanField()
    del field, q

    def set_quiz_correct_answer(self, question):
        setattr(self, f'{question}_correct', getattr(self, question) == Constants.quiz[question]['correct'])

    def get_quiz_feedback(self, question):
        return Constants.quiz[question]['feedback'] if getattr(self, question) is not None else ''

    def get_instructs(self, num):
        return Constants.instructs[num]

    trial_type = models.StringField()
    game_type = models.StringField()
    game_status = models.LongStringField(initial=[])
    ego_num_doors_opened = models.IntegerField(initial=0)
    ego_helped = models.IntegerField(initial=0)
    ego_lost = models.BooleanField(initial=False)
    time_start = models.IntegerField(initial=0)
    time_left = models.IntegerField()
    timeout = models.BooleanField()

    round_to_pay = models.IntegerField()

    def live_game(self, data):
        if data == 'start_timer':
            if self.time_start == 0:
                time_start = int(time())
                self.time_start = time_start
            time_left = ceil(self.session.vars['games'][self.round_number - 1]['sec_per_trial'] - (time() - self.time_start))
            self.time_left = time_left
            return {self.id_in_group: dict(time_left=time_left)}

        game_status = json.loads(self.game_status)
        event = game_status[-1]
        event.update(data)
        game_status.append(event)
        self.game_status = json.dumps(game_status)
        self.ego_num_doors_opened = event['ego_num_doors_open']
        if not self.ego_lost and 'ego' in event['dead_players']:
            self.ego_lost = True

    def get_round_to_pay(self, const: Constants):
        return randint(const.num_test_trial + 1, const.num_rounds)

    def set_zpg_payoff(self):
        const = Constants
        round_to_pay = self.get_round_to_pay(const)
        self.round_to_pay = round_to_pay

        self.participant.vars['zpg_payoff'] = self.in_round(round_to_pay).payoff
        self.participant.payoff = self.in_round(round_to_pay).payoff

    def set_payoff(self):
        self.payoff = Constants.bonus_for_treasure
