from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
# from .models import Homework, GroupStudy

class NoteForms(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','description','due','document','is_finished',]

class DashboardForm(forms.Form):
    text = forms.CharField(max_length= 100, label = "enter your search:")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = {'title','is_finished'}

class ConversionForm(forms.Form):
    CHOICES = [('length','length'),('mass','mass')]
    measurement = forms.ChoiceField(choices = CHOICES,widget = forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES = [('yard','yard'),('foot','foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(attrs = {'type':'number','placeholder':'Enter the number'}))
    measure1 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )


class ConversionMassForm(forms.Form):
    CHOICES = [('pound','pound'),('kilogram','kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(attrs = {'type':'number','placeholder':'Enter the number'}))
    measure1 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='',widget=forms.Select(choices=CHOICES)
    )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class GroupForm(forms.ModelForm):
    class Meta:
        model = GroupStudy
        fields = ['name','description']

class AddMemberForm(forms.Form):
    username = forms.CharField(max_length=150)
    
# ebooks

class EbooksForm(forms.ModelForm):
    class Meta:
        model = Ebooks
        fields = ['subject','description','document',]




class GroupHomeworkForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=GroupStudy.objects.none(),
        required=False,
        help_text="Assign homework to a group (only for admins)."
    )

    class Meta:
        model = GroupHomework
        widgets = {'due':DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'document', 'group']


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['group'].queryset = GroupStudy.objects.filter(created_by=user)
