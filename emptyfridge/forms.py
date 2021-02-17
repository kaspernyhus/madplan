from django import forms
from django.forms import fields
from ingredients.models import Ingredients

class IngredientForm(forms.ModelForm):
  class Meta:
    model = Ingredients

    fields = (
      'name',
    )