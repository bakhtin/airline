# -*- coding: utf-8 -*-
import datetime
from django.db import models
from unique_flight.models import UniqueFlight


class Order(models.Model):
    registration_time = models.DateTimeField(verbose_name='Flight registration time', default='1990-01-01 00:00')
    is_registered = models.BooleanField(verbose_name='Is registered', default=False)
    first_name = models.CharField(max_length=255, verbose_name='First name', default='')
    last_name = models.CharField(max_length=255, verbose_name='Last name', default='')
    document_id = models.CharField(max_length=11, verbose_name='Document ID', default='')
    birth_day = models.DateField(verbose_name='Date of birth', default='1990-01-01')
    email = models.EmailField(max_length=255, verbose_name='Email', default='')
    unique_flight = models.ForeignKey(UniqueFlight, verbose_name='Unique flight', default='', on_delete=models.CASCADE)
    order_hash = models.CharField(max_length=256, verbose_name='Hash', default='')
    booking_id = models.CharField(max_length=7, verbose_name='Booking ID', default='')
    class_of_service = models.CharField(max_length=1, verbose_name='Class of service', default='E')
    taken_seat = models.CharField(max_length=4, default='')

    def try_take_seat(self, seat):
        free_seats = Order.get_free_seats(self.unique_flight.id, self.unique_flight.flight.aircraft,
                                          self.class_of_service)
        if seat not in free_seats:
            return False
        self.taken_seat = seat
        self.is_registered = True
        self.registration_time = datetime.datetime.now()
        self.save()
        return True

    @staticmethod
    def get_taken_seats(unique_flight_id):
        orders = Order.objects.all().filter(unique_flight_id=unique_flight_id)
        return [order.taken_seat for order in orders if order.taken_seat != '']

    @staticmethod
    def get_free_seats(unique_flight_id, aircraft, class_of_service):
        taken_seats = Order.get_taken_seats(unique_flight_id)
        seats = aircraft.seat_map_generator()[class_of_service]
        return [x for x in seats if x not in taken_seats]