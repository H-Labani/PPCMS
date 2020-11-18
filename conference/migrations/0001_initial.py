# Generated by Django 3.1 on 2020-11-10 13:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('CID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter the conference name', max_length=200)),
                ('acronym', models.CharField(help_text='Enter the Acronym of the conferece', max_length=50, null=True)),
                ('web_page', models.URLField(default='', help_text='Enter the web page of your conference')),
                ('venue', models.CharField(help_text='Enter the venue of the conference', max_length=200, null=True)),
                ('city', models.CharField(default='', help_text='Enter the city of the conference', max_length=200)),
                ('country', models.CharField(default='', help_text='Enter the country/region of the conference', max_length=200)),
                ('start_date', models.DateField(blank=True, default=datetime.date.today, help_text='Enter the start date of the conference')),
                ('end_date', models.DateField(blank=True, default=datetime.date.today, help_text='Enter the end date of the conference')),
                ('submission_deadline', models.DateField(blank=True, help_text='Enter the submission deadline of the conference', null=True)),
                ('phase', models.CharField(blank=True, default='', max_length=100)),
                ('PCM', models.ManyToManyField(blank=True, default='', related_name='conference_PCM', to=settings.AUTH_USER_MODEL)),
                ('chair', models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='conference_chair', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
