# Generated by Django 3.1.3 on 2020-12-02 16:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0010_auto_20201202_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferencepcminvitations',
            name='invitation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]