from django import forms
from django.forms import fields
from .models import Freezerstock


class FreezerstockForm(forms.ModelForm):
  class Meta:
    model = Freezerstock

    fields = (
      'type',
      'name',
      'qty',
      'best_before'
    )

