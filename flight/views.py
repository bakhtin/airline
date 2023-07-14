# coding: utf-8
from django.shortcuts import render
from django.template.context import RequestContext
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView
from django.shortcuts import render
from blog.models import Post
from datetime import timedelta
from flight.models import Flight
from .forms import *
from unique_flight.models import UniqueFlight
from django.core.paginator import Paginator
from datetime import datetime
import datetime

class ListFlightView(ListView):
    model = Flight
    template_name = 'flights.html'


def index(request):
    search_form = SearchForm()
    posts = Post.objects.all()
    return render(request, 'index.html', {'search_form': search_form,
                                          'object_list': posts})


def contacts(request):
    return render(request, 'contacts.html')


def search(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            departure_city = search_form.cleaned_data['departure_city']
            arrival_city = search_form.cleaned_data['arrival_city']
            departure_date = search_form.cleaned_data['departure_date']

            unique_flights = []

            for flight in Flight.objects.all():
                diff = int((departure_date - flight.departure_date_begin).total_seconds() / 86400)

                if diff < 0 or diff % flight.repeat_interval != 0 \
                        or flight.departure_airport.city != departure_city \
                        or flight.arrival_airport.city != arrival_city:
                    continue

                departure_datetime = parse_datetime('{} {}'.format(departure_date, flight.departure_time))
                uniq_diff = flight.arrival_date_begin - flight.departure_date_begin
                arrival_date = departure_datetime.date() + timedelta(days=uniq_diff.days)
                arrival_time = flight.arrival_time
                db_unique_flights = UniqueFlight.objects.filter(flight__exact=flight,
                                                                departure_datetime=departure_datetime)

                if db_unique_flights.count() == 0:
                    unique_flight = UniqueFlight(flight_id=flight.id,
                                                 departure_datetime=departure_datetime,
                                                 arrival_date=arrival_date,
                                                 arrival_time=arrival_time,
                                                 left_seats_F=flight.aircraft.seat_count_F,
                                                 left_seats_B=flight.aircraft.seat_count_B,
                                                 left_seats_E=flight.aircraft.seat_count_E)
                    unique_flight.save()
                else:
                    unique_flight = db_unique_flights[0]

                unique_flights.append(unique_flight)

            return render(request, 'flights.html', {'unique_flights': unique_flights,
                                                       'search_form': search_form})
    else:
        search_form = SearchForm()
    return render(request, 'search.html', {'search_form': search_form})


def timetable(request):
    for flight in Flight.objects.all():
        day = flight.departure_date_begin.strftime("%A")
        interval = flight.repeat_interval
        if interval == 1:
            interval = 'Every day'
        elif interval == 7:
            interval = 'Every %s' % day
        else:
            interval = None
        day_diff = flight.arrival_date_begin - flight.departure_date_begin
        flight_time = ''
        if day_diff.days > 1:
            flight_time = (1440 - (flight.departure_time.hour * 60 + flight.departure_time.minute)) \
                          + flight.arrival_time.hour * 60 + flight.arrival_time.minute + day_diff.days * 1440
        elif day_diff.days == 1:
            flight_time = (1440 - (flight.departure_time.hour * 60 + flight.departure_time.minute)) \
                          + flight.arrival_time.hour * 60 + flight.arrival_time.minute
        elif day_diff.days == 0:
            flight_time = (flight.arrival_time.hour * 60 + flight.arrival_time.minute) - \
                          (flight.departure_time.hour + flight.departure_time.minute)
        flight_time_hours = flight_time // 60
        flight_time_minutes = flight_time - flight_time_hours * 60
        return render(request, 'timetable.html', {'flight': flight,
                                                     'day': day,
                                                     'interval': interval,
                                                     'flight_time_hours': flight_time_hours,
                                                     'flight_time_minutes': flight_time_minutes})


def show_all(request):

    unique_flights = []

    today = datetime.date.today()

    for i in range(1, 183):
        current_day = today + datetime.timedelta(days=i)

        for flight in Flight.objects.all():
            diff = int((current_day - flight.departure_date_begin).total_seconds() / 86400)

            if diff < 0 or diff % flight.repeat_interval != 0:
                continue

            current_datetime = parse_datetime('{} {}'.format(current_day, flight.departure_time))
            uniq_diff = flight.arrival_date_begin - flight.departure_date_begin
            arrival_date = current_datetime.date() + timedelta(days=uniq_diff.days)
            arrival_time = flight.arrival_time
            db_unique_flights = UniqueFlight.objects.filter(flight__exact=flight,
                                                            departure_datetime=current_datetime)

            if db_unique_flights.count() == 0:
                unique_flight = UniqueFlight(flight_id=flight.id,
                                             departure_datetime=current_datetime,
                                             arrival_date=arrival_date,
                                             arrival_time=arrival_time,
                                             left_seats_F=flight.aircraft.seat_count_F,
                                             left_seats_B=flight.aircraft.seat_count_B,
                                             left_seats_E=flight.aircraft.seat_count_E
                                             )
                unique_flight.save()
            else:
                unique_flight = db_unique_flights[0]
            unique_flights.append(unique_flight)

    p = Paginator(unique_flights, 10)

    if 'page' in request.POST:
        page = request.POST.get("page", "")
        page_number = int(page)
    else:
        page_number = 1

    is_next = p.page(page_number).has_next()
    is_previous = p.page(page_number).has_previous()
    if 'next' in request.POST:
        if is_next:
            page_number += 1
    if 'previous' in request.POST:
        if is_previous:
            page_number -= 1

    is_next = p.page(page_number).has_next()
    is_previous = p.page(page_number).has_previous()

    current_objects = p.page(page_number).object_list
    return render(request, 'flights_all.html', {'object_list': current_objects,
                                                   'page_number': page_number, 'next': is_next,
                                                   'previous': is_previous})