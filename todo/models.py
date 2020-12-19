from django.db import models
from foodplan.models import Foodplans

class Task(models.Model):
  title = models.CharField(max_length=200)
  ingredient_category = models.IntegerField(blank=True, default=0)
  complete = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)
  foodplan = models.IntegerField(blank=False, default=1)

  def __str__(self):
    return self.title
  
  def get_foodplan_id(self):
    return self.foodplan.foodplan_id
  