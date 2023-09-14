from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('workcenters/', views.workcenter_list, name='workcenter_list'),
    path('workcenter/<str:pk>', views.workcenter_detail, name='workcenter_detail'),
    path('accident/<str:pk>', views.accident_detail, name='accident_detail'),
    path('create-accident/', views.create_accident, name='create_accident'),
    path('edit-accident/<uuid:uuid>', views.EditAccident.as_view(), name='edit_accident'),
    path('delete-accident/<str:pk>', views.DeleteAccident.as_view(), name='delete_accident'),
    path('create-task/<uuid:uuid>', views.CreateTask.as_view(), name='create_task'),
    path('edit-task/<uuid:uuid>', views.EditTask.as_view(), name='edit_task'),
    path('edit-task-progress/<uuid:uuid>', views.EditTaskProgress.as_view(), name='edit_task_progress'),
    path('delete-task/<uuid:uuid>', views.DeleteTask.as_view(), name='delete_task'),
    path('no-permission/<str:pk>', views.no_permission, name='no_permission'),
    path('no-permission-workcenter/<str:pk>', views.no_permission_workcenter, name='no_permission_workcenter'),
    path('create-workcenter/>', views.CreateWorkcenter.as_view(), name='create_workcenter'),
    path('delete-workcenter/<str:pk>', views.DeleteWorkcenter.as_view(), name='delete_workcenter')

]