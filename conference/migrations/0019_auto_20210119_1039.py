# Generated by Django 3.1.3 on 2021-01-19 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0018_conferencesubmissions_reviewers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='acronym',
            field=models.CharField(help_text='Enter the Acronym of the conference', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='conferencepcminvitations',
            name='conference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_conference', to='conference.conference'),
        ),
        migrations.AlterField(
            model_name='conferencepcminvitations',
            name='inviter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_inviter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='conferencesubmissions',
            name='authors',
            field=models.ManyToManyField(related_name='submission_authors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='conferencesubmissions',
            name='conference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submission_conference', to='conference.conference'),
        ),
        migrations.AlterField(
            model_name='conferencesubmissions',
            name='reviewers',
            field=models.ManyToManyField(related_name='submission_reviewers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ConferenceUserRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[(1, 'chair'), (3, 'author'), (2, 'reviewer')], max_length=10)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_conference', to='conference.conference')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='role_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('conference', 'user', 'role')},
            },
        ),
    ]
