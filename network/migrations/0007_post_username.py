# Generated by Django 4.0.6 on 2022-07-22 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_profile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='username',
            field=models.TextField(blank=True),
        ),
    ]
