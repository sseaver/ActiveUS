from django import forms
from app.models import Star_Rating


class RatingForm(forms.ModelForm):
    model = Star_Rating
    fields = ('rating',)
