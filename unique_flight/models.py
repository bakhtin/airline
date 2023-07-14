from django.db import models

from flight.models import Flight


class UniqueFlight(models.Model):
    flight = models.ForeignKey(Flight, verbose_name='Flight', on_delete=models.CASCADE)
    departure_datetime = models.DateTimeField(verbose_name='Departure date and time', default='1990-01-01 00:00')
    left_seats_F = models.IntegerField(verbose_name='Left seats of first class', default=0)
    left_seats_B = models.IntegerField(verbose_name='Left seats of business class', default=0)
    left_seats_E = models.IntegerField(verbose_name='Left seats of economy class', default=0)
    taken_seats_list = models.CharField(verbose_name='List of taken seats', default='', max_length=2000)
    arrival_date = models.DateField(verbose_name='Arrival date', default='1990-01-01')
    arrival_time = models.TimeField(verbose_name='Arrival time', default='00:00')
    flight_time = ''

    def get_price(self, class_of_service):
        if class_of_service == Flight.ECONOMY_CLASS:
            return self.flight.price_E
        elif class_of_service == Flight.BUSINESS_CLASS:
            return self.flight.price_B
        else:
            return self.flight.price_F

    def try_take_seat(self, class_of_service):
        if class_of_service == Flight.ECONOMY_CLASS and self.left_seats_E > 0:
            self.left_seats_E -= 1
            self.save()
            return True
        elif class_of_service == Flight.BUSINESS_CLASS and self.left_seats_B > 0:
            self.left_seats_B -= 1
            self.save()
            return True
        elif class_of_service == Flight.FIRST_CLASS and self.left_seats_F > 0:
            self.left_seats_F -= 1
            self.save()
            return True
        else:
            return False

    def get_flight_time(self):
        day_diff = self.flight.arrival_date_begin - self.flight.departure_date_begin
        flight_time = ''
        if day_diff.days > 1:
            flight_time = (1440 - (self.flight.departure_time.hour * 60 + self.flight.departure_time.minute)) \
                          + self.flight.arrival_time.hour * 60 + self.flight.arrival_time.minute + day_diff.days * 1440
        elif day_diff.days == 1:
            flight_time = (1440 - (self.flight.departure_time.hour * 60 + self.flight.departure_time.minute)) \
                          + self.flight.arrival_time.hour * 60 + self.flight.arrival_time.minute
        elif day_diff.days == 0:
            flight_time = (self.flight.arrival_time.hour * 60 + self.flight.arrival_time.minute) - \
                          (self.flight.departure_time.hour * 60 + self.flight.departure_time.minute)
        flight_time_hours = flight_time // 60
        flight_time_minutes = flight_time - flight_time_hours * 60
        return str(flight_time_hours) + '.' + str(flight_time_minutes) + 'h'

    def __str__(self):
        return "{} {} - {} : {} {} {}".format(self.departure_datetime, self.flight.departure_airport,
                                              self.flight.arrival_airport, self.left_seats_E, self.left_seats_B,
                                              self.left_seats_F)

    def get_left_seats(self, class_of_service):
        if class_of_service == Flight.ECONOMY_CLASS:
            return self.left_seats_E
        elif class_of_service == Flight.BUSINESS_CLASS:
            return self.left_seats_B
        elif class_of_service == Flight.FIRST_CLASS:
            return self.left_seats_F
