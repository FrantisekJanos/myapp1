from django.shortcuts import render, redirect
from django.views import View

from .models import PizzaDayDay, PizzaOrder, LunchMenuOption, LunchOrder, LunchMeal, LunchMenu, TransactionHistory, Profile
from .forms import PizzaOrderForm, CreatePizzadayForm, LunchOrderForm, EditLunchAccountForm, CreateMealForm, CreateMenuForm, CreateLunchMenuOptionForm

from django.db.models import Q, Sum
from django.utils import timezone
from django.views.generic import DeleteView

from django.contrib import messages
from datetime import timedelta, datetime

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

import django_filters

from django.db.models.functions import Lower
#UPDEJTOVAT
from django.urls import reverse_lazy

class HasRequiredRoleMixin:
    '''Funkcionalita pro kontrolu, zda uživatel má požadovanou roli(práva pro přístup k některým stránkám)'''
    def has_required_role(self, user, required_roles):
        user_roles = user.profile.role_set.values_list('name', flat=True)
        return any(role in user_roles for role in required_roles)

class AllPizzaDayView(ListView):
    '''Zobrazí seznam všech pizzadayů a formulář pro objednání pizzy pro aktuálního uživatele'''
    template_name = "food/pizza_day_list.html"
    form_class = PizzaOrderForm

    def get_context_data(self, **kwargs):
        context = {}
        current_date = timezone.now().date()
        last_pizzaday = PizzaDayDay.objects.filter(to_date__gte=current_date).order_by('to_date').first()
        context['last_pizzaday'] = last_pizzaday
        context['form'] = self.form_class(initial={'pizza_day': last_pizzaday})
        context['all_pizzadays'] = PizzaDayDay.objects.order_by('-to_date')
        context['has_lunchmanager_role'] = self.request.user.profile.role_set.filter(name='LunchManager')
        context['current_user'] = self.request.user

        user = self.request.user
        if user.is_authenticated:
            # Zjištění, zda uživatel již objednal pizzu
            has_ordered = PizzaOrder.objects.filter(ordered_by=user.profile, pizza_day=last_pizzaday).exists()
            context['has_ordered'] = has_ordered

        return context


    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Pro odeslání objednávky musíte být přihlášení.')
            return redirect('login')

        form = PizzaOrderForm(request.POST)
        if form.is_valid():
            pizza_order = form.save(commit=False)  # Uložení objednávky do databáze
            pizza_order.ordered_by = request.user.profile  # Předvyplnění ordered_by
            pizza_order.save()  # Uložení objednávky
            messages.success(request, 'Objednávka byla úspěšně odeslána.')
            return redirect('pizza_day_list')
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class SinglePizzaDayView(View):
    template_name = 'food/pizza_day_detail.html'
    model = PizzaDayDay


    def get(self, request, slug):
        pizzaday = PizzaDayDay.objects.get(slug=slug)

        # Získání hodnoty filtru pro selection a to_time
        selection_filter = request.GET.get('selection-selection', None)
        time_filter = request.GET.get('time-selection', None)

        # Vytvoření Q objektu pro kombinaci filtrů
        q_filters = Q(pizza_day=pizzaday)
        if selection_filter:
            q_filters &= Q(selection=selection_filter)
        if time_filter:
            q_filters &= Q(to_time=time_filter)

        # Filtrování objednávek pomocí kombinovaných filtrů
        orders = PizzaOrder.objects.filter(q_filters)

        # Sčítání vyfiltrovaných položek
        count_filtered = orders.count()

        context = {
            'pizzaday': pizzaday,
            'orders': orders,
            'count_filtered': count_filtered,
        }
        return render(request, 'food/pizza_day_detail.html', context)


def create_pizza_day(request):
    user = request.user
    if not user.profile.role_set.filter(name='MaintenanceManager').exists():
        return redirect('pizza_day_list')
    form = CreatePizzadayForm()

    if request.method == 'POST':
        form = CreatePizzadayForm(request.POST)
        if form.is_valid():
            to_date = form.cleaned_data['to_date']

            if PizzaDayDay.objects.filter(to_date=to_date).exists():
                messages.error(request, 'Pizza day s tímto datem již existuje.')
                messages.error(request, 'Zvol jiný datum.')
            else:
                form.save()
                messages.success(request,
                                 'Pizzaday byl úspěšně vytvořen a pokud jeho termín je nejblíší aktuálnímu datu z pizzadayjů již vytvořených, byl aktivován jako jediný platný do kterého kterého si lze zaregistrovat doručení pizzy.')
                return redirect('pizza_day_list')

    context = {'form': form}
    return render(request, 'food/create_pizza_day.html', context)

#Alternativní jednodušší způsob smazání záznamu databáze pomocí DeleteView
# class DeletePizzaDay(DeleteView):
#     template_name = 'food/delete_pizza_day.html'
#     model = PizzaDayDay
#     context_object_name = 'pizzaday_delete'
#     success_url = reverse_lazy('pizza_day_list')

class DeletePizzaDay(View, HasRequiredRoleMixin, LoginRequiredMixin):
    template_name = 'food/delete_pizza_day.html'
    model = PizzaDayDay



    def get(self, request, slug):
        pizzaday = PizzaDayDay.objects.get(slug=slug)
        required_roles = ["LunchManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("pizza_day_list")
        context = {
            'pizzaday': pizzaday,
        }

        return render(request, 'food/delete_pizza_day.html', context)

    def post(self, request, slug):
        pizzaday = PizzaDayDay.objects.get(slug=slug)
        if request.method == 'POST':
            pizzaday.delete()

            return redirect('pizza_day_list')

class RegistrationStatusChange(View, HasRequiredRoleMixin, LoginRequiredMixin):
    template_name = 'food/registration_status_change.html'
    model = PizzaDayDay
    login_url = "login"


    def get_context_data(self, **kwargs):
        context = {}
        current_date = timezone.now().date()
        last_pizzaday = PizzaDayDay.objects.filter(to_date__gte=current_date).order_by('to_date').first()
        context['last_pizzaday'] = last_pizzaday

        return context


    def get(self, request):
        required_roles = ["LunchManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("pizza_day_list")
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        current_date = timezone.now().date()
        last_pizzaday = PizzaDayDay.objects.filter(to_date__gte=current_date).order_by('to_date').first()

        if last_pizzaday:
            last_pizzaday.registration_open = not last_pizzaday.registration_open
            last_pizzaday.save()

        return redirect('pizza_day_list')

class LunchWeekList(ListView):
    template_name = 'food/lunch_list.html'
    model = LunchMenuOption
    context_object_name = 'menu_options'
    # form_class = LunchOrderForm

    class LunchMenuListView(ListView):
        model = LunchMenuOption
        template_name = 'lunch_menu_list.html'
        context_object_name = 'menu_options_by_day'



    def get_queryset(self):

        selected_week = self.request.GET.get('week')
        if selected_week:
            # Výpočet počátečního a koncového data pro vybraný týden
            selected_date = timezone.now().date()
            start_of_week = selected_date - timedelta(days=selected_date.weekday()) + timedelta(
                weeks=int(selected_week))
            end_of_week = start_of_week + timedelta(days=4)

            # Získání nabídek pro vybraný týden rozdělených podle dnů
            queryset = LunchMenuOption.objects.filter(menu__date__range=[start_of_week, end_of_week])
            menu_options_by_day = {}
            weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

            for menu_option in queryset:
                day = menu_option.menu.date.strftime('%A')
                if day in menu_options_by_day:
                    menu_options_by_day[day].append(menu_option)
                else:
                    menu_options_by_day[day] = [menu_option]

            sorted_menu_options_by_day_dict = {day: menu_options_by_day[day] for day in weekdays_order if day in menu_options_by_day}

            return sorted_menu_options_by_day_dict

        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_week'] = self.request.GET.get('week')
        context['has_lunchmanager_role'] = self.request.user.profile.role_set.filter(name='LunchManager')
        context['current_user'] = self.request.user
        context['selected_date'] = timezone.now().date()
        # context['form'] = self.form_class()
        print(context)

        return context


class OrderLunch(LoginRequiredMixin, View):
    login_url = "login"
    template_name = 'food/order_lunch.html'
    model = LunchMenuOption
    form_class = LunchOrderForm

    def get(self, request, uuid):
        menu_option = LunchMenuOption.objects.get(id=uuid)
        cena = menu_option.meal.price
        profill = request.user.profile
        print(f"Cena za jídlo je: {menu_option.meal.price}")
        print(f"Dostupných porcí je:{menu_option.available_portions}")
        print(f"Dostupný cash je:{request.user.profile.lunch_account}")
        print(profill)

        initial_data = {'menu_option': menu_option,
                        'user': request.user.profile}
        print(initial_data)
        form = self.form_class(initial=initial_data)
        context = {'menu_option': menu_option, 'form': form}

        return render(request, self.template_name, context)

    def post(self, request, uuid):
        menu_option = LunchMenuOption.objects.get(id=uuid)
        portions = menu_option.available_portions
        profile = request.user.profile
        cena = menu_option.meal.price
        ucet = request.user.profile.lunch_account

        form = self.form_class(request.POST)

        if form.is_valid():
            remain_portions = portions - 1
            rozdil = ucet - cena
            menu_option.available_portions = remain_portions
            menu_option.save()
            profile.lunch_account = rozdil
            profile.save()
            order = form.save(commit=False)
            order.user = request.user.profile
            order.menu_option = menu_option
            # UPDEJTOVAT


            transaction_user_data = str(profile.name + " " + profile.surname)
            transaction_data = str("order: " + menu_option.meal.name)
            transaction = TransactionHistory(
                transaction=transaction_data,
                related_user=transaction_user_data,
                value=int(-cena)
            )

            transaction.save()
            order.save()
            return redirect('lunch_week_list')

        context = {'menu_option': menu_option, 'form': form}
        return render(request, self.template_name, context)

class LunchOrderFilter(django_filters.FilterSet):
    dateFilter = django_filters.DateFilter(field_name='menu_option__menu__date', lookup_expr='exact', label='Date')

    class Meta:
        model = LunchOrder
        fields = []

class OrderOverview(LoginRequiredMixin, View, HasRequiredRoleMixin):
    login_url = "login"
    template_name = 'food/order_overview.html'
    model = LunchOrder
    filterset_class = LunchOrderFilter
    context_object_name = 'orders'

    def get(self, request):
        orders = LunchOrder.objects.all()
        required_roles = ["LunchManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("lunch_week_list")
        order_filter = LunchOrderFilter(request.GET, queryset=orders)
        context = {'orders': order_filter.qs, 'filter': order_filter}
        if 'dateFilter' in request.GET:
            selected_date = datetime.strptime(request.GET['dateFilter'], '%Y-%m-%d')
            formatted_date = selected_date.strftime('%d.%m.%Y')
            context['selected_date'] = formatted_date
        else:
            context['selected_date'] = "No filter selected"
        return render(request, self.template_name, context)

class OrderWeekList(ListView):
    template_name = 'food/my_orders.html'
    model = LunchOrder
    context_object_name = 'my_orders'


    class LunchOrder(ListView):
        model = LunchOrder
        template_name = 'lunch_menu_list.html'
        context_object_name = 'my_order_by_day'



    def get_queryset(self):

        selected_week = self.request.GET.get('week')
        if selected_week:
            # Výpočet počátečního a koncového data pro vybraný týden
            selected_date = timezone.now().date()
            start_of_week = selected_date - timedelta(days=selected_date.weekday()) + timedelta(
                weeks=int(selected_week))
            end_of_week = start_of_week + timedelta(days=4)


            # Získání nabídek pro vybraný týden rozdělených podle dnů
            queryset = LunchOrder.objects.filter(menu_option__menu__date__range=[start_of_week, end_of_week],
                                                 user=self.request.user.profile)
            menu_options_by_day = {}
            weekdays_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

            for order in queryset:
                day = order.menu_option.menu.date.strftime('%A')  # Získání názvu dne v týdnu
                if day in menu_options_by_day:
                    menu_options_by_day[day].append(order)
                else:
                    menu_options_by_day[day] = [order]

            sorted_menu_options_by_day_dict = {day: menu_options_by_day[day] for day in weekdays_order if day in menu_options_by_day}

            return sorted_menu_options_by_day_dict

        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_week'] = self.request.GET.get('week')
        # context['form'] = self.form_class()

        return context

def lunch_account_overview(request):

    user = request.user
    if not user.profile.role_set.filter(name='LunchManager').exists():
        return redirect('lunch_week_list')

    persons = Profile.objects.all()

    sort_order = request.GET.get('sort_order', 'ascendingBank')
    print(persons)
    if sort_order == 'descendingBank':
        persons = persons.order_by('-lunch_account')
    elif sort_order == 'ascendingBank':
        persons = persons.order_by('lunch_account')
    elif sort_order == 'descendingName':
        persons = persons.annotate(lower_name=Lower('name')).order_by('-lower_name')
    elif sort_order == 'ascendingName':
        persons = persons.annotate(lower_name=Lower('name')).order_by('lower_name')
    elif sort_order == 'descendingSurname':
        persons = persons.annotate(lower_surname=Lower('surname')).order_by('-lower_surname')
    elif sort_order == 'ascendingSurname':
        persons = persons.annotate(lower_surname=Lower('surname')).order_by('lower_surname')
    context = {'persons': persons, 'sort_order': sort_order}

    return render(request, 'food/lunch_account_overview.html', context)

class EditLunchAccount(View, HasRequiredRoleMixin, LoginRequiredMixin):
    template_name = 'food/edit_account.html'
    model = Profile
    form_class = EditLunchAccountForm
    login_url = "login"


    def get(self, request, uuid):
        person = Profile.objects.get(id=uuid)
        form = self.form_class()
        required_roles = ["LunchManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("lunch_week_list")
        context = {'person': person, 'form': form}
        print(person.lunch_account)
        return render(request, self.template_name, context)

    def post(self, request, uuid):
        person = Profile.objects.get(id=uuid)
        person_cash = person.lunch_account
        form = self.form_class()
        if request.method == 'POST':
            value = request.POST['cash']
            value = int(value)
            new_total_cash = value + person_cash
            person.lunch_account = new_total_cash
            #UPDEJTOVAT
            profile = Profile.objects.get(id=uuid)
            transaction_value = value
            transaction_user_data = str(profile.name + " " + profile.surname)
            transaction_data = "account change:"
            transaction = TransactionHistory(
                transaction=transaction_data,
                related_user=transaction_user_data,
                value=int(transaction_value)
            )
            print(transaction_value, transaction_user_data, transaction_data, transaction)
            transaction.save()
            person.save()
            messages.success(request, f"Na účtu {person.name} {person.surname} jste provedli změnu {value}kč.")
            return redirect('lunch_account_overview')

        context = {'person': person, 'form': form}
        return render(request, self.template_name, context)

class CreateMeal(View, HasRequiredRoleMixin, LoginRequiredMixin):
    template_name = 'food/create_meal.html'
    model = LunchMeal
    form_class = CreateMealForm
    login_url = "login"

    def get(self, request):
        form = self.form_class()
        required_roles = ["LunchManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("lunch_week_list")
        context = {'form': form}

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            meal = form.save(commit=False)
            meal.save()
            return redirect('lunch_week_list')
        context = {'form': form}
        return render(request, self.template_name, context)

class CreateMenu(View, HasRequiredRoleMixin, LoginRequiredMixin):
    template_name = 'food/create_menu.html'
    model = LunchMenu
    form_class = CreateMenuForm
    login_url = "login"

    def get(self, request):
        form = self.form_class()
        required_roles = ["LunchManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("lunch_week_list")
        context = {'form': form}

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            #UPDEJTOVAT
            date = form.cleaned_data['date']
            if LunchMenu.objects.filter(date=date).exists():
                messages.success(request, "Menu pro tento den je již vytvořeno.")
                context = {
                    'form': form
                }
                return render(request, self.template_name, context)

            menu = form.save(commit=False)
            menu.save()
            return redirect('lunch_week_list')
        context = {'form': form}
        return render(request, self.template_name, context)

class CreateLunchMenuOption(View, HasRequiredRoleMixin, LoginRequiredMixin):
    template_name = 'food/create_menu.html'
    model = LunchMenu
    form_class = CreateLunchMenuOptionForm
    login_url = "login"

    def get(self, request):
        form = self.form_class()
        required_roles = ["LunchManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("lunch_week_list")
        context = {'form': form}

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            menu_option = form.save(commit=False)
            menu_option.save()
            return redirect('lunch_week_list')
        context = {'form': form}
        return render(request, self.template_name, context)

#UPDEJTOVAT

class LunchMealListView(ListView, HasRequiredRoleMixin, LoginRequiredMixin):
    model = LunchMeal
    template_name = 'food/meal_list.html'
    context_object_name = 'meals'
    login_url = 'login'


    def get(self, request, *args, **kwargs):

        meals = LunchMeal.objects.all()
        required_roles = ["LunchManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("lunch_week_list")
        context = {'meals': meals}

        return render(request, self.template_name, context)

class LunchMealDeleteView(DeleteView):
    model = LunchMeal
    success_url = reverse_lazy("lunch_week_list")

class LunchMenuOptionDeleteView(DeleteView):
    model = LunchMenuOption
    success_url = reverse_lazy("lunch_week_list")

class EditAvailablePortions(View):
    template_name = 'food/edit_available_portions.html'
    model = LunchMenuOption
    form_class = EditLunchAccountForm

    def get(self, request, uuid):
        menu_option = LunchMenuOption.objects.get(id=uuid)
        form = self.form_class
        context = {"menu_option": menu_option, "form": form}
        return render(request, self.template_name, context)

    def post(self, request, uuid):
        menu_option = LunchMenuOption.objects.get(id=uuid)
        available_portions = menu_option.available_portions

        form = self.form_class

        if request.method == 'POST':
            value = request.POST['portions']
            value = int(value)
            new_total_portions = value + available_portions
            menu_option.available_portions = new_total_portions
            menu_option.save()
            messages.success(request, f"V menu {menu_option.meal.name} {menu_option.menu.date} jste provedli změnu {value} porcí.")
            return redirect('lunch_week_list')

class TransactionFilter(django_filters.FilterSet):
    dateFilter = django_filters.DateFilter(field_name='created_at__date', lookup_expr='exact', label='Date')

    class Meta:
        model = TransactionHistory
        fields = []

class Transactions(LoginRequiredMixin, View, HasRequiredRoleMixin):
    login_url = "login"
    template_name = 'food/transactions.html'
    model = TransactionHistory
    filterset_class = TransactionFilter
    context_object_name = 'transactions'

    def get(self, request):
        transactions = TransactionHistory.objects.all().order_by('-created_at')
        order_filter = TransactionFilter(request.GET, queryset=transactions)
        required_roles = ["LunchManager"]
        if not self.has_required_role(request.user, required_roles):
            return redirect("lunch_week_list")
        context = {'transactions': order_filter.qs, 'filter': order_filter}
        if 'dateFilter' in request.GET:
            selected_date = datetime.strptime(request.GET['dateFilter'], '%Y-%m-%d')
            formatted_date = selected_date.strftime('%d.%m.%Y')
            context['selected_date'] = formatted_date
        else:
            context['selected_date'] = "No filter selected"
        return render(request, self.template_name, context)