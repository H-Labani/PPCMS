# Generated by Django 3.1.3 on 2021-01-25 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0034_auto_20210125_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_confidence',
            field=models.IntegerField(choices=[(5, 'very high'), (3, 'normal'), (4, 'high'), (2, 'low'), (1, 'very low')]),
        ),
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_score',
            field=models.IntegerField(choices=[(-2, 'strong reject'), (0, 'borderline paper'), (2, 'strong accept'), (1, 'weak accept'), (-1, 'weak reject')]),
        ),
    ]