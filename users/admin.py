from django.contrib import admin
from .models import Profile, Role, Workcenter
# Register your models here.

admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(Workcenter)