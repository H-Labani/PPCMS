from django.urls import path
from conference import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:pk>', views.ConferenceDetailView.as_view(), name='conference-detail'),
    path('create', views.ConferenceCreate.as_view(), name='conference-create'),
    path('update<uuid:pk>/', views.ConferenceUpdate.as_view(), name='conference-update'),
    path('delete<uuid:pk>/', views.ConferenceDelete.as_view(), name='conference-delete'),
    path('invite/<uuid:pk>/', views.InvitePCMView.as_view(), name='invite-pcm'),

]