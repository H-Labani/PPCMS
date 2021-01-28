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
    acronym = models.CharField(max_length=50, help_text='Enter the Acronym of the conference', null=True) #The conference Acronym
    web_page = models.URLField(max_length=200, help_text='Enter the web page of your conference', default="") #The conference web page
    venue = models.CharField(max_length=200, help_text="Enter the venue of the conference", null=True) # Location
    city = models.CharField(max_length=200, help_text="Enter the city of the conference", default="") # Location
    country = models.CharField(max_length=200, help_text="Enter the country/region of the conference", default="") # Location
    start_date = models.DateField(help_text="Enter the start date of the conference", default=timezone.now, blank=True) # The conference data
    end_date = models.DateField(help_text="Enter the end date of the conference", default=timezone.now, blank=True) # The conference data
    phase = models.IntegerField(choices=((1,'registration'),(2,'submission'),(3,'review'),(4,'discussion'),(5,'notification')), default=1)
    chair = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name="conference_chair", default=1)

    # class Meta:
    #     permissions = (
    #         ('chair', 'Chair'),
    #         ('reviewer', 'Reviewer'),
    #     )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('conference-details', args=[str(self.CID)])


class ConferenceUserRole(models.Model):
    role_conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='role_conference')
    role_user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name='role_user')

    roles_choices = {(1, 'chair'),
                     (2, 'reviewer'),
                     (3, 'author')}

    role = models.IntegerField(choices=roles_choices)

    class Meta:
        unique_together = ('role_conference', 'role_user', 'role')
        ordering = ['role']

    def __str__(self):
        return self.role_conference.name + '_' + self.role_user.first_name + '_' + self.get_role_display()


class ConferencePCMInvitationsManager(models.Manager):

    def get_expired(self):
        return self.filter(self.get_expired_query())

    def get_active(self):
        return self.exclude(self.get_expired_query())

    def get_expired_query(self):
        expiration_date = timezone.now() - timedelta(
            days=settings.INVITATION_EXPIRY)
        query = Q(accepted=True) | Q(invitation_date__lt=expiration_date)
        return query

    def delete_expired_confirmations(self):
        self.all_expired().delete()


class ConferencePCMInvitation(models.Model):
    invitee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='invitation_invitee')
    inviter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='invitation_inviter')
    invitation_date = models.DateField(default=timezone.now)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='invitation_conference')
    role = models.IntegerField(choices=((1,'chair'),(2,'member'),), default=2)
    accepted = models.BooleanField(default=False)
    objects = ConferencePCMInvitationsManager()

    class Meta:
        unique_together = ('conference', 'invitee', 'role')

    def get_roles_str(self):
        if self.role == 1:
            return "chair"
        elif self.role == 2:
            return "PC member"


class ConferenceSubmission(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='submission_conference')
    authors = models.ManyToManyField(CustomUser, related_name='submission_authors')
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    submission_date = models.DateField(default=timezone.now)
    paper_file = models.FileField(upload_to='submissions/')
    reviewers = models.ManyToManyField(CustomUser, related_name='submission_reviewers')
    decision = models.IntegerField(choices=((1,'accept'),(2, 'reject')), null=True)

    # class Meta:
    #     permissions = (
    #         ('chair', 'Chair'),
    #         ('reviewer', 'Reviewer'),
    #         ('author', 'Author'),
    #     )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('submission-details', args=[self.id])


class ConferenceSubmissionReview(models.Model):
    review_conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='review_conference')
    review_submission = models.ForeignKey(ConferenceSubmission, on_delete=models.CASCADE, related_name='review_submission')
    review_reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='review_reviewer' , default=1)
    review_text = models.TextField()
    scores = {
        (-2, 'strong reject'),
        (-1, 'weak reject'),
        (0, 'borderline paper'),
        (1, 'weak accept'),
        (2, 'strong accept'),
    }

    confidence = {
        (1, 'very low'),
        (2, 'low'),
        (3, 'normal'),
        (4, 'high'),
        (5, 'very high'),
    }
    review_score = models.IntegerField(choices=scores)
    review_confidence = models.IntegerField(choices=confidence)
    review_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['review_date_time']
        # permissions = (
        #     ('chair', 'Chair'),
        #     ('reviewer', 'Reviewer'),
        #     ('author', 'Author'),
        # )

    def __str__(self):
        return self.review_submission.title


class ConferenceSubmissionDiscussion(models.Model):
    discussion_conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='discussion_conference')
    discussion_submission = models.ForeignKey(ConferenceSubmission, on_delete=models.CASCADE,
                                          related_name='discussion_submission')
    discussion_reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='discussion_reviewer',
                                        default=1)
    discussion_text = models.TextField()
    discussion_date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['discussion_date_time']
        # permissions = (
        #     ('chair', 'Chair'),
        #     ('reviewer', 'Reviewer'),
        #     ('author', 'Author'),
        # )

    def __str__(self):
        return self.discussion_submission.title