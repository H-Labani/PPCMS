# Generated by Django 3.1.3 on 2021-01-26 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0040_auto_20210126_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferencepcminvitation',
            name='invitee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_invitee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_confidence',
            field=models.IntegerField(choices=[(5, 'very high'), (3, 'normal'), (1, 'very low'), (4, 'high'), (2, 'low')]),
        ),
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_score',
            field=models.IntegerField(choices=[(-2, 'strong reject'), (1, 'weak accept'), (2, 'strong accept'), (0, 'borderline paper'), (-1, 'weak reject')]),
        ),
        migrations.AlterField(
            model_name='conferenceuserrole',
            name='role',
            field=models.IntegerField(choices=[(2, 'reviewer'), (3, 'author'), (1, 'chair')]),
        ),
    ]
