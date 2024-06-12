from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as cu,
    currency_range,
)

author = 'Kathy Lau'

doc = """
On Prolific Academy, add ?participant_label={{%PROLIFIC_PID%}} to session wide link
"""

# read rounds from olddataV2.csv file and store in dictionary
# column headers: round,payoff_large,payoff_small,starting_point,number_steps_to_large,number_steps_to_small,time_large,time_small
def read_rounds(f):
    with open(f) as file:
        data = file.readlines()

    header = data[0].split(',')

    rows = data[1:]
    rounds = {}

    for row in rows:
        row = row.split(',')
        round_num = row[0]

        rounds[round_num] = {
            header[0]: row[0],
            header[1]: row[1],
            header[2]: row[2],
            header[3]: row[3],
            header[4]: row[4],
            header[5]: row[5],
            header[6]: row[6],
            header[7].strip(): row[7].strip()
        }

    return rounds

class Constants(BaseConstants):
    name_in_url = 'boat'
    players_per_group = None
    num_rounds = 13
    exchange_rate = 0.05
    rounds = read_rounds('patience_game/data.csv')
    round_order = [2,3,13,11,4,9,7,6,5,12,1,8,10]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    direction = models.BooleanField(label='Direction', initial=0, choices=[(1, 'Left'), (0, 'Right')])
    points = models.IntegerField(initial=0)
    bonus = models.CurrencyField()

    def set_direction(self, dir):
        self.direction = dir

    def set_points(self, num_points):
        self.points = num_points

    def set_payoff(self, new_points):
        self.payoff += cu(new_points/20)
