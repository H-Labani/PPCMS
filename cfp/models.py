from django.db import models


# Create your models here.

class ConferenceCFP(models.Model):
    abstract_deadline = models.DateField()
    submission_deadline = models.DateField()
    conference_id = models.ForeignKey('conference.Conference', on_delete=models.CASCADE, related_name="cfp", default=1)
    cfp_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

"""
    def get_absolute_url(self):
        #Returns the url to access a particular instance of the model.
        return reverse('cfp-detail', args=[str(self.id)])

"""