from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# page to display rounds from models page (which stores from data.csv)
class Round(Page):
    form_model = 'player'
    form_fields = ['direction']
    # store direction user picked (1 for left, 0 for right)

    def get_round_vars(self):
        curr_round = Constants.round_order[self.player.round_number-1]  # subtract one practice round
        round = Constants.rounds[str(curr_round)]

        # convert starting position to pos on background image
        starting_point = float(round['starting_point'])
        pos = str(starting_point * 840) + "px"

        # convert time to seconds
        large_duration = int(round['time_large'])*1000
        small_duration = int(round['time_small'])*1000

        large_payoff = int(round['payoff_large'])
        small_payoff = int(round['payoff_small'])

        return [starting_point, pos, large_duration, small_duration, large_payoff, small_payoff, curr_round]

    # pass round variables to template page
    def vars_for_template(self):
        round_vars = self.get_round_vars()

        return dict(
            starting_point=round_vars[0],
            pos=round_vars[1],
            large_duration=round_vars[2],
            small_duration=round_vars[3],
            large_payoff=round_vars[4],
            small_payoff=round_vars[5],
            curr_round=self.player.round_number
        )

    # set and store points earned by participant before moving to new round
    def before_next_page(self):
        round_vars = self.get_round_vars()
        starting_point = round_vars[0]

        # special rules for catch round
        if self.player.round_number == 3:
            if self.player.direction == 1:
                self.player.set_points(round_vars[4])
                self.player.set_payoff(round_vars[4])
            else:
                self.player.set_points(round_vars[5])
                self.player.set_payoff(round_vars[5])

        # add small payoff
        elif starting_point < 0.5 and self.player.direction == 1:
            self.player.set_points(round_vars[5])
            self.player.set_payoff(round_vars[5])
        # add small payoff
        elif starting_point > 0.5 and self.player.direction == 0:
            self.player.set_points(round_vars[5])
            self.player.set_payoff(round_vars[5])
        # add large payoff
        else:
            self.player.set_points(round_vars[4])
            self.player.set_payoff(round_vars[4])

    def is_displayed(self):
        return self.player.round_number <= Constants.num_rounds


# page to display points earned by participant before next round
class RoundPayoff(Page):

    def vars_for_template(self):
        total_points = sum([p.points for p in self.player.in_all_rounds()])
        earnings = total_points * 0.05
        return dict(
            total_points = total_points,
            earnings = earnings,
            curr_round=self.player.round_number
            )


    def is_displayed(self):
        return self.player.round_number <= Constants.num_rounds


page_sequence = [Round, RoundPayoff]
