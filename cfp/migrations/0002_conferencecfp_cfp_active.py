# Generated by Django 3.1 on 2020-11-17 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferencecfp',
            name='cfp_active',
            field=models.BooleanField(default=False),
        ),
    ]
