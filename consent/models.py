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


author = 'Your name here'

doc = """
On Prolific Academy, add ?participant_label={{%PROLIFIC_PID%}} to session wide link
"""


class Constants(BaseConstants):
    name_in_url = 'consent'
    players_per_group = None
    num_rounds = 1

    consents = [
        'I confirm that I have read and understand the information for the above study. '
        'I have had the opportunity to consider the information, ask questions and have had these '
        'answered satisfactorily.',
        'I understand that my participation is voluntary and that I am free to withdraw at any '
        'time without giving any reason, without my rights being affected.',
        'I understand that data collected during the study, may be looked at by individuals '
        'from The University of Warwick where it is relevant to my taking part in this study. '
        'I give permission for these individuals to have access to my data.',
        'I understand that my anonymized data will be made publicly available to the scientific community and may used in future research.',
        'I agree to take part in the above study.'
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    for n, c in enumerate(Constants.consents):
        locals()[f'consent_{n+1}'] = models.BooleanField(label=c, widget=widgets.CheckboxInput)
    del n, c

    age = models.IntegerField(label='Age:', blank=True)
    age_no_say = models.BooleanField(label='', choices=[(1, 'Prefer not to say')], widget=widgets.RadioSelect, blank=True)
    gender = models.StringField(label='Gender:', choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other (Please describe if you wish):'), ('N', 'Prefer not to say')], widget=widgets.RadioSelect)
    gender_other = models.StringField(label='', blank=True)
