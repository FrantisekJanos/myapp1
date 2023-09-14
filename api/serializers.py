from rest_framework import serializers
from maintenance.models import Accident, MaintenanceTask
from users.models import Profile, Workcenter, Role

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class WorkcenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workcenter
        fields = '__all__'


class AccidentSerializer(serializers.ModelSerializer):
    created_by = ProfileSerializer(many=False)
    workcenter = WorkcenterSerializer(many=False)
    # tasks = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Accident
        fields = '__all__'

    def get_tasks(self, obj):
        # tasks = MaintenanceTask.objects.filter(accident=obj)
        tasks = obj.maintenancetask_set.all()
        serializer = TaskSerializer(tasks, many=True)
        return serializer.data

class TaskSerializer(serializers.ModelSerializer):
    accident = AccidentSerializer(many=False)
    created_by = ProfileSerializer(many=False)
    owner = ProfileSerializer(many=False)
    class Meta:
        model = MaintenanceTask
        fields = '__all__'