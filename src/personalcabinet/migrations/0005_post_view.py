# Generated by Django 3.1.4 on 2021-03-24 18:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personalcabinet', '0004_auto_20210324_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='view',
            field=models.ManyToManyField(related_name='view', to=settings.AUTH_USER_MODEL),
        ),
    ]
