from django.urls import path, include
from account.views import RegisterView
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('login/', LoginView.as_view(redirect_authenticated_user=True)),
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register')
]