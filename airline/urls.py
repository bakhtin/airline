from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import aircraft.views
import flight.views
import order.views

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flights/', flight.views.ListFlightView.as_view(), name='flights'),
    path('', flight.views.index),
    path('search/', flight.views.search),
    path('flights_all/', flight.views.show_all),
    path('search_results/', flight.views.search),
    path('blog/', include('blog.urls')),
    path('fill_data/', order.views.fill_data),
    path('place_order/', order.views.place_order),
    path('show_order/order_id/<int:order_id>/hash/<str:hash_str>/', order.views.show_order),
    path('register/', order.views.register),
    path('seat_conf/', aircraft.views.show_seat_conf),
    path('media/aircraft_images/<str:image>', aircraft.views.get_image),
    path('contacts/', flight.views.contacts),
    # path('timetable/', flight.views.timetable),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
