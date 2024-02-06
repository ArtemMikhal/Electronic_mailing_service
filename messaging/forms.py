from django import forms

from mailing.models import MailingSettings
from messaging.models import MailingMessage

class MailingMessageForm(forms.ModelForm):

    class Meta:
        model = MailingMessage
        fields = '__all__'
        widgets = {
            'mailing': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Получите все созданные рассылки
        self.fields['mailing'].queryset = MailingSettings.objects.all()


class MailingActivateForm(forms.ModelForm):
    is_active = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = MailingSettings
        fields = ['is_active']