# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aircraft', '0001_initial'),
        ('airport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flight_number', models.CharField(max_length=8, verbose_name=b'Flight Number')),
                ('departure_date_begin', models.DateField(default=b'1990-01-01', verbose_name=b'Departure date begin')),
                ('arrival_date_begin', models.DateField(default=b'1990-01-01', verbose_name=b'Arrival date begin')),
                ('repeat_interval', models.IntegerField(default=1, verbose_name=b'Repeat interval')),
                ('departure_time', models.TimeField(default=b'08:00', verbose_name=b'Departure time')),
                ('arrival_time', models.TimeField(default=b'10:00', verbose_name=b'Arrival time')),
                ('price_F', models.FloatField(default=b'22500', verbose_name=b'Price first class')),
                ('price_B', models.FloatField(default=b'18200', verbose_name=b'Price business class')),
                ('price_E', models.FloatField(default=b'11400', verbose_name=b'Price economic class')),
                ('aircraft', models.ForeignKey(related_name='aircraft', default=b'', verbose_name=b'Aircraft', on_delete=models.CASCADE, to='aircraft.Aircraft')),
                ('arrival_airport', models.ForeignKey(related_name='arrival_airport', default=b'', on_delete=models.CASCADE, verbose_name=b'Arrival airport', to='airport.Airport')),
                ('departure_airport', models.ForeignKey(related_name='departure_airport', default=b'', on_delete=models.CASCADE, verbose_name=b'Departure airport', to='airport.Airport')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
