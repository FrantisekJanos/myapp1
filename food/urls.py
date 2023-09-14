from django.urls import path
from . import views

urlpatterns = [
    path('pizza-day-list/', views.AllPizzaDayView.as_view(), name='pizza_day_list'),
    path('pizza-day/<slug:slug>', views.SinglePizzaDayView.as_view(), name='single_pizza_day'),
    path('create-pizza-day/', views.create_pizza_day, name='create_pizza_day'),
    path('delete-pizza-day/<slug:slug>', views.DeletePizzaDay.as_view(), name='delete_pizza_day'),
    path('registration-status-change', views.RegistrationStatusChange.as_view(), name='registration_status_change'),
    path('lunch-list', views.LunchWeekList.as_view(), name='lunch_week_list'),
    path('order-lunch/<uuid:uuid>', views.OrderLunch.as_view(), name='order_lunch'),
    path('order-overview/', views.OrderOverview.as_view(), name='order_overview'),
    path('my-order-list/', views.OrderWeekList.as_view(), name='my_order_list'),
    path('lunch-account-overview/', views.lunch_account_overview, name='lunch_account_overview'),
    path('edit-lunch-account/<uuid:uuid>', views.EditLunchAccount.as_view(), name='edit_lunch_account'),
    path('create-meal/', views.CreateMeal.as_view(), name='create_meal'),
    path('create-menu/', views.CreateMenu.as_view(), name='create_menu'),
    path('crate-menu-option', views.CreateLunchMenuOption.as_view(), name='create_menu_option'),
    #UPDEJTOVAT
    path('lunch-meal-list/', views.LunchMealListView.as_view(), name='lunch_meal_list'),
    path('lunch-meal-delete/<str:pk>', views.LunchMealDeleteView.as_view(), name='lunch_meal_delete'),
    path('lunch-menu-option-delete/<str:pk>', views.LunchMenuOptionDeleteView.as_view(), name='lunch_menu_option_delete'),
    path('edit-available-portions/<uuid:uuid>', views.EditAvailablePortions.as_view(), name='edit_available_portions'),
    path('transactions', views.Transactions.as_view(), name='transactions')



]