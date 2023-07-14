# -*- coding: utf-8 -*-
from django.db import models


class Country(models.Model):
    country = models.CharField(max_length=255, verbose_name='Country')

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return '{}'.format(self.country)