from django.db import models
from django.contrib.auth.models import User

import uuid
from users.models import Profile, Workcenter, Role
# Create your models here.



class Accident(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    short_text = models.CharField(max_length=200, blank=True, null=True)
    long_text = models.TextField(max_length=2000, blank=True, null=True)
    PROGRESS_CHOICES = [
        ('N', 'Not started'),
        ('I', 'In progress'),
        ('C', 'Completed'),
    ]
    progress = models.CharField(max_length=1, choices=PROGRESS_CHOICES)
    PRIORITY_CHOICES = [
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'Important'),
        ('4', 'Urgent'),
    ]
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    workcenter = models.ForeignKey(Workcenter, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    accident_image = models.ImageField(null=True, blank=True, upload_to='accident_images/', default="accident_images/accident_image.png")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,)

    class AdditionalImage(models.Model):
        accident = models.ForeignKey('Accident', related_name='additional_images', on_delete=models.CASCADE, blank=True, null=True)
        image = models.ImageField(upload_to='additional_images/')
        created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.short_text)


class MaintenanceTask(models.Model):
    accident = models.ForeignKey('Accident', related_name='additional_image', on_delete=models.CASCADE, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    short_text = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    PROGRESS_CHOICES = [
        ('N', 'Not started'),
        ('I', 'In progress'),
        ('C', 'Completed'),
    ]
    progress = models.CharField(max_length=1, choices=PROGRESS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.short_text)

