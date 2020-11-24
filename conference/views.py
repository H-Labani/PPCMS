from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from conference.models import Conference
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from guardian.shortcuts import assign_perm, get_objects_for_user, get_objects_for_group
from django.contrib.auth.models import Group


@login_required
def index(request):

    # List the conferences
    conferences_list = get_objects_for_user(request.user, 'conference.view_conference')
    # Create context
    context= {
        'conferences_list': conferences_list,
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
