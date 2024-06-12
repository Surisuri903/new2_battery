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

import random as rnd
import json

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'task'
    players_per_group = None
    num_pairs = 3  # 8
    num_rep_per_pair = 50
    num_rounds = num_pairs

    seconds_selected_door_displayed = 0.1
    seconds_before_display_values_after_selection = 0.05
    seconds_values_displayed = 1
    seconds_inter_trial_interval = 0.1

    choice_set_file_path = ''
    imgs_base_url = 'risk_from_experience_task/imgs/doors/'

    doors_order = [['A', 'B'] for _ in range(int(num_rep_per_pair/2))] + \
                  [['B', 'A'] for _ in range(int(num_rep_per_pair / 2))]

    # values_uncertain = [(i, j, z) for i, j, z in zip(
    #     [10, 7, 2, -10, 2, 6, 2, -7], [0, 1, 8, 0, 4, 0, 8, -1], [0.1, 0.5, 0.3, 0.1, 0.5, 0.5, 0.7, 0.5])]
    # values_certain = [1, 4, 4, -1, 0, 3, 5, -4]

    values_uncertain = [(i, j, z) for i, j, z in zip(
        [6, 2, 7], [0, 4, 1], [0.5, 0.5, 0.5])]
    values_certain = [3, 0, 4]
    pairs_values_and_probs = [{'A': i, 'B': j} for i, j in zip(values_uncertain, values_certain)]


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            pairs_values_and_probs = Constants.pairs_values_and_probs
            doors_order = Constants.doors_order.copy()
            doors_order_per_pair = []
            for n in range(Constants.num_pairs):
                rnd.seed(n)
                rnd.shuffle(doors_order)
                doors_order_per_pair.append(doors_order)

            all_doors = []
            for d in range(Constants.num_pairs):
                rep_for_pair = []
                for o in doors_order_per_pair[d]:
                    print(d)
                    print(pairs_values_and_probs[d])
                    rep_for_pair.append(
                        {'pair': d + 1,
                         'values': {
                             'A': rnd.choices(
                                 list(pairs_values_and_probs[d]['A'][:2]),
                                 weights=[pairs_values_and_probs[d]['A'][2], 1 - pairs_values_and_probs[d]['A'][2]])[0],
                             'B': pairs_values_and_probs[d]['B']
                         },
                         'order': o}
                    )
                all_doors.append(rep_for_pair)
            self.session.vars['all_doors'] = all_doors

            for p in self.get_players():
                p.participant.vars.update(door_left=[], door_right=[], choice=[], pair_payoffs=[], latency=[])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pair = models.IntegerField()
    num_rep = models.IntegerField(initial=0)
    door_left = models.LongStringField()
    door_right = models.LongStringField()
    choice = models.LongStringField()
    pair_payoffs = models.LongStringField()
    latency = models.LongStringField()
    payment = models.CurrencyField()

    def live_task(self, data):
        id = self.id_in_group
        pvars = self.participant.vars
        for k in ['door_left', 'door_right', 'choice', 'pair_payoffs', 'latency']:
            pvars[k].append(data[k])

        if self.num_rep >= Constants.num_rep_per_pair - 1:
            for k in ['choice', 'door_left', 'door_right', 'pair_payoffs', 'latency']:
                setattr(self, k, json.dumps(pvars[k]))
            return {self.id_in_group: dict(type='submit')}

        self.num_rep += 1
        doors_params = self.session.vars['all_doors'][self.round_number - 1][self.num_rep]
        pair_number, values, order = doors_params['pair'], doors_params['values'], doors_params['order']
        doors = [{'type': o, 'value': values[o], 'url': f'/static/{Constants.imgs_base_url}{pair_number}_{o}.jpg'} for o in
                 order]
        return {id: dict(type='task', task=doors)}

    def set_payoff(self):
        self.payoff = sum(self.participant.vars['pair_payoffs']) * 0.01*1.94

    def reset_pvars(self):
        self.participant.vars.update(door_left=[], door_right=[], choice=[], pair_payoffs=[], latency=[])

    comments = models.LongStringField(
        label="This is a pilot run of the task. We would appreciate any feedback you have for us "
              "(did everything work alright, were instructions clear, … anything you think could be improved):",
        blank=True
    )
