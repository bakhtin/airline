# Generated by Django 4.2.3 on 2023-07-14 12:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("unique_flight", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uniqueflight",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
