from django.shortcuts import render, get_list_or_404
from conference.models import Conference
from django.views.generic import TemplateView, ListView
from .models import ConferenceCFP
# Create your views here.


class CFPView(ListView):
    template_name = "cfp_search.html"

    def get_queryset(self):
        if(not self.request.GET.get('search_term')):
            queryset = Conference.objects.filter(cfp__cfp_active=True)
        else:
            queryset = Conference.objects.filter(name__icontains=self.request.GET.get('search_term'), cfp__cfp_active=True)
        return queryset


class CFPSearchResult(ListView):
    model = Conference
    template_name = "cfp_search_result.html"

    def get_queryset(self):
        queryset = Conference.objects.filter(name__icontains=self.request.GET.get('search_term'), cfp__cfp_active=True)
        return queryset