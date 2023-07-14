# coding: utf-8
import uuid
import datetime

from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.context import RequestContext

from order.forms import OrderForm
from order.models import Order
from unique_flight.models import UniqueFlight
from django.core.mail import EmailMessage


def fill_data(request):
    if request.method == 'POST':
        unique_flight_id = request.POST['unique_flight_id']
        class_of_service = request.POST['class_of_service']

        unique_flight = UniqueFlight.objects.filter(id__exact=unique_flight_id)[0]

        order_form = OrderForm()
        return render(request, 'order.html', {'order_form': order_form, 'unique_flight': unique_flight,
                                                 'class_of_service': class_of_service,
                                                 'price': unique_flight.get_price(class_of_service)})
    else:
        return redirect('/search/')


def send_order(order):
    HOST = 'https://calm-stream-1314.herokuapp.com'
    email = EmailMessage(subject='Your order',
                         body='Thanks for choosing us!\n'
                              'Link to your order is {}/show_order/order_id/{}/hash/{}'.format(HOST, order.id, order.order_hash),
                         to=[order.email])
    email.send()
    return 0


def place_order(request):
    if request.method == 'POST':
        search_form = OrderForm(request.POST)
        if search_form.is_valid():
            unique_flight_id = request.POST['unique_flight_id']
            first_name = search_form.cleaned_data['first_name']
            last_name = search_form.cleaned_data['last_name']
            document_id = search_form.cleaned_data['document_id']
            birth_day = search_form.cleaned_data['birth_day']
            email = search_form.cleaned_data['email']
            class_of_service = request.POST['class_of_service']

            order = Order(unique_flight_id=unique_flight_id,
                          first_name=first_name,
                          last_name=last_name,
                          document_id=document_id,
                          birth_day=birth_day,
                          email=email,
                          order_hash=uuid.uuid1().hex,
                          booking_id=uuid.uuid1().hex[:7].upper(),
                          class_of_service=class_of_service)

            if order.unique_flight.try_take_seat(class_of_service):
                order.save()
                send_order(order)
                return render(request, 'status.html', {'status': 'Order created, link sent to you by email'})
            else:
                return render(request, 'status.html', {
                    'status': 'We are sorry, but there are no free places of class you have chosen'})
    else:
        return redirect('/search/')


def show_order(request, order_id, order_hash):
    try:
        order = Order.objects.get(pk=order_id, order_hash=order_hash)
    except Order.DoesNotExist:
        raise Http404
    diff = int((order.unique_flight.departure_datetime - datetime.datetime.now()).total_seconds() / 60)
    if 30 < diff < 360:
        aircraft = order.unique_flight.flight.aircraft
        free_seats = Order.get_free_seats(order.unique_flight.id, aircraft, order.class_of_service)
        return render(request, 'show_order.html', {'order': order,
                                                      'price': order.unique_flight.get_price(order.class_of_service),
                                                      'free_seats': free_seats,
                                                      'order_id': order_id})
    else:
        return render(request, 'status.html', {'status': 'It is not time for registration yet'})


def register(request):
    if request.method != 'POST':
        return redirect('/search/')

    order_id = request.POST['order_id']
    order = Order.objects.get(pk=order_id)
    diff = int((order.unique_flight.departure_datetime - datetime.datetime.now()).total_seconds() / 60)

    if order.is_registered:
        status = 'You have already registered'
    elif 30 < diff < 360:
        if order.try_take_seat(request.POST['seats']):
            status = 'You are successfully registered'
        else:
            status = 'Sorry, seat is already taken, try again'
    elif diff < 30:
        status = 'Sorry, but registration on this flight completed'
    else:
        status = 'It is not time for registration yet'

    return render(request, 'status.html', {'status': status})


def ticket(request):
    pass