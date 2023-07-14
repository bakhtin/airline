from django.core.validators import MaxValueValidator
from django.db import models


class Aircraft(models.Model):
    FIRST_CLASS = 'F'
    BUSINESS_CLASS = 'B'
    ECONOMY_CLASS = 'E'
    CLASS_OF_SERVICE = (
        (FIRST_CLASS, 'First'),
        (BUSINESS_CLASS, 'Business'),
        (ECONOMY_CLASS, 'Economy'),
    )
    company = models.CharField(max_length=16)
    model = models.CharField(max_length=16)
    seat_count_F = models.IntegerField(default=0, validators=[MaxValueValidator(3)])
    seat_count_B = models.IntegerField(default=0, validators=[MaxValueValidator(3)])
    seat_count_E = models.IntegerField(default=0, validators=[MaxValueValidator(3)])
    seats_in_a_row_F = models.IntegerField(default=0)
    seats_in_a_row_B = models.IntegerField(default=0)
    seats_in_a_row_E = models.IntegerField(default=0)
    seat_map_picture = models.ImageField(default='', upload_to='aircraft_images')

    def get_seat_count(self, class_of_service):
        if class_of_service == self.FIRST_CLASS:
            return self.seat_count_F
        elif class_of_service == self.BUSINESS_CLASS:
            return self.seat_count_B
        else:
            return self.seat_count_E

    def seat_map_generator(self):
        seat_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K']
        seat_count_F = self.seat_count_F
        seat_count_B = self.seat_count_B
        seat_count_E = self.seat_count_E
        seats_F = []
        seats_B = []
        seats_E = []
        i = 0
        j = 0
        while seat_count_F > 0:
            seat_count_F -= self.seats_in_a_row_F
            for seat in seat_letters:
                if j == self.seats_in_a_row_F:
                    j = 0
                    break
                seats_F.append(str(seat_letters[j]) + str(i+1))
                j += 1
            i += 1
        while seat_count_B > 0:
            for seat in seat_letters:
                if j == self.seats_in_a_row_B:
                    j = 0
                    break
                seats_B.append(str(seat_letters[j]) + str(i+1))
                j += 1
            seat_count_B -= self.seats_in_a_row_B
            i += 1
        while seat_count_E > 0:
            seat_count_E -= self.seats_in_a_row_E
            for seat in seat_letters:
                if j == self.seats_in_a_row_E:
                    j = 0
                    break
                seats_E.append(str(seat_letters[j]) + str(i + 1))
                j += 1
            i += 1
        return {'F': seats_F, 'B': seats_B, 'E': seats_E}

    def __str__(self):
        return '{} {}'.format(self.company, self.model, self.seat_count_F, self.seat_count_B, self.seat_count_E)
