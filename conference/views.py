from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from conference.models import Conference
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.contrib.auth.models import Group
from account.models import CustomUser
from invitations.utils import get_invitation_model
from .forms import InvitePCMForm, AddReviewersForm
from .models import ConferencePCMInvitations, ConferenceSubmissions, ConferenceUserRoles
from django.contrib import messages

@login_required
def index(request):

    # List the conferences
    conferences_list = get_objects_for_user(request.user, 'conference.view_conference')

    # retrieve only the active invitations.
    invitations_list = ConferencePCMInvitations.objects.get_active()

    # Create context
    context= {
        'conferences_list': conferences_list,
        'invitations_list': invitations_list,
    }

    # Render the html page
    return render(request, 'index.html', context=context)

@login_required
def next_phase(request, pk):
    conference = Conference.objects.get(CID = pk)
    conference.phase = conference.phase+1
    conference.save()
    return redirect('conference-detail',pk)

# Display the details of a conference using the CID
class ConferenceDetailView(LoginRequiredMixin ,DetailView):
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

# This class represent the paper submission view
class SubmissionCreate(LoginRequiredMixin, CreateView):
    model = ConferenceSubmissions
    fields = ['authors', 'title', 'abstract', 'paper_file']

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.conference = Conference.objects.get(CID = self.kwargs['pk']) # add the conference instance to the submission
        submission.save()
        form.save_m2m()
        return super(SubmissionCreate,self).form_valid(submission)

    def get_success_url(self):
        return reverse('index') # I will change this later to redirect the user to either the submissions page or the submission detail page. I am in favor of the latter.


class SubmissionsList(LoginRequiredMixin, ListView):
    model = ConferenceSubmissions
    context_object_name = 'my_submissions_list'
    template_name = 'my_submissions_list'

    def get_queryset(self):
        queryset = ConferenceSubmissions.objects.filter(authors=self.request.user)
        return queryset

class MySubmissionDetails(LoginRequiredMixin, DetailView):
    model = ConferenceSubmissions
    template_name = 'my_submission_details.html'


class SubmissionDetails(LoginRequiredMixin, DetailView):
    model = ConferenceSubmissions
    template_name = 'conference/conference_submission_details.html'

class SubmissionUpdate(LoginRequiredMixin, UpdateView):
    model = ConferenceSubmissions
    fields = ['authors', 'title', 'abstract', 'paper_file']


class SubmissionDelete(LoginRequiredMixin, DeleteView):
    model = ConferenceSubmissions

    def get_success_url(self):
        return reverse('my-submissions')

class ViewConferenceSubmissions(LoginRequiredMixin, ListView):
    model = ConferenceSubmissions
    context_object_name = 'my_submissions_list'

    def get_queryset(self):
        queryset = ConferenceSubmissions.objects.filter(conference=self.kwargs['pk'])
        return queryset


class AddAReviewer(LoginRequiredMixin, FormView):
    model = ConferenceSubmissions
    template_name = 'conference/add_reviewer.html'
    form_class = AddReviewersForm


    def get_context_data(self, **kwargs):
        context = super(AddAReviewer, self).get_context_data(**kwargs)
        current_reviewers = ConferenceSubmissions.objects.get(pk = self.kwargs['pk'])
        context['current_reviewers'] = current_reviewers
        return context

    def get_success_url(self):
        return reverse('submission-details', kwargs={'pk':self.kwargs['pk']})

    def form_valid(self, form):
        reviewers = form.cleaned_data['reviewers']
        submission = ConferenceSubmissions.objects.get(pk = self.kwargs['pk'])
        for reviewer in reviewers:
            submission.reviewers.add(reviewer)
        print(submission.id)
        return super(AddAReviewer, self).form_valid(form)

def delete_reviewer(request, submid, reviewerid):
    submission = ConferenceSubmissions.objects.get(pk=submid)
    submission.reviewers.remove(CustomUser.objects.get(pk=reviewerid))
    return redirect('submission-details', pk=submid)
