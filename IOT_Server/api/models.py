from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone

class Devices(models.Model):
    device_id = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class ValueTypes(models.Model):
    TYPE_CHOICES = (
        ('string', 'Alphanumeric text'),
        ('dec', 'Decimal Number'),
        ('int', 'Integer'),
        ('bool', 'Boolean'),
        )
    value_type_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

class Tags(models.Model):
    tag_id = models.CharField(max_length=25, primary_key=True, validators=[MinLengthValidator(3)])
    device = models.ForeignKey(Devices, on_delete=models.PROTECT)
    value_type = models.ForeignKey(ValueTypes, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class IotData(models.Model):
    tag = models.ForeignKey(Tags, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    value_int = models.IntegerField(blank=True, null = True)
    value_dec = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null = True)
    value_text = models.CharField(max_length=100, blank=True, null = True)
    value_bool = models.BooleanField(blank=True, null = True)
