from django.urls import path
from conference import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:pk>', views.ConferenceDetailView.as_view(), name='conference-detail'),
    path('create', views.ConferenceCreate.as_view(), name='conference-create'),
    path('update/<uuid:pk>/', views.ConferenceUpdate.as_view(), name='conference-update'),
    path('delete/<uuid:pk>/', views.ConferenceDelete.as_view(), name='conference-delete'),
    path('invite/<uuid:pk>/', views.InvitePCMView.as_view(), name='invite-pcm'),
    path('invite/success/<uuid:pk>/', views.InvitePCMView.as_view(), name='invitation-success'),
    path('next_phase/<uuid:pk>/', views.next_phase, name='next-phase'),
    path('submit_a_paper/<uuid:pk>/', views.SubmissionCreate.as_view(), name='paper-submit'),
    path('my_submissions/', views.SubmissionsList.as_view(), name='my-submissions'),
    path('submission/<pk>', views.SubmissionDetails.as_view(), name='submission-detail'),
    path('submission/update/<pk>', views.SubmissionUpdate.as_view(), name='submission-update'),
    path('submission/delete/<pk>', views.SubmissionDelete.as_view(), name='submission-delete'),

]