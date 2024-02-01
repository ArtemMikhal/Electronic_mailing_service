from django import forms

from customers.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
