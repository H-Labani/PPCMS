# Generated by Django 3.1.3 on 2021-01-26 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0039_auto_20210125_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_confidence',
            field=models.IntegerField(choices=[(3, 'normal'), (5, 'very high'), (2, 'low'), (1, 'very low'), (4, 'high')]),
        ),
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_score',
            field=models.IntegerField(choices=[(-1, 'weak reject'), (-2, 'strong reject'), (0, 'borderline paper'), (1, 'weak accept'), (2, 'strong accept')]),
        ),
        migrations.AlterField(
            model_name='conferenceuserrole',
            name='role',
            field=models.IntegerField(choices=[(2, 'reviewer'), (1, 'chair'), (3, 'author')]),
        ),
    ]
