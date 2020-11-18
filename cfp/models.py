from django.db import models
from conference.models import Conference


# Create your models here.

class ConferenceCFP(models.Model):
    abstract_deadline = models.DateField()
    submission_deadline = models.DateField()
    conference_id = models.ForeignKey('conference.Conference', on_delete=models.CASCADE, related_name="cfp", default=1)
    cfp_active = models.BooleanField(default=False)
