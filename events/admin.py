from django.contrib import admin

# Register your models here.

from .models import Event, Category, RSVP


admin.site.register(Event)
admin.site.register(Category)
admin.site.register(RSVP)
