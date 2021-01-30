from django import forms
from django.db.models import fields
from .models import *

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = (
      'title',
      'ingredient_category'
    )
    labels = {
      'title': '',
      'ingredient_category': '',
    }
    widgets = {
      'title': forms.TextInput(attrs={'placeholder': 'Tilføj til listen...', 'size': 20}),
      'ingredient_category': forms.Select(attrs={'style': 'width:100px'})
    }


class ChangeNameForm(forms.ModelForm):
  class Meta:
    model = Shoppinglist
    fields = (
      'name',
    )
    labels = {
      'name': ''
    }