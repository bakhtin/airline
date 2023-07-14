import os
from django.http import HttpResponse, Http404

from django.shortcuts import render
from django.template.context import RequestContext

from aircraft.forms import AircraftForm
from aircraft.models import Aircraft
from wsgiref.util import FileWrapper


def show_seat_conf(request):
    if request.method == 'POST':
        aircraft_form = AircraftForm(request.POST)
        if aircraft_form.is_valid():
            aircraft_id = int(request.POST['aircraft'])
            aircraft = Aircraft.objects.filter(pk=aircraft_id)
            seat_conf = Aircraft.seat_map_generator(aircraft[0])
            return render(request, 'seat_conf.html', {'seat_conf': seat_conf})
    else:
        aircraft_form = AircraftForm()
        return render(request, 'seat_conf.html', {
            'aircraft_form': aircraft_form})


def get_image(request):
    path_items = request.get_full_path().split('/')
    image_name = os.path.join(path_items[-2], path_items[-1])
    image_ext = image_name.split('.')[-1]
    images = Aircraft.objects.filter(seat_map_picture=image_name)

    if images.count() == 0:
        raise Http404

    image = images[0].seat_map_picture
    response = HttpResponse(FileWrapper(image), content_type='image/%s' % image_ext)
    response['Content-Disposition'] = 'attachment; filename=%s' % image_name.split('/')[-1]
    return response