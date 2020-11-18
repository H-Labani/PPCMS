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
    queryset = Conference.objects.filter(name__icontains='A', conferencecfp__cfp_active=True)
    #get_list_or_404(Conference,
                                          #conferencecfp__cfp_active=True,
                                          #name="TestCon" )
    def search_cfp(self):
        conference_list = get_list_or_404(Conference,
                                          ConferenceCFP__cfp_active=True,
                                          name=self.request.GET.get('search_term'))
        return conference_list