from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import AccidentSerializer, TaskSerializer#, UserSerializer, RoleSerializer, WorkcenterSerializer
from maintenance.models import Accident, MaintenanceTask

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/maintenance/accidents'},
        {'GET': '/api/maintenance/ accidents/id'},
        {'GET': '/api/maintenance/accidents/id/task/id'},

        {'POST': '/api/maintenance/accidents'},
        {'POST': '/api/maintenance/accidents/id'},
        {'POST': '/api/maintenance/accidents/id/task/id'},

        {'POST': '/api/maintenance/users/token'},
        {'POST': '/api/maintenance/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getAccidents(request):
    accidents = Accident.objects.all()
    serializer = AccidentSerializer(accidents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAccident(request, pk):
    accident = Accident.objects.get(id=pk)
    serializer = AccidentSerializer(accident)
    return Response(serializer.data)

@api_view(['GET'])
def getTasks(request, pk):
    accident = Accident.objects.get(id=pk)
    tasks = MaintenanceTask.objects.filter(accident=accident)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)