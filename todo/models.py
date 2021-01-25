from django.db import models
from django.db.models.fields import CharField, IntegerField
from foodplan.models import Foodplans
from ingredients.models import IngredientCategory


class Shoppinglist(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  list_source = CharField(max_length=50, blank=False, default=None)
  source_id = IntegerField(blank=True, null=True)
  completed = models.BooleanField(default=False)


class Task(models.Model):
  title = models.CharField(max_length=200)
  ingredient_category = models.ForeignKey(IngredientCategory, on_delete=models.DO_NOTHING, blank=True, null=True, default=1)
  complete = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)
  shoppinglist = models.ForeignKey(Shoppinglist, on_delete=models.CASCADE, blank=True, null=True)

  def __str__(self):
    return self.title
  
  def get_foodplan_id(self):
    return self.foodplan.foodplan_id
  