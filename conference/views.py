from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from conference.models import Conference
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.contrib.auth.models import Group
from account.models import CustomUser
from invitations.utils import get_invitation_model
from .forms import InvitePCMForm, AddReviewersForm
from .models import ConferencePCMInvitation, ConferenceSubmission, ConferenceUserRole, ConferenceSubmissionReview, ConferenceSubmissionDiscussion
from django.contrib import messages


class ConferenceHomePage(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        pass


@login_required
def index(request):

    # List the conferences
    conferences_list = Conference.objects.exclude(role_conference__role_user=request.user)

    # fetch my conferences
    my_conferences = Conference.objects.filter(role_conference__role_user=request.user)

    # fetch all the roles for the user
    user_roles = ConferenceUserRole.objects.filter(role_user=request.user)
    # retrieve only the active invitations.
    invitations_list = ConferencePCMInvitation.objects.get_active().filter(invitee=request.user)


    # Create context
    context= {
        'my_conferences': my_conferences,
        'conferences_list': conferences_list,
        'invitations_list': invitations_list,
        'user_roles': user_roles,
    }

    # Render the html page
    return render(request, 'index.html', context=context)

@login_required
def next_phase(request, pk):
    conference = Conference.objects.get(CID = pk)
    conference.phase = conference.phase+1
    conference.save()
    return redirect('conference-manage',pk)


# Create a new conference
class ConferenceCreate(LoginRequiredMixin, CreateView):
    model = Conference
    template_name = 'conference/chair/chair_conference_create_form.html'
    fields = ['name', 'acronym', 'web_page', 'venue', 'city', 'country', 'start_date', 'end_date' ]

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.chair = self.request.user
        candidate.save()

        conference = Conference.objects.get(pk=candidate.pk)
        user = self.request.user
        temp_role = ConferenceUserRole(role_conference=conference, role_user= user, role=1)
        temp_role.save()

        group_name = 'PCM_' + candidate.name +'_' + str(candidate.CID)
        group = Group.objects.create(name=group_name)
        assign_perm('reviewer', group, candidate)
        self.request.user.groups.add(Group.objects.get(name=group_name))
        assign_perm('chair',self.request.user, candidate)
        assign_perm('view_conference',self.request.user, candidate)
        assign_perm('delete_conference',self.request.user, candidate)
        assign_perm('change_conference',self.request.user, candidate)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


# Chair's conference details view
class ChairConferenceManageView(LoginRequiredMixin ,DetailView):
    model = Conference
    template_name = 'conference/chair/chair_conference_details.html'

    def get_queryset(self):
        queryset = Conference.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        # Display the current PC members in the view
        context = super(ChairConferenceManageView, self).get_context_data(**kwargs)
        conference = Conference.objects.get(pk=self.kwargs['pk'])
        group_name = 'PCM_' + conference.name + '_' + str(conference.CID)
        context['PCM'] = CustomUser.objects.filter(groups__name=group_name)
        return context


# The public main page of the conference
class PublicConferenceDetailView(LoginRequiredMixin ,DetailView):
    model = Conference
    template_name = 'conference/conference_details.html'

    def get_queryset(self):
        queryset = Conference.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        # Display the current PC members in the view
        context = super(PublicConferenceDetailView, self).get_context_data(**kwargs)
        conference = Conference.objects.get(pk=self.kwargs['pk'])
        group_name = 'PCM_' + conference.name + '_' + str(conference.CID)
        context['PCM'] = CustomUser.objects.filter(groups__name=group_name)
        return context


# Update a conference using the CID
class ConferenceUpdate(LoginRequiredMixin, UpdateView):
    model = Conference
    fields = ['name', 'acronym', 'web_page', 'venue', 'city', 'country', 'start_date', 'end_date' ]
    template_name = 'conference/chair/chair_conference_create_form.html'


class ConferenceDelete(LoginRequiredMixin ,DeleteView):
    model = Conference
    success_url = reverse_lazy('index')
    template_name = 'conference/chair/chair_conference_confirm_delete.html'


# Invite PCM to the conference view
class InvitePCMView(LoginRequiredMixin, CreateView):
    #form_class = InvitePCMForm
    model = ConferencePCMInvitation
    fields = ['invitee', 'role']
    template_name = 'invite_pcm.html'

    def form_valid(self, form):
        invitation = form.save(commit=False)
        if ConferencePCMInvitation.objects.filter(inviter=self.request.user, invitee=invitation.invitee, role=invitation.role).count() == 0:
            # add the conference instance to the invitation
            invitation.conference = Conference.objects.get(pk=self.kwargs['pk'])
            invitation.inviter = self.request.user # add the conference instance to the invitation
            invitation.save()
            form.save_m2m()
            messages.success(self.request, invitation.invitee.first_name +' has been invited.')
        else:
            messages.error(self.request, 'An invitation has already been sent to '+ invitation.invitee.last_name  +
                           ', ' + invitation.invitee.first_name + ' for the role ' + invitation.get_role_display())
            return HttpResponseRedirect(self.get_success_url())
        # email = form.cleaned_data['invitee_email']
        # role = form.cleaned_data['role']
        # conference = Conference.objects.get(CID = self.kwargs['pk'])
        # # invitation_exist = ConferencePCMInvitation.objects.filter(invitee=email, conference=conference).count()
        # if (invitation_exist > 0):
        #     messages.error(self.request, 'An invitation has already been sent to '+ email)
        #     return super(InvitePCMView, self).form_valid(form)
        # messages.success(self.request, email +' has been invited.')
        # try:
        #     user = CustomUser.objects.get(email=email)
        #     ConferencePCMInvitation.objects.create(inviter = self.request.user, invitee= email, conference = conference, role = role)
        # except CustomUser.DoesNotExist:
        #     invitation = get_invitation_model()
        #     invite = invitation.create(email, inviter= self.request.user)
        #     invite.send_invitation(self.request)
        #     ConferencePCMInvitation.objects.create(inviter = self.request.user, invitee= email, conference = conference, role = role)
        #     return super().form_valid(form)
        return super(InvitePCMView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Display the current PC members in the view
        context = super(InvitePCMView, self).get_context_data(**kwargs)
        conference = Conference.objects.get(pk=self.kwargs['pk'])
        group_name = 'PCM_' + conference.name + '_' + str(conference.CID)
        context['PCM'] = CustomUser.objects.filter(groups__name=group_name)
        context['conference'] = conference
        return context

    def get_success_url(self):
        return reverse('invite-pcm', kwargs={'pk':self.kwargs['pk']})


def accept_invite(request, inviteid):
    invite = ConferencePCMInvitation.objects.get(pk=inviteid)

    # Add the role to the database
    conference = invite.conference
    user = request.user
    temp_role = ConferenceUserRole(role_conference=conference, role_user=user, role=2)
    temp_role.save()

    # Add the user to the PCM group
    group_name = 'PCM_' + invite.conference.name + '_' + str(invite.conference.CID)
    group = Group.objects.get(name=group_name)
    group.user_set.add(user)

    # Update the invitation accepted field
    invite.accepted = True
    invite.save()
    return redirect('index')


def reject_invite(request, inviteid):
    invite = ConferencePCMInvitation.objects.get(pk=inviteid)
    invite.delete()
    return redirect('index')


# This class represent the paper submission view
class SubmissionCreate(LoginRequiredMixin, CreateView):
    model = ConferenceSubmission
    fields = ['authors', 'title', 'abstract', 'paper_file']
    template_name = 'conference/author/author_conference_submission_form.html'

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.conference = Conference.objects.get(CID = self.kwargs['pk']) # add the conference instance to the submission
        submission.save()
        form.save_m2m()
        return super(SubmissionCreate,self).form_valid(submission)

    def get_success_url(self):
        return reverse('index') # I will change this later to redirect the user to either the submissions page or the submission detail page. I am in favor of the latter.


class MySubmissionsList(LoginRequiredMixin, ListView):
    model = ConferenceSubmission
    context_object_name = 'my_submissions_list'
    template_name = 'conference/author/author_my_submissions_list.html'

    def get_queryset(self):
        queryset = ConferenceSubmission.objects.filter(authors=self.request.user)
        return queryset


class MySubmissionDetails(LoginRequiredMixin, DetailView):
    model = ConferenceSubmission
    template_name = 'conference/author/author_my_submission_details.html'


class SubmissionUpdate(LoginRequiredMixin, UpdateView):
    model = ConferenceSubmission
    fields = ['authors', 'title', 'abstract', 'paper_file']
    template_name = 'conference/author/author_conference_submission_form.html'


class SubmissionDelete(LoginRequiredMixin, DeleteView):
    model = ConferenceSubmission
    template_name = 'conference/author/author_conference_submission_confirm_delete.html'

    def get_success_url(self):
        return reverse('my-submissions')


class ViewConferenceSubmissions(LoginRequiredMixin, ListView):
    model = ConferenceSubmission
    context_object_name = 'submissions_list'
    template_name = 'conference/chair/chair_submissions_list.html'

    def get_queryset(self):
        queryset = ConferenceSubmission.objects.filter(conference=self.kwargs['pk'])
        return queryset


class ChairSubmissionDetails(LoginRequiredMixin, UpdateView):
    model = ConferenceSubmission
    template_name = 'conference/chair/chair_submission_details.html'
    context_object_name = 'submission_details'
    fields = ['decision']

    def get_success_url(self):
        return reverse('chair-submission-details', kwargs={'pk':self.kwargs['pk']})


class AddAReviewer(LoginRequiredMixin, FormView):
    model = ConferenceSubmission
    template_name = 'conference/chair/chair_add_reviewer_to_submission.html'
    form_class = AddReviewersForm

    # def get_form_kwargs(self):
    #     kwargs = super(AddAReviewer, self).get_form_kwargs()
    #     submission = ConferenceSubmission.objects.get(pk=self.kwargs['pk'])
    #     group_name = 'PCM_' + submission.conference.name + '_' + str(submission.conference.CID)
    #     kwargs['group'] = group_name
    #     print(group_name)
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super(AddAReviewer, self).get_context_data(**kwargs)
        current_reviewers = ConferenceSubmission.objects.get(pk = self.kwargs['pk'])
        context['current_reviewers'] = current_reviewers
        return context

    def get_success_url(self):
        return reverse('chair-submission-details', kwargs={'pk':self.kwargs['pk']})

    def form_valid(self, form):
        reviewers = form.cleaned_data['reviewers']
        submission = ConferenceSubmission.objects.get(pk = self.kwargs['pk'])
        for reviewer in reviewers:
            submission.reviewers.add(reviewer)
            ConferenceUserRole.objects.create(role_conference=submission.conference, role_user=reviewer, role=2)
        return super(AddAReviewer, self).form_valid(form)


def delete_reviewer(request, submid, reviewerid):
    submission = ConferenceSubmission.objects.get(pk=submid)
    reviewer = CustomUser.objects.get(pk=reviewerid)
    submission.reviewers.remove(reviewer)
    conference_role = ConferenceUserRole.objects.get(role_conference=submission.conference, role_user=reviewer, role=2)
    conference_role.delete()
    return redirect('chair-submission-details', pk=submid)


class ReviewerAssignedSubmissions(LoginRequiredMixin, ListView):
    model = ConferenceSubmission
    template_name = 'conference/reviewer/reviewer_submissions_list.html'
    context_object_name = 'reviewer_submissions_list'
    
    def get_queryset(self):
        queryset = ConferenceSubmission.objects.filter(reviewers= self.request.user)
        return queryset


class ReviewerSubmissionReview(LoginRequiredMixin, CreateView):
    model = ConferenceSubmissionReview
    fields = ['review_text', 'review_score', 'review_confidence']
    template_name = 'conference/reviewer/reviewer_submission_review.html'

    def get_context_data(self, **kwargs):
        # Add the submission data to the context
        context = super(ReviewerSubmissionReview, self).get_context_data(**kwargs)
        submission = ConferenceSubmission.objects.get(pk=self.kwargs['submid'])
        context['submission_details'] = submission
        # Add the reviews of the submission to the context.
        reviews = ConferenceSubmissionReview.objects.filter(review_submission=self.kwargs['submid'])
        context['reviews'] = reviews
        return context

    def form_valid(self, form):
        review = form.save(commit=False)
        review.review_conference = Conference.objects.get(submission_conference = self.kwargs['submid']) # add the conference instance to the submission
        review.review_submission = ConferenceSubmission.objects.get(pk = self.kwargs['submid']) # add the conference instance to the submission
        review.review_reviewer = self.request.user
        review.save()
        form.save_m2m()
        return super(ReviewerSubmissionReview,self).form_valid(review)

    def get_success_url(self):
        return reverse('reviewer-submission-reviews-discussions', kwargs={'submid': self.kwargs['submid']})

class ReviewerSubmissionReviewsAndDiscussions(LoginRequiredMixin, CreateView):
    model = ConferenceSubmissionDiscussion
    fields = ['discussion_text']
    template_name = 'conference/reviewer/reviewer_submission_reviews_and_discussions.html'

    def get_context_data(self, **kwargs):
        # Add the submission data to the context
        context = super(ReviewerSubmissionReviewsAndDiscussions, self).get_context_data(**kwargs)
        submission = ConferenceSubmission.objects.get(pk=self.kwargs['submid'])
        context['submission_details'] = submission
        # Add the reviews of the submission to the context.
        reviews = ConferenceSubmissionReview.objects.filter(review_submission=self.kwargs['submid'])
        context['reviews'] = reviews
        # Add the discussions of the submission to the context.
        discussions = ConferenceSubmissionDiscussion.objects.filter(discussion_submission=self.kwargs['submid'])
        context['discussions'] = discussions
        return context

    def form_valid(self, form):
        discussion = form.save(commit=False)
        discussion.discussion_conference = Conference.objects.get(
            submission_conference=self.kwargs['submid'])  # add the conference instance to the submission
        discussion.discussion_submission = ConferenceSubmission.objects.get(
            pk=self.kwargs['submid'])  # add the conference instance to the submission
        discussion.discussion_reviewer = self.request.user
        discussion.save()
        form.save_m2m()
        return super(ReviewerSubmissionReviewsAndDiscussions, self).form_valid(discussion)

    def get_success_url(self):
        return reverse('reviewer-submission-reviews-discussions', kwargs={'submid': self.kwargs['submid']})