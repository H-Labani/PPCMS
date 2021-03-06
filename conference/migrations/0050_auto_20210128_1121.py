# Generated by Django 3.1.3 on 2021-01-28 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0049_auto_20210128_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferencesubmission',
            name='decision',
            field=models.IntegerField(choices=[(1, 'accept'), (2, 'reject')], null=True),
        ),
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_confidence',
            field=models.IntegerField(choices=[(4, 'high'), (1, 'very low'), (3, 'normal'), (5, 'very high'), (2, 'low')]),
        ),
        migrations.AlterField(
            model_name='conferencesubmissionreview',
            name='review_score',
            field=models.IntegerField(choices=[(-1, 'weak reject'), (2, 'strong accept'), (-2, 'strong reject'), (1, 'weak accept'), (0, 'borderline paper')]),
        ),
        migrations.AlterField(
            model_name='conferenceuserrole',
            name='role',
            field=models.IntegerField(choices=[(2, 'reviewer'), (3, 'author'), (1, 'chair')]),
        ),
    ]
