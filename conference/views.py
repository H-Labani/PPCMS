from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from conference.models import Conference
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.contrib.auth.models import Group
from account.models import CustomUser
from invitations.utils import get_invitation_model
from .forms import InvitePCMForm
from .models import ConferencePCMInvitations
from django.contrib import messages

@login_required
def index(request):

    # List the conferences and invitations
    conferences_list = get_objects_for_user(request.user, 'conference.view_conference')
    invitations_list = ConferencePCMInvitations.objects.filter(invitee = request.user.email)

    # Create context
    context= {
        'conferences_list': conferences_list,
        'invitations_list': invitations_list,
    }

    # Render the html page
    return render(request, 'index.html', context=context)


# Display the details of a conference using the CID
class ConferenceDetailView(LoginRequiredMixin ,generic.DetailView):
    model = Conference

    def get_queryset(self):
        queryset = get_objects_for_user(self.request.user, 'conference.view_conference')
        return queryset


# Create a new conference
class ConferenceCreate(LoginRequiredMixin, CreateView):
    model = Conference
    fields = ['name', 'acronym', 'web_page', 'venue', 'city', 'country', 'start_date', 'end_date' ]

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.chair = self.request.user
        candidate.save()
        group_name = 'PCM_' + str(candidate.CID)
        group = Group.objects.create(name=group_name)
        assign_perm('view_conference', group, candidate)
        self.request.user.groups.add(Group.objects.get(name=group_name))
        assign_perm('delete_conference',self.request.user, candidate)
        assign_perm('change_conference',self.request.user, candidate)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')

# Update a conference using the CID
class ConferenceUpdate(LoginRequiredMixin, UpdateView):
    model = Conference
    fields = ['name', 'acronym', 'web_page', 'venue', 'city', 'country', 'start_date', 'end_date' ]

class ConferenceDelete(LoginRequiredMixin ,DeleteView):
    model = Conference
    success_url = reverse_lazy('index')


# Invite PCM to the conference view
class InvitePCMView(LoginRequiredMixin, FormView):
    form_class = InvitePCMForm
    template_name = 'invite_pcm.html'
    success_url = 'invite_pcm_outcome.html'

    def form_valid(self, form):
        email = form.cleaned_data['invitee_email']
        role = form.cleaned_data['role']
        conference = Conference.objects.get(CID = self.kwargs['pk'])
        invitation_exist = ConferencePCMInvitations.objects.filter(invitee=email, conference=conference).count()
        if (invitation_exist > 0):
            messages.error(self.request, 'An invitation has already been sent to '+ email)
            return super(InvitePCMView, self).form_valid(form)
        messages.success(self.request, email +' has been invited.')
        try:
            user = CustomUser.objects.get(email=email)
            ConferencePCMInvitations.objects.create(inviter = self.request.user, invitee= email, conference = conference, role = role)
        except CustomUser.DoesNotExist:
            invitation = get_invitation_model()
            invite = invitation.create(email, inviter= self.request.user)
            invite.send_invitation(self.request)
            ConferencePCMInvitations.objects.create(inviter = self.request.user, invitee= email, conference = conference, role = role)
            return super().form_valid(form)
        return super(InvitePCMView, self).form_valid(form)

    def get_success_url(self):
        return reverse('invite-pcm', kwargs={'pk':self.kwargs['pk']})
