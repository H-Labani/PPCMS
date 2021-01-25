# Generated by Django 3.1.3 on 2021-01-22 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0023_auto_20210119_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('abstract', models.TextField()),
                ('submission_date', models.DateField(default=django.utils.timezone.now)),
                ('paper_file', models.FileField(upload_to='submissions/')),
                ('authors', models.ManyToManyField(related_name='submission_authors', to=settings.AUTH_USER_MODEL)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submission_conference', to='conference.conference')),
                ('reviewers', models.ManyToManyField(related_name='submission_reviewers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceSubmissionReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('review_score', models.IntegerField(choices=[(-1, 'weak reject'), (0, 'borderline paper'), (1, 'weak accept'), (-2, 'strong reject'), (2, 'strong accept')])),
                ('review_confidence', models.IntegerField(choices=[(4, 'high'), (1, 'very low'), (3, 'normal'), (2, 'low'), (5, 'very high')])),
                ('review_conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_conference', to='conference.conference')),
                ('review_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_submission', to='conference.conferencesubmission')),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceUserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'chair'), (2, 'reviewer'), (3, 'author')])),
                ('role_conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_conference', to='conference.conference')),
                ('role_user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='role_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('role_conference', 'role_user', 'role')},
            },
        ),
        migrations.RenameModel(
            old_name='ConferencePCMInvitations',
            new_name='ConferencePCMInvitation',
        ),
        migrations.AlterUniqueTogether(
            name='conferenceuserroles',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='conferenceuserroles',
            name='role_conference',
        ),
        migrations.RemoveField(
            model_name='conferenceuserroles',
            name='role_user',
        ),
        migrations.DeleteModel(
            name='ConferenceSubmissions',
        ),
        migrations.DeleteModel(
            name='ConferenceUserRoles',
        ),
    ]