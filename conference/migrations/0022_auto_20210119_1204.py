# Generated by Django 3.1.3 on 2021-01-19 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0021_auto_20210119_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferenceuserroles',
            name='role',
            field=models.IntegerField(choices=[(3, 'author'), (1, 'chair'), (2, 'reviewer')], max_length=2),
        ),
    ]
