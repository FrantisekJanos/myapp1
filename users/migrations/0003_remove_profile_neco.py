# Generated by Django 4.2.5 on 2023-09-12 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_neco'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='neco',
        ),
    ]