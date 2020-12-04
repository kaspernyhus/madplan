from django.db import models



class RecipeTypes(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name


class Recipies(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=300)
  recipe_type = models.ForeignKey(RecipeTypes, on_delete=models.DO_NOTHING, blank=True)

  def __str__(self):
    return self.name
  
  def get_type(self):
    return self.recipe_type.name


class Ingredients(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=300)
  price = models.FloatField(blank=True)

  def __str__(self):
    return self.name


class MeasurementUnits(models.Model):
  unit_name = models.CharField(max_length=50)


class RecipeIngredients(models.Model):
  recipe = models.ForeignKey(Recipies, on_delete=models.CASCADE)
  ingredient = models.ForeignKey(Ingredients, on_delete=models.DO_NOTHING)
  measurement_unit = models.ForeignKey(MeasurementUnits, on_delete=models.DO_NOTHING, blank=False, default=1)
  amount = models.FloatField(default=1, blank=False)


class RecipeInstructions(models.Model):
  recipe = models.ForeignKey(Recipies, on_delete=models.CASCADE)
  step = models.IntegerField(default=1, blank=False)
  description = models.CharField(max_length=2000)


