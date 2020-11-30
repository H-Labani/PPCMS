from django.urls import path, include
from .views import CFPView #CFPSearchResult

urlpatterns = [
    path('',  CFPView.as_view(), name='cfp-search'),
    #path('search/', CFPSearchResult.as_view(), name='cfp-search-result'),
]