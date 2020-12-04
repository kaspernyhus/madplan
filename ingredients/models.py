from django.db import models

class Ingredients(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=300)
  best_before = models.IntegerField(blank=True, null=True)
  price = models.FloatField(blank=True)

  def __str__(self):
    return self.name
