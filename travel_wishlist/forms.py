from django import forms
from .models import Place


class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')  # only fields the user should be editing go here (ex. not PK)


class DateInput(forms.DateInput):
    input_type = 'date'


class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = {'notes', 'date_visited', 'photo'}
        widgets = {
            'date_visited': DateInput()
        }
