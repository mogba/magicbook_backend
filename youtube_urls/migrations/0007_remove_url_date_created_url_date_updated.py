# Generated by Django 5.1.1 on 2024-10-01 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_urls', '0006_url_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='date_created',
        ),
        migrations.AddField(
            model_name='url',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date updated'),
        ),
    ]
