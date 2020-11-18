from django.urls import path
from conference import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:pk>', views.ConferenceDetailView.as_view(), name='conference-detail'),
    path('create/', views.ConferenceCreate.as_view(), name='conference-create'),
    path('<uuid:pk>/update/', views.ConferenceUpdate.as_view(), name='conference-update'),
    path('<uuid:pk>/delete/', views.ConferenceDelete.as_view(), name='conference-delete'),

]