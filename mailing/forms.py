from django import forms

from mailing.models import MailingSettings


class MailingSettingsForm(forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ('name', 'frequency', 'send_time', 'clients',)