from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import csv
from django.conf import settings
from urllib.parse import urlencode

with open(settings.BUS_STATION_CSV, encoding='cp1251') as csvfile:
    bus_stations_info = list(csv.DictReader(csvfile))

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    current_page = request.GET.get('page', '1')

    paginator = Paginator(bus_stations_info, 10)
    page_object = paginator.get_page(current_page)
    current_bus_stations = []
    for bus_station in page_object.object_list:
        current_bus_stations.append({'Name': bus_station['Name'], 'Street': bus_station['Street'], 'District': bus_station['District']})

    print(paginator.count)

    if int(current_page) > paginator.count//10+1:
        current_page = str(paginator.count//10+1)

    if page_object.has_next():
        next_page_url = f'{reverse(bus_stations)}?page={page_object.next_page_number()}'
    else:
        next_page_url = None

    if page_object.has_previous():
        previous_page_url = f'{reverse(bus_stations)}?page={page_object.previous_page_number()}'
    else:
        previous_page_url = None

    return render_to_response('index.html', context={
        'bus_stations': current_bus_stations,
        'current_page': current_page,
        'prev_page_url': previous_page_url,
        'next_page_url': next_page_url,
    })

