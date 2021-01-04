from django.db import models
import uuid
from django.urls import reverse
from account.models import CustomUser

from datetime import timedelta
from django.db.models import Q
from django.conf import settings
from django.utils import timezone


class Conference(models.Model):
    """" This is the class for the conference model/table"""
    CID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #The Conference ID
    name = models.CharField(max_length=200, help_text='Enter the conference name') #The conference name
    acronym = models.CharField(max_length=50, help_text='Enter the Acronym of the conferece', null=True) #The conference Acronym
    web_page = models.URLField(max_length=200, help_text='Enter the web page of your conference', default="") #The conference web page
    venue = models.CharField(max_length=200, help_text="Enter the venue of the conference", null=True) # Location
    city = models.CharField(max_length=200, help_text="Enter the city of the conference", default="") # Location
    country = models.CharField(max_length=200, help_text="Enter the country/region of the conference", default="") # Location
    start_date = models.DateField(help_text="Enter the start date of the conference", default=timezone.now, blank=True) # The conference data
    end_date = models.DateField(help_text="Enter the end date of the conference", default=timezone.now, blank=True) # The conference data
    phase = models.CharField(max_length=100, blank= True, default="Registgit ration")
    PCM = models.ManyToManyField(CustomUser, related_name="conference_PCM", blank=True, default="")
    chair = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name="conference_chair", default=1)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('conference-detail', args=[str(self.CID)])


class ConferencePCMInvitationsManager(models.Manager):

    def get_expired(self):
        return self.filter(self.get_expured_query())

    def get_active(self):
        return self.exclude(self.get_expured_query())

    def get_expured_query(self):
        expiration_date = timezone.now() - timedelta(
            days=settings.INVITATION_EXPIRY)
        query = Q(accepted=True) | Q(invitation_date__lt=expiration_date)
        return query

    def delete_expired_confirmations(self):
        self.all_expired().delete()


class ConferencePCMInvitations(models.Model):
    invitee = models.EmailField()
    inviter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inviter')
    invitation_date = models.DateTimeField(default=timezone.now)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='conference_invitation')
    role = models.IntegerField(choices=((1,'chair'),(2,'member')), default=2)
    accepted = models.BooleanField(default=False)
    objects = ConferencePCMInvitationsManager()

    class Meta:
        unique_together = ('conference', 'invitee',)

    def get_roles_str(self):
        if self.role == 1:
            return "chair"
        elif self.role == 2:
            return "member"
