from django import forms
from account.models import CustomUser
from .models import ConferenceSubmission


class InvitePCMForm(forms.Form):
    invitee_email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.', required=True)
    roles = (
        (1,'chair'),
        (2,'member'),
    )
    role = forms.ChoiceField(choices= roles)


class AddReviewersForm(forms.Form):

    class Meta:
        model = ConferenceSubmission
        fields = ['reviewers']

    reviewers = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), label= 'Reviewers')

    # def __init__(self, *args, **kwargs):
    #     super(AddReviewersForm, self).__init__(*args, **kwargs)
    #     group_name = kwargs.pop('group')
    #     self.fields['reviewers'].queryset= CustomUser.objects.filter(groups__name=group_name)