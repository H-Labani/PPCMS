from django import forms
from account.models import CustomUser


class InvitePCMForm(forms.Form):
    invitee_email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.', required=True)
    roles = (
        (1,'chair'),
        (2,'member'),
    )
    role = forms.ChoiceField(choices= roles)