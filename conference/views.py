from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from conference.models import Conference
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy


@login_required
def index(request):

    # List the conferences
    conferences_list = Conference.objects.all()
    # Create context
    context= {
        'conferences_list': conferences_list,
    }

    # Render the html page
    return render(request, 'index.html', context=context)

# Display the details of a conference using the CID
class ConferenceDetailView(LoginRequiredMixin ,generic.DetailView):
    model = Conference


# Create a new conference
class ConferenceCreate(LoginRequiredMixin, CreateView):
    model = Conference
    fields = ['name', 'acronym', 'web_page', 'venue', 'city', 'country', 'start_date', 'end_date' ]

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.chair = self.request.user
        candidate.save()
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
