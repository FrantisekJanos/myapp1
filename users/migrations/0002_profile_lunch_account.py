# Generated by Django 4.2.1 on 2023-08-30 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='lunch_account',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
