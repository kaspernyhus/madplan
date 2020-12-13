from django import forms
from .models import Ingredients, IngredientCategory


class NewIngredientForm(forms.ModelForm):
  class Meta:
    model = Ingredients
    fields = [
      'name',
      'description',
      'category',
      'best_before',
      'price'
    ]