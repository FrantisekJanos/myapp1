from django.contrib import admin
from .models import PizzaDayDay, PizzaOrder, LunchOrder, LunchMeal, LunchMenu, LunchMenuOption, TransactionHistory

# Register your models here.
admin.site.register(PizzaDayDay)
admin.site.register(PizzaOrder)
admin.site.register(LunchMenu)
admin.site.register(LunchMenuOption)
admin.site.register(LunchMeal)
admin.site.register(LunchOrder)
admin.site.register(TransactionHistory)
