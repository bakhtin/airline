# -*- coding: utf-8 -*-
from django.db import models

from aircraft.models import Aircraft
from airport.models import Airport


class Flight(models.Model):
    FIRST_CLASS = 'F'
    BUSINESS_CLASS = 'B'
    ECONOMY_CLASS = 'E'
    CLASS_OF_SERVICE = (
        (FIRST_CLASS, 'First'),
        (BUSINESS_CLASS, 'Business'),
        (ECONOMY_CLASS, 'Economy'),
    )
    flight_number = models.CharField(max_length=8, verbose_name='Flight Number')
    departure_airport = models.ForeignKey(Airport, verbose_name='Departure airport', default='',
                                          related_name='departure_airport', on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey(Airport, verbose_name='Arrival airport', default='',
                                        related_name='arrival_airport', on_delete=models.CASCADE)
    departure_date_begin = models.DateField(verbose_name='Departure date begin', default='1990-01-01')
    arrival_date_begin = models.DateField(verbose_name='Arrival date begin', default='1990-01-01')
    repeat_interval = models.IntegerField(verbose_name='Repeat interval', default=1)
    departure_time = models.TimeField(verbose_name='Departure time', default="08:00")
    arrival_time = models.TimeField(verbose_name='Arrival time', default="10:00")
    aircraft = models.ForeignKey(Aircraft, verbose_name='Aircraft', default='', related_name='aircraft', on_delete=models.CASCADE)
    price_F = models.FloatField(verbose_name='Price first class', default='22500')
    price_B = models.FloatField(verbose_name='Price business class', default='18200')
    price_E = models.FloatField(verbose_name='Price economy class', default='11400')

    def __str__(self):
        return '{} : {} {} {} -> {} {} {} : repeat = {}: {}'.format(self.flight_number,
                                                                    self.departure_date_begin,
                                                                    self.departure_time,
                                                                    self.departure_airport,
                                                                    self.arrival_airport,
                                                                    self.arrival_date_begin,
                                                                    self.arrival_time,
                                                                    self.repeat_interval,
                                                                    self.aircraft,
                                                                    self.price_F,
                                                                    self.price_B,
                                                                    self.price_E)