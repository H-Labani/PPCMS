# Generated by Django 3.1.3 on 2020-11-30 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0005_auto_20201129_1717'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='conferencepcminvitations',
            unique_together={('conference', 'invitee')},
        ),
    ]
