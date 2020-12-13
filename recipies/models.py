from django.db import models
from datetime import datetime
from django.utils import timezone
from ingredients.models import Ingredients


class RecipeTypes(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name


class Recipies(models.Model):
  date = models.DateTimeField(default=timezone.now)
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=300)
  recipe_type = models.ForeignKey(RecipeTypes, on_delete=models.DO_NOTHING, blank=True)

  def __str__(self):
    return self.name
  
  def get_type(self):
    return self.recipe_type.name


class MeasurementUnits(models.Model):
  unit_name = models.CharField(max_length=50)


class RecipeIngredients(models.Model):
  recipe = models.ForeignKey(Recipies, on_delete=models.CASCADE)
  ingredient = models.ForeignKey(Ingredients, on_delete=models.DO_NOTHING)
  measurement_unit = models.ForeignKey(MeasurementUnits, on_delete=models.DO_NOTHING, blank=False, default=1)
  amount = models.FloatField(default=1, blank=False)

  def get_ingredient_name(self):
    return self.ingredient.name
  
  def get_ingredient_description(self):
    return self.ingredient.description
  
  def get_unit_name(self):
    return self.measurement_unit.unit_name


class RecipeInstructions(models.Model):
  recipe = models.ForeignKey(Recipies, on_delete=models.CASCADE)
  step = models.IntegerField(default=1, blank=False)
  description = models.CharField(max_length=2000)


