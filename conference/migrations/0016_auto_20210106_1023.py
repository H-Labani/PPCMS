# Generated by Django 3.1.3 on 2021-01-06 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0015_conferencesubmissions_conference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferencesubmissions',
            name='paper_file',
            field=models.FileField(upload_to='submissions/'),
        ),
    ]
