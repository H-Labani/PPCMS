from django.urls import path
from conference import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:pk>', views.PublicConferenceDetailView.as_view(), name='conference-details'),

    #Chair's URLs:
    path('create', views.ConferenceCreate.as_view(), name='conference-create'),
    path('manage/<uuid:pk>', views.ChairConferenceManageView.as_view(), name='conference-manage'),
    path('update/<uuid:pk>/', views.ConferenceUpdate.as_view(), name='conference-update'),
    path('delete/<uuid:pk>/', views.ConferenceDelete.as_view(), name='conference-delete'),
    path('next_phase/<uuid:pk>/', views.next_phase, name='next-phase'),

    path('submissions/<uuid:pk>/', views.ViewConferenceSubmissions.as_view(), name='view-submissions'),
    path('submission/<pk>', views.ChairSubmissionDetails.as_view(), name='chair-submission-details'),
    path('add_reviewer/<pk>/', views.AddAReviewer.as_view(), name='add-reviewer'),
    path('delete_reviewer/<submid>-<reviewerid>/', views.delete_reviewer, name='delete-reviewer'),

    path('reviewer/submissions_list/<uuid:pk>/', views.ReviewerAssignedSubmissions.as_view(),
         name='reviewer-assigned-submissions'),
    path('reviewer/submission_review/<submid>/', views.ReviewerSubmissionReview.as_view(),
         name='reviewer-submission-review'),
    path('reviewer/submission_reviews_and_discussions/<submid>/', views.ReviewerSubmissionReviewsAndDiscussions.as_view(),
         name='reviewer-submission-reviews-discussions'),

    path('invite/<uuid:pk>/', views.InvitePCMView.as_view(), name='invite-pcm'),
    path('invite/success/<uuid:pk>/', views.InvitePCMView.as_view(), name='invitation-success'),

    #Author's URLs
    path('submit_a_paper/<uuid:pk>/', views.SubmissionCreate.as_view(), name='paper-submit'),
    path('my_submissions/', views.SubmissionsList.as_view(), name='my-submissions'),
    path('submission/<pk>', views.MySubmissionDetails.as_view(), name='submission-details'),
    path('submission/update/<pk>', views.SubmissionUpdate.as_view(), name='submission-update'),
    path('submission/delete/<pk>', views.SubmissionDelete.as_view(), name='submission-delete'),


]