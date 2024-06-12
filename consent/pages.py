from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class FilterMobileOut(Page):
    def is_displayed(self):
        return self.request.user_agent.is_mobile or self.request.user_agent.is_tablet

class ParticipantsFirstPage(Page):
    pass

class ParticipantsInformationSheet(Page):
    pass


class ParticipantsConsentForm(Page):
    form_model = 'player'
    form_fields = [f'consent_{n}' for n in range(1, len(Constants.consents) + 1)]


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'age_no_say', 'gender', 'gender_other']

    def error_message(self, values):
        if not values['age'] and not values['age_no_say']:
            return 'Please, indicate your age or if you prefer not to say it.'


page_sequence = [
    FilterMobileOut, ParticipantsFirstPage,
    ParticipantsInformationSheet, ParticipantsConsentForm, Demographics]
