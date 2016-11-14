from django import forms
from app.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'date', 'time', 'location', 'participants')
