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


doc = """
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = None
    num_rounds = 1

    endowment = c(5)
    multiplier = 3
    return_factor = 0.5

    waiting_page_seconds_range = [8, 18]

    q1_correct = 2
    q2_correct = 2
    q3_correct = 1
    q1_wrong = 'Incorrect. The correct answer is £0 - £9. The other can send back any amount ' \
                'between £0 and £9.00 because the amount you sent to them gets tripled.'
    q2_wrong = 'Incorrect. The correct answer is £5. You have £5 at the end because you kept £2 of ' \
                'your initial £5 and get added the £3 that the other player sent back to you.'
    q3_wrong = 'Incorrect. The correct answer is £0 - £0, because you only sent £0 to them.'

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.IntegerField(
        label='(1) Imagine you send £3.00 to the other player. '
              'What is the range of possible values that the other can send back to you?',
        choices=[(1, '£0 - £3'), (2, '£0 - £9'), (3, '£3 - £9'), (4, '£3 - £12')],
        widget=widgets.RadioSelect()
    )
    q2 = models.IntegerField(
        label='(2) Imagine you send £3.00 to the other player and the other player sends back £3.00 to you. '
              'How much do you have at the end?',
        choices=[(1, '£2'), (2, '£5'), (3, '£6'), (4, '£12')],
        widget=widgets.RadioSelect()
    )
    q3 = models.IntegerField(
        label='(3) Imagine you send £0.00 to the other player. What is the range of possible values that the other can send back to you?',
        choices=[(1, '£0 - £0'), (2, '£0 - £5'), (3, '£5 - £10'), (4, '£5 - £15')],
        widget=widgets.RadioSelect()
    )
    sent = models.CurrencyField(label='Please enter an amount from 0 to 5:', min=0, max=Constants.endowment)
    returned = models.CurrencyField()

    def set_payoff(self):
        const = Constants
        self.returned = self.sent * const.multiplier * const.return_factor
        self.payoff = const.endowment - self.sent + self.returned
