from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from time import time


class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1


class Instr1(Page):
    def vars_for_template(self):
        return dict(pences_per_coin=int(Constants.exchange_rate * 100))

    def is_displayed(self):
        return self.round_number == 1


class Instr2(Page):
    def vars_for_template(self):
        return dict(seconds_for_timeout=self.session.vars['seconds_for_timeout'])

    def is_displayed(self):
        return self.round_number == 1


class Instr3(Page):
    def is_displayed(self):
        return self.round_number == 1


class Choice(Page):
    form_model = 'player'
    form_fields = ['choice', 'choice_latency']

    def vars_for_template(self):
        return dict(
            small_payoff=[list(range(self.session.vars['small_payoff']))]
        )

    def before_next_page(self):
        if self.player.choice == 0:
            self.player.set_payoff()


class LargeOptionTransfer(Page):
    form_model = 'player'
    form_fields = ['num_coins', 'is_stopped', 'num_rect', 'is_timeout']

    live_method = 'live_coins_transfer'

    def vars_for_template(self):
        player = self.player
        return dict(
            coins_in_pig_pos=player.set_coins_in_pig_pos(Constants.total_coins),
            coin_in_transfer=player.coin_in_transfer
        )

    def js_vars(self):
        player = self.player
        participant = player.participant
        svars = player.session.vars
        start_timer = participant.vars.get('start_timer')
        if not start_timer:
            start_timer = participant.vars.setdefault('start_timer', time())
        return dict(
            total_coins=Constants.total_coins,
            transfer_duration=svars['seconds_per_coin_transfer'],
            coin_in_transfer=player.coin_in_transfer,
            seconds_for_timeout=svars['seconds_for_timeout'],
            start_timer=start_timer,
            max_seconds_on_page=svars['max_seconds_on_coins_transfer_page'] + 20,
            rect_displayed=player.rect_displayed,
            rects_start_timers=svars['rects_start_timers'][player.round_number],
            transfer_start_timestamp=participant.vars['transfer_start_timestamp']
        )

    def is_displayed(self):
        return self.player.choice == 1

    def before_next_page(self):
        participant = self.participant
        participant.vars['transfer_start_timestamp'] = 0
        del participant.vars['start_timer']
        self.player.set_payoff()


class RoundPayoff(Page):
    def vars_for_template(self):
        return dict(
            earnings=self.player.payoff,
            coins_in_pig_pos=self.player.set_coins_in_pig_pos(self.player.num_coins))


class Results(Page):

    def vars_for_template(self):
        tot_coins = sum([p.num_coins for p in self.player.in_all_rounds()])

        return dict(tot_coins=tot_coins, 
            hybrid_delay_payoff=self.participant.vars['hybrid_delay_payoff'].to_real_world_currency(self.session), 
            coins_in_pig_pos=self.player.set_coins_in_pig_pos(tot_coins))

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class EndSession2(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Welcome,
    Instr1, Instr2, Instr3,
    Choice, LargeOptionTransfer, RoundPayoff, Results, EndSession2]
