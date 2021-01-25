from django.contrib import admin
from .models import Conference, ConferencePCMInvitation, ConferenceSubmission, ConferenceUserRole, ConferenceSubmissionReview, ConferenceSubmissionDiscussion



# Register your models here.
admin.site.register(Conference)
admin.site.register(ConferencePCMInvitation)
admin.site.register(ConferenceSubmission)
admin.site.register(ConferenceUserRole)
admin.site.register(ConferenceSubmissionReview)
admin.site.register(ConferenceSubmissionDiscussion)
