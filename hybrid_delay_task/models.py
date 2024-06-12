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

from random import randint

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'hybrid_delay_task'
    players_per_group = None
    num_rounds = 2
    coins_rows = [list(range(n))for n in [6, 5, 4, 1]]
    total_coins = sum([len(r) for r in coins_rows])
    seconds_per_coin_transfer = 15
    rects_per_minute = 3
    seconds_for_timeout = 10
    exchange_rate = 0.1
    small_payoff = 1

    session_vars = [
        'total_coins', 'small_payoff', 'seconds_per_coin_transfer', 'rects_per_minute', 'seconds_for_timeout'
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        ps = self.get_players()
        svars = self.session.vars
        round_number = self.round_number

        if round_number == 1:
            const = Constants
            session = self.session
            config = session.config
            for v in const.session_vars:
                svars[v] = config.get(v, getattr(const, v))
            svars['max_seconds_on_coins_transfer_page'] = svars['total_coins'] * svars['seconds_per_coin_transfer']
            svars['rects_start_timers'] = dict()

            for p in ps:
                participant = p.participant
                participant.vars['transfer_start_timestamp'] = 0
                participant.vars['hybrid_delay_payoff'] = 0

        svars['rects_start_timers'][round_number] = self.get_rects_start_timers(svars)

    def get_rects_start_timers(self, svars):
        rects_per_minute = svars['rects_per_minute']
        seconds_for_timeout = svars['seconds_for_timeout']
        rects_start_timers = []
        e, p = 3, 60
        for m in range(int(svars['max_seconds_on_coins_transfer_page'] // p)):
            for n in range(rects_per_minute):
                lower = e
                if rects_start_timers:
                    lower = max(p * m, rects_start_timers[-1] + seconds_for_timeout + e)
                upper = p * m + p - (rects_per_minute - n) * (seconds_for_timeout + e)
                rects_start_timers.append(randint(lower, upper))
        return rects_start_timers


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice = models.BooleanField()
    choice_latency = models.FloatField()
    num_coins = models.IntegerField(initial=0)
    is_stopped = models.BooleanField(initial=False)
    num_rect = models.IntegerField(initial=0)
    rect_displayed = models.BooleanField(initial=False)
    coin_in_transfer = models.BooleanField(initial=False)
    is_timeout = models.BooleanField(initial=False)

    def live_coins_transfer(self, data):
        participant = self.participant
        self.num_coins = data['num_coins']
        self.num_rect = data['num_rect']
        self.rect_displayed = data['rect_displayed']
        self.coin_in_transfer = data['coin_in_transfer']
        participant.vars.update(transfer_start_timestamp=data['transfer_start_timestamp'])

    def set_coins_in_pig_pos(self, num_coins):
        return [(50 + randint(-10, 14), 40 + randint(-6, 14)) for _ in range(num_coins)]

    def set_payoff(self):
        const = Constants
        if self.choice == 0:
            self.num_coins = self.session.vars['small_payoff']
        self.payoff = round(self.num_coins * const.exchange_rate, 2)
        self.participant.vars['hybrid_delay_payoff'] += self.payoff
        if self.round_number == const.num_rounds:
            self.participant.payoff += self.participant.vars['hybrid_delay_payoff']
