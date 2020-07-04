#--- IOT_Server - api app models ----------------------------------------------
#--- Original Release: December 2018
#--- By: Conrad Eggan
#--- Email: Conrade@RedCatMfg.com

from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
from django.utils import timezone

class Devices(models.Model):
    device_id = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

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
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ValueType'
        verbose_name_plural = 'ValueTypes'


class Tags(models.Model):
    tag_id = models.CharField(max_length=25, primary_key=True, validators=[MinLengthValidator(3)])
    device = models.ForeignKey(Devices, related_name='device_tags', on_delete=models.PROTECT)
    value_type = models.ForeignKey(ValueTypes, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.device.owner

    #for Tags page in Admin module
    def device_concat(self):
        return self.device.device_id + ' / ' + self.device.name
    device_concat.short_description = 'Belongs to Device'

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['device', 'tag_id']


class IotData(models.Model):
    tag = models.ForeignKey(Tags, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(default=timezone.now)
    value_int = models.IntegerField(blank=True, null = True)
    value_dec = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null = True)
    value_text = models.CharField(max_length=100, blank=True, null = True)
    value_bool = models.BooleanField(blank=True, null = True)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def value(self):
        tag_type = self.tag.value_type.type
        if tag_type == 'bool':
            return self.value_bool
        elif tag_type == 'int':
            return self.value_int
        elif tag_type == 'dec':
            return self.value_dec
        elif tag_type == 'string':
            return self.value_text
        else:
            return 'Unknown value type for tag.'

    @property
    def owner(self):
        return self.tag.device.owner


class WeatherStations(models.Model):
    identifier = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null = True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null = True)
    type = models.CharField(max_length=50, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identifier + " - " + self.name

    class Meta:
        verbose_name = 'WeatherStation'
        verbose_name_plural = 'WeatherStations'


class WeatherData(models.Model):
    station = models.ForeignKey(WeatherStations, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null = True)
    dewpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null = True)
    temp_uom = models.CharField(max_length=10, blank=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null = True)
    wind_gust = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null = True)
    wind_uom = models.CharField(max_length=10, blank=True)
    wind_dir = models.IntegerField(blank=True, null = True)
    dir_uom = models.CharField(max_length=10, blank=True)
    pressure = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null = True)
    press_uom = models.CharField(max_length=10, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def owner(self):
        return self.station.owner

    @property
    def identifier(self):
        return self.station.identifier
