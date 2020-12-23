from django.db import models
from recipies.models import Recipies
from datetime import datetime
from django.utils import timezone


class FoodplanStatus(models.Model):
  foodplan_id = models.IntegerField(primary_key=True)
  complete = models.BooleanField(blank=False, default=False)


class Foodplans(models.Model):
  class Meta:
    verbose_name = 'Foodplan'
  date = models.DateTimeField(default=timezone.now)
  foodplan_id = models.IntegerField(blank=False, default=1)
  recipe = models.ForeignKey(Recipies, on_delete=models.DO_NOTHING, blank=True, null=True)
  quantity = models.IntegerField(blank=False, default=1)
  
  def get_recipe_name(self):
    return self.recipe.name