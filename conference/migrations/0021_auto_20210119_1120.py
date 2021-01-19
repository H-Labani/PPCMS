# Generated by Django 3.1.3 on 2021-01-19 11:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0020_auto_20210119_1113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conferenceuserroles',
            old_name='conference',
            new_name='role_conference',
        ),
        migrations.RenameField(
            model_name='conferenceuserroles',
            old_name='user',
            new_name='role_user',
        ),
        migrations.AlterField(
            model_name='conferenceuserroles',
            name='role',
            field=models.CharField(choices=[(3, 'author'), (1, 'chair'), (2, 'reviewer')], max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='conferenceuserroles',
            unique_together={('role_conference', 'role_user', 'role')},
        ),
    ]