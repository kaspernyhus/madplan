from django.db import models


class IngredientCategory(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name


class Ingredients(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=300, blank=True, null=True)
  category = models.ForeignKey(IngredientCategory, on_delete=models.DO_NOTHING, blank=True, null=True)
  best_before = models.IntegerField(blank=True, null=True)
  price = models.FloatField(blank=True, null=True)

  def __str__(self):
    return self.name
  
  def get_type(self):
    return self.category.name

