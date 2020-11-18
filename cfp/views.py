from django.shortcuts import render, get_list_or_404
from conference.models import Conference
from django.views.generic import TemplateView, ListView
from .models import ConferenceCFP
# Create your views here.


class CFPView(TemplateView):
    template_name = "cfp_search.html"



class CFPSearchResult(ListView):
    model = Conference
    template_name = "cfp_search_result.html"
    #queryset = ConferenceCFP.objects.filter(conference_id__name__icontains='A')
    #queryset = Conference.objects.filter(name__icontains=self.request.GET.get('search_term'), cfp__cfp_active=True)
    #queryset = queryset.
    #get_list_or_404(Conference,
                                          #conferencecfp__cfp_active=True,
                                          #name="TestCon" )
    def get_queryset(self):
        queryset = Conference.objects.filter(name__icontains=self.request.GET.get('search_term'), cfp__cfp_active=True)
        return queryset