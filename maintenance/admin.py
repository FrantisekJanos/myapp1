from django.contrib import admin
from .models import Accident, MaintenanceTask
# Register your models here.


admin.site.register(Accident)
admin.site.register(MaintenanceTask)
admin.site.register(Accident.AdditionalImage)
