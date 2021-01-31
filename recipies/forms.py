from django import forms
from django.db import models
from django.db.models import fields
from django.db.models.fields import files
from django.db.models.query import QuerySet
from django.forms import widgets
from .models import Addons, Recipies, RecipeTypes
from ingredients.models import Ingredients
from django.db.models import Q


class NewRecipeForm(forms.ModelForm):
  class Meta:
    model = Recipies
    
    fields = (
      'name',
      'description',
      'recipe_type',
      'tags',
      'URL',
      'photo_thumbnail',
    )
    labels = {
      'name': '',
      'description': '',
      'recipe_type': 'Type',
      'URL': 'Website',
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
      'prep_time',
    )
    labels = {
      'name': '',
      'description': '',
      'prep_time': '',
    }
    widgets = {
      'name': forms.TextInput(attrs={'placeholder': 'Overskrift..', 'size': 30}),
      'description': forms.Textarea(
          attrs={'cols':30, 'rows': 3, 'placeholder': 'Beskrivelse..'}),
      'prep_time': forms.TextInput(attrs={'placeholder': '0:00', 'size': 6}),
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
      'URL',
      'add_ons',
    )
    labels = {
      'tags': '',
      'URL': 'Website',
      'add_ons': 'Tillad andet tilbehør',
    }
  

class AddAddonsForm(forms.Form):
  add_on = forms.ModelChoiceField(queryset=Recipies.objects.filter(Q(recipe_type_id=2)|Q(recipe_type_id=5)), label='')
  