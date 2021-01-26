from django import forms
from django.db.models import fields
from django.db.models.fields import files
from django.db.models.query import QuerySet
from django.forms import widgets
from .models import Recipies, RecipeTypes
from ingredients.models import Ingredients


class NewRecipeForm(forms.ModelForm):
  class Meta:
    model = Recipies
    
    fields = (
      'name',
      'description',
      'recipe_type',
      'tags',
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


class EditRecipeNameForm(forms.ModelForm):
  class Meta:
    model = Recipies

    fields = (
      'name',
      'description',
    )
    labels = {
      'name': '',
      'description': '',
    }
    widgets = {
      'name': forms.TextInput(attrs={'placeholder': 'Overskrift..', 'size': 30}),
      'description': forms.Textarea(
          attrs={'cols':30, 'rows': 3, 'placeholder': 'Beskrivelse..'}),
    }


class RecipeTypeFilterBox(forms.ModelForm):
  class Meta:
    model = Recipies

    fields = (
    'recipe_type',
    'tags',
    )
    
    labels = {
      'recipe_type': '',
      'tags': '',
    }

    widgets = {
      'recipe_type': forms.Select(attrs={'onchange': 'filterbox.submit();'}),
      'tags': forms.Select(attrs={'onchange': 'filterbox.submit();'}),
    }


class RecipeTagsForm(forms.ModelForm):
  class Meta:
    model = Recipies

    fields = (
      'tags',
      'prep_time'
    )
    labels = {
      'tags': '',
      'prep_time': ''
    }
    widgets = {
      'prep_time': forms.TextInput(attrs={'size': 6}),
    }