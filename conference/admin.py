from django.contrib import admin
from .models import Conference, ConferencePCMInvitations, ConferenceSubmissions



# Register your models here.
admin.site.register(Conference)
admin.site.register(ConferencePCMInvitations)
admin.site.register(ConferenceSubmissions)
