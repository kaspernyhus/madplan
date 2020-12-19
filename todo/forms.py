from django import forms
from .models import *

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = (
      'title',
    )
    labels = {
      'title': '',
    }
    widgets = {
      'title': forms.TextInput(attrs={'placeholder': 'Tilføj til listen...', 'size': 30}),
    }