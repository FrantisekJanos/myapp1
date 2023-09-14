from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('login_register/', views.register_user, name='login_register'),

    path('profiles', views.profiles, name='profiles'),
    path('user_profile/<str:pk>', views.user_profile, name='user_profile'),
    path('user_account/', views.user_account, name='user_account'),
    path('edit_account/', views.edit_account, name='edit_account'),
]