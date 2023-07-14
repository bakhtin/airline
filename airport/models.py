# -*- coding: utf-8 -*-
from django.db import models
from city.models import City


class Airport(models.Model):
    code = models.CharField(max_length=3, verbose_name='Код', unique=True)
    city = models.ForeignKey(City, default='', on_delete=models.CASCADE)

    def __str__(self):
        return '{}, {}'.format(self.code, self.city)