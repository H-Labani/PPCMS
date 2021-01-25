# Generated by Django 3.1.3 on 2021-01-25 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0033_auto_20210125_1036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conferencesubmissiondiscussion',
            options={'ordering': ['discussion_date_time']},
        ),
        migrations.AlterModelOptions(
            name='conferencesubmissionreview',
            options={'ordering': ['review_date_time']},
        ),
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_confidence',
            field=models.IntegerField(choices=[(2, 'low'), (4, 'high'), (1, 'very low'), (3, 'normal'), (5, 'very high')]),
        ),
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_score',
            field=models.IntegerField(choices=[(0, 'borderline paper'), (-1, 'weak reject'), (-2, 'strong reject'), (2, 'strong accept'), (1, 'weak accept')]),
        ),
        migrations.AlterField(
            model_name='conferenceuserrole',
            name='role',
            field=models.IntegerField(choices=[(2, 'reviewer'), (1, 'chair'), (3, 'author')]),
        ),
    ]
