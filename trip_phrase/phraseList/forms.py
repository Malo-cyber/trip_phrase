from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from phraseList.models import Context

CHOICES = Context.choices

class ChooseContextForm(forms.Form):
	context = forms.ChoiceField(choices=CHOICES)
	

