from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1


class Intro1(Page):
    def is_displayed(self):
        return self.round_number == 1


class Intro2(Page):
    def is_displayed(self):
        return self.round_number == 1


class Task(Page):
    form_model = 'player'
    form_fields = ['is_exploded', 'points']

    def vars_for_template(self):
        round_number = self.round_number
        points_last_balloon = 0
        total_points = 0
        if round_number > 1:
            points_last_balloon = self.player.in_round(self.round_number-1).points
            total_points += sum(p.points for p in self.player.in_previous_rounds())
        return dict(
            points_last_balloon=points_last_balloon/100,
            total_points=total_points/100,
            round_number=round_number
        )

    def js_vars(self):
        const = Constants
        return dict(
            points_per_pump=const.points_per_pump,
            max_num_pumps=const.max_num_pumps,
            breaking_point=self.session.vars['breakpoints'][self.round_number-1],
            sec_delay_submit=const.sec_delay_submit
        )

    def before_next_page(self):
        self.player.set_payoff()


class Results(Page):
    def vars_for_template(self):
        return dict(bart_payoff=self.participant.vars['bart_payoff'].to_real_world_currency(self.session))

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Welcome, Intro1, Intro2, Task, Results]
