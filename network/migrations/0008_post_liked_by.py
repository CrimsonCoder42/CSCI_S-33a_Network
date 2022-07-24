# Generated by Django 4.0.6 on 2022-07-24 11:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_post_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='liked_by',
            field=models.ManyToManyField(related_name='post_liked_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
