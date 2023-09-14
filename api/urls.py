from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes, name="routes"),
    path('accidents/', views.getAccidents, name="accidents"),
    path('accidents/<str:pk>/', views.getAccident, name="accident"),
    path('accidents/<str:pk>/tasks/', views.getTasks, name="tasks"),

]
