# Generated by Django 3.1.3 on 2021-01-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0024_auto_20210122_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_confidence',
            field=models.IntegerField(choices=[(4, 'high'), (5, 'very high'), (3, 'normal'), (1, 'very low'), (2, 'low')]),
        ),
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_score',
            field=models.IntegerField(choices=[(0, 'borderline paper'), (2, 'strong accept'), (-2, 'strong reject'), (1, 'weak accept'), (-1, 'weak reject')]),
        ),
        migrations.AlterField(
            model_name='conferenceuserrole',
            name='role',
            field=models.IntegerField(choices=[(2, 'reviewer'), (1, 'chair'), (3, 'author')]),
        ),
    ]