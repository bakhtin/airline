# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('city', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=3, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xb4')),
                ('city', models.ForeignKey(default=b'', on_delete=models.CASCADE, to='city.City')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
