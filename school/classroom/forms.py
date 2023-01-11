from django import forms 
from .models import Classroom, Student


class StudentForm(forms.Form):

    name = forms.CharField(max_length=200, label='Tu nombre', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(max_length=200, label='Tu apellido', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    idClassroom = forms.ModelChoiceField(queryset=Classroom.objects.all(), empty_label=None, label='Aula', widget=forms.Select(attrs={
        'class': 'form-select'
    }))

    # class Meta:
    #     model = Student
    #     fields = ['name', 'last_name', 'idClassroom']
    #     labels = {
    #         'name': 'Nombres',
    #         'last_name': 'Apellidos',
    #         'idClassroom': 'Aula'
    #     }
    #     widgets = {
    #         'idClassroom': forms.Select(attrs={
    #             'class': 'form-select'
    #         }),
    #     }