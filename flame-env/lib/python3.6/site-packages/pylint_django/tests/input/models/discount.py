from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    operator = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.NullBooleanField()
