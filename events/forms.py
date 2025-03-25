# forms.py
from django import forms
from .models import Event, Category, RSVP
from django.core.exceptions import ValidationError
from django.utils import timezone
from cloudinary.forms import CloudinaryFileField

class EventForm(forms.ModelForm):
    image = CloudinaryFileField()
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'value': timezone.now().date(), 'placeholder': 'YYYY-MM-DD'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'value': timezone.now().strftime('%H:%M'), 'placeholder': 'HH:MM'}),
            'name': forms.TextInput(attrs={'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Event Description .....'}),
            'image': forms.FileInput(attrs={'type': 'file', 'accept': 'image/*', 'class': 'form-control', 'style': 'border: 1px solid #ced4da; padding: 10px; border-radius: 0.25rem;'}),
        }
        labels = {
            'date': 'Event Date',
            'time': 'Event Time',
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

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['response']  # Only the response field is needed for the form
        widgets = {
            'response': forms.CheckboxInput(attrs={
                'required': True,
                'class': 'checkbox-helper'
            }),
        }
        labels = {
            'response': 'Will you attend?',
        }
        help_texts = {
            'response': 'Tick the box if you plan to attend the event.',
        }

    def __init__(self, *args, **kwargs):
        super(RSVPForm, self).__init__(*args, **kwargs)
        self.fields['response'].required = True
