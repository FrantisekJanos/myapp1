# Generated by Django 4.2.5 on 2023-09-12 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('short_text', models.CharField(blank=True, max_length=200, null=True)),
                ('long_text', models.TextField(blank=True, max_length=2000, null=True)),
                ('progress', models.CharField(choices=[('N', 'Not started'), ('I', 'In progress'), ('C', 'Completed')], max_length=1)),
                ('priority', models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'Important'), ('4', 'Urgent')], max_length=1)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('accident_image', models.ImageField(blank=True, default='accident_images/accident_image.png', null=True, upload_to='accident_images/')),
                ('created_by', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workcenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.workcenter')),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('short_text', models.CharField(blank=True, max_length=200, null=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('progress', models.CharField(choices=[('N', 'Not started'), ('I', 'In progress'), ('C', 'Completed')], max_length=1)),
                ('accident', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='additional_image', to='maintenance.accident')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='additional_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accident', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='additional_images', to='maintenance.accident')),
            ],
        ),
    ]
