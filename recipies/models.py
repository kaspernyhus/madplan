from django.db import models
from datetime import datetime
from django.utils import timezone
from ingredients.models import Ingredients


class RecipeTypes(models.Model):
  class Meta:
    verbose_name = 'Recipe type'
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name


class RecipeTags(models.Model):
  class Meta:
    verbose_name = 'Recipe tag'
  tag = models.CharField(max_length=50)

  def __str__(self):
    return self.tag


class Recipies(models.Model):
  class Meta:
    verbose_name = 'Recipe'
    verbose_name_plural = 'Recipies'
  date = models.DateTimeField(default=timezone.now)
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=300, blank=True)
  recipe_type = models.ForeignKey(RecipeTypes, on_delete=models.DO_NOTHING, blank=True)
  photo_thumbnail = models.ImageField(upload_to='photos/thumbnails/', blank=True)
  tags = models.ManyToManyField(RecipeTags)
  prep_time = models.CharField(max_length=6, blank=True, null=True)
  URL = models.URLField(max_length=200, blank=True, null=True)
  add_ons = models.BooleanField(blank=False, null=False, default=0)
  preferred_add_ons = models.ManyToManyField('self', blank=True)

  def __str__(self):
    return self.name
  
  def get_type(self):
    return self.recipe_type.name


class MeasurementUnits(models.Model):
  class Meta:
    verbose_name = 'Recipe measurement unit'
  unit_name = models.CharField(max_length=50)

  def __str__(self):
    return self.unit_name


class RecipeIngredients(models.Model):
  class Meta:
    verbose_name = 'Recipe Ingredient'
  recipe = models.ForeignKey(Recipies, on_delete=models.CASCADE)
  ingredient = models.ForeignKey(Ingredients, on_delete=models.DO_NOTHING)
  description = models.CharField(max_length=300, blank=True, null=True)
  measurement_unit = models.ForeignKey(MeasurementUnits, on_delete=models.DO_NOTHING, blank=False, default=1)
  amount = models.FloatField(default=1, blank=False)

  def get_ingredient_name(self):
    return self.ingredient.name
  
  def get_ingredient_description(self):
    return self.ingredient.description

  def get_ingredient_category(self):
    return self.ingredient.category
  
  def get_unit_name(self):
    return self.measurement_unit.unit_name


class RecipeIngredientsHeading(models.Model):
  class Meta:
    verbose_name = 'Recipe Ingredient Heading'
  recipe = models.ForeignKey(Recipies, on_delete=models.CASCADE)
  heading = models.CharField(max_length=300, blank=True, null=True)
  place = models.IntegerField(default=1)


class RecipeInstructions(models.Model):
  class Meta:
    verbose_name = 'Recipe instruction'
  recipe = models.ForeignKey(Recipies, on_delete=models.CASCADE)
  step = models.IntegerField(default=1, blank=False)
  description = models.CharField(max_length=2000)
  is_bold = models.BooleanField(default=False)


class AddOns(models.Model):
  class Meta:
    verbose_name = 'Recipe Add-ons'
  recipe = models.ForeignKey(Recipies, on_delete=models.CASCADE, related_name="recipe")
  add_on = models.ForeignKey(Recipies, on_delete=models.CASCADE, related_name="add_on")
  active = models.BooleanField(default=1)
  qty_multiplier = models.FloatField(blank=False, default=1.0)