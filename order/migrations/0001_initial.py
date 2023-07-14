# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unique_flight', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('registration_time', models.DateTimeField(default=b'1990-01-01 00:00', verbose_name=b'Flight registration time')),
                ('is_registered', models.BooleanField(default=False, verbose_name=b'Is registered')),
                ('first_name', models.CharField(default=b'', max_length=255, verbose_name=b'First name')),
                ('last_name', models.CharField(default=b'', max_length=255, verbose_name=b'Last name')),
                ('document_id', models.CharField(default=b'', max_length=11, verbose_name=b'Document ID')),
                ('birth_day', models.DateField(default=b'1990-01-01', verbose_name=b'Date of birth')),
                ('email', models.EmailField(default=b'', max_length=255, verbose_name=b'Email')),
                ('order_hash', models.CharField(default=b'', max_length=256, verbose_name=b'Hash')),
                ('booking_id', models.CharField(default=b'', max_length=7, verbose_name=b'Booking ID')),
                ('class_of_service', models.CharField(default=b'E', max_length=1, verbose_name=b'Class of service')),
                ('taken_seat', models.CharField(default=b'', max_length=4)),
                ('unique_flight', models.ForeignKey(default=b'', verbose_name=b'Unique flight', on_delete=models.CASCADE, to='unique_flight.UniqueFlight')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
