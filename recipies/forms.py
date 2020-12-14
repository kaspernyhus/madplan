from django import forms
from django.db.models import fields
from .models import Recipies


class NewRecipeForm(forms.ModelForm):
  class Meta:
    model = Recipies
    
    fields = (
      'name',
      'description',
      'recipe_type',
      'photo_thumbnail',
    )
    labels = {
      'name': '',
      'description': '',
      'recipe_type': 'Type',
      'photo_thumbnail': '',
    }
    widgets = {
      'name': forms.TextInput(attrs={'placeholder': 'Overskrift..', 'size': 30}),
      'description': forms.Textarea(
          attrs={'cols':30, 'rows': 3, 'placeholder': 'Beskrivelse..'}),
    }