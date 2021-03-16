from django.db import models
from recipies.models import Recipies
from datetime import datetime
from django.utils import timezone


class Foodplans(models.Model):
  class Meta:
    verbose_name = 'Foodplan'
  date = models.DateTimeField(default=timezone.now)
  complete = models.BooleanField(blank=False, default=False)
  

class FoodplanRecipies(models.Model):
  foodplan = models.ForeignKey(Foodplans, on_delete=models.CASCADE, default=1)
  recipe = models.ForeignKey(Recipies, on_delete=models.DO_NOTHING, blank=True, null=True)
  quantity = models.FloatField(blank=False, default=1.0)
  
  def __str__(self):
    return self.recipe.name