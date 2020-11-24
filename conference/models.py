from django.db import models
import uuid
from django.urls import reverse
from datetime import date
from account.models import CustomUser

class Conference(models.Model):
    """" This is the class for the conference model/table"""
    CID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #The Conference ID
    name = models.CharField(max_length=200, help_text='Enter the conference name') #The conference name
    acronym = models.CharField(max_length=50, help_text='Enter the Acronym of the conferece', null=True) #The conference Acronym
    web_page = models.URLField(max_length=200, help_text='Enter the web page of your conference', default="") #The conference web page
    venue = models.CharField(max_length=200, help_text="Enter the venue of the conference", null=True) # Location
    city = models.CharField(max_length=200, help_text="Enter the city of the conference", default="") # Location
    country = models.CharField(max_length=200, help_text="Enter the country/region of the conference", default="") # Location
    start_date = models.DateField(help_text="Enter the start date of the conference", default=date.today, blank=True) # The conference data
    end_date = models.DateField(help_text="Enter the end date of the conference", default=date.today, blank=True) # The conference data
    phase = models.CharField(max_length=100, blank= True, default="")
    PCM = models.ManyToManyField(CustomUser, related_name="conference_PCM", blank=True, default="")
    chair = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name="conference_chair", default=1)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('conference-detail', args=[str(self.CID)])
