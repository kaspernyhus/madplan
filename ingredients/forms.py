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
  
  def save(self, commit=True):
      instance = super(NewIngredientForm, self).save(commit=False)
      instance.name = self.cleaned_data['name'].lower()
      if commit:
          instance.save()
      return instance