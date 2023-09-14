from django.forms import ModelForm
from django import forms


from django.contrib.auth.models import User
from .models import PizzaDayDay, PizzaOrder, LunchOrder, LunchMenu, LunchMeal, LunchMenuOption, Profile

class PizzaOrderForm(ModelForm):
    selection = forms.ChoiceField(
        choices=[('', 'All')] + PizzaOrder.PIZZA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    to_time = forms.ChoiceField(
        choices=PizzaOrder.TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = PizzaOrder
        fields = '__all__'
        widgets = {
            # 'ordered_by': forms.Select(attrs={'class': 'form-control'}),
            # 'to_time': forms.Select(attrs={'class': 'form-control'}),
            # 'selection': forms.Select(attrs={'class': 'form-control'}),
            'pizza_day': forms.HiddenInput(),
            'ordered_by': forms.HiddenInput()
        }


    def __init__(self, *args, **kwargs):
        super(PizzaOrderForm, self).__init__(*args, **kwargs)
        self.fields['selection'].widget.attrs.update({'class': 'form-control', 'name': 'selection'})
        self.fields['to_time'].widget.attrs.update({'class': 'form-control', 'name': 'to_time'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })

class CreatePizzadayForm(ModelForm):
    class Meta:
        model = PizzaDayDay
        fields = '__all__'
        widgets = {
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(CreatePizzadayForm, self).__init__(*args, **kwargs)
        self.fields['to_date'].widget.attrs.update({'class': 'form-control', 'name': 'selection'})


        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })


class LunchOrderForm(forms.ModelForm):
    class Meta:
        model = LunchOrder
        fields = ['user', 'menu_option', 'note']
        widgets = {
            'user': forms.HiddenInput(),
            'menu_option': forms.HiddenInput(),
            'note': forms.HiddenInput()
        }

    # menu_option = forms.ModelChoiceField(queryset=LunchMenuOption.objects.all(), empty_label=None, label='Menu Option')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_option'].queryset = LunchMenuOption.objects.all()

class EditLunchAccountForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['lunch_account']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lunch_account'].queryset = Profile.objects.all()

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })


class CreateMealForm(forms.ModelForm):
    class Meta:
        model = LunchMeal
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })


class CreateMenuForm(forms.ModelForm):
    class Meta:
        model = LunchMenu
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })

class CreateLunchMenuOptionForm(forms.ModelForm):
    class Meta:
        model = LunchMenuOption
        fields = "__all__"
        # widgets = {
        #     'date': forms.DateInput(attrs={'type': 'date'}),
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })
            #UPDEJTOVAT
        self.fields['menu'].queryset = LunchMenu.objects.all().order_by('-date')

#UPDEJTOVAT
class EditAvailablePortionsForm:
    class Meta:
        model = LunchMenuOption
        fields = ['available_portions']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['available_portions'].queryset = Profile.objects.all()

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })