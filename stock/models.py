from django.db import models


class Freezerstock(models.Model):
  freeze_date = models.DateTimeField(auto_now_add=True)
  type = models.CharField(max_length=20, blank=False, default='ingrediens')
  name = models.CharField(max_length=50, blank=False, default=None)
  qty = models.IntegerField(blank=False)
  best_before = models.DateTimeField(blank=True, null=True)