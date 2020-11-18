# Generated by Django 3.1 on 2020-11-11 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conference', '0002_remove_conference_submission_deadline'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceCFP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abstract_deadline', models.DateField()),
                ('submission_deadline', models.DateField()),
                ('conference_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='conference_chair', to='conference.conference')),
            ],
        ),
    ]
