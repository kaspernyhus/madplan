from django import forms
from .models import RecipeIngredients


class AddIngredientsForm(forms.ModelForm):
  
  measurement_unit = forms.CharField(label='')

  class Meta:
    model = RecipeIngredients
    fields = [
      'ingredient',
      'amount',
    ]
    labels = {
            'ingredient': '',
            'amount': '',
        }