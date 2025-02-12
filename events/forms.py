# forms.py
from django import forms
from .models import Event, Participant, Category
from django.core.exceptions import ValidationError
from django.utils import timezone

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'value': timezone.now().date(), 'placeholder': 'YYYY-MM-DD'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'value': timezone.now().strftime('%H:%M'), 'placeholder': 'HH:MM'}),
            'name':forms.TextInput(attrs={'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Event Description .....'}),
        }
        labels = {
            'date': 'Event Date',
            'time': 'Event Time',
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise ValidationError("Event date cannot be in the past")
        return date

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'events': forms.CheckboxSelectMultiple(attrs={"type": 'multiple'}),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'events': 'Events',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = { 
            'name': forms.TextInput(attrs={'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Category Description .....'}),
        }
        labels = {
            'name': 'Category Name',
        }


