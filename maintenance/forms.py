from django.forms import ModelForm
from django import forms
from .models import Accident, MaintenanceTask, User, Profile, Role, Workcenter
from.models import Accident as AccidentModel
from django.forms import inlineformset_factory

AdditionalImage = AccidentModel.AdditionalImage
AdditionalImageFormSet = inlineformset_factory(Accident, AdditionalImage, fields=('image',), extra=3, can_delete=False)
# class AccidentListForm(modelForm):
#     class Meta:
#         model: Accident

class CreateAccidentForm(forms.ModelForm):
    class Meta:
        model = Accident
        fields = ['workcenter', 'short_text', 'long_text', 'progress', 'priority', 'due_date', 'accident_image']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateAccidentForm, self).__init__(*args, **kwargs)
        self.additional_images_formset = AdditionalImageFormSet(*args, instance=self.instance,
                                                                prefix='additional_images')
        self.fields['due_date'].widget.attrs.update({'class': 'form-control', 'name': 'selection'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTask
        fields = ['short_text', 'owner', 'due_date', 'progress']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })

class EditTaskProgressForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTask
        fields = ['progress']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditTaskProgressForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })

class CreateWorkcenterForm(forms.ModelForm):
    class Meta:
        model = Workcenter
        fields = ['name']
        # widgets = {
        #     'due_date': forms.DateInput(attrs={'type': 'date'}),
        # }

    def __init__(self, *args, **kwargs):
        super(CreateWorkcenterForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', })