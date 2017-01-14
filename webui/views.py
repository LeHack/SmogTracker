from datetime import date
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import dateparse
from .models import Area, Measurement, Parameter, Station
from gatherer.models import Gatherer
from gatherer.service import Manager


def index(request):
    # fetch params and set defaults
    pm_type_name = request.POST['pm'] if 'pm' in request.POST else Parameter.objects.first().name
    pm_type = Parameter.objects.get(name=pm_type_name)

    area = None
    area_name = request.POST['area'] if 'area' in request.POST else "dowolne"
    if area_name != "dowolne":
        area = Area.objects.get(name=area_name)
    else:
        area_name = "dowolne"

    areas = [Area(name="dowolne")]
    for a in Area.objects.all():
        areas.append(a)

    day = Measurement.objects.last().date
    if 'date' in request.POST:
        temp = dateparse.parse_date(request.POST['date'])
        if temp is not None:
            day = temp
        else:
            day = date.today()

    params = {
        "available": {
            "pm": Parameter.objects.all(),
            "area": areas
        },
        "selected": {
            "pm": pm_type_name,
            "area": area_name,
            "date": day.strftime('%Y-%m-%d')
        }
    }

    filters = {"date__startswith": day.strftime('%Y-%m-%d')}
    stations = []
    if area:
        filters["station__area"] = area
        stations = Station.objects.filter(area=area).all().order_by("name")
    else:
        stations = Station.objects.all().order_by("name")

    if pm_type:
        filters["type"] = pm_type

    parsed = {}
    for entry in Measurement.objects.filter(**filters).all().order_by('date'):
        if entry.date not in parsed:
            parsed[entry.date] = {
                'date': entry.date.strftime('%H:%M:%S'),
            }
        norm = (entry.value * 100 / entry.type.norm)
        parsed[entry.date][entry.station.name] = {
            "raw"  : entry.value,
            "norm" : ("%.02d") % (norm),
            "class": get_class_for(norm),
        }

    context = {
        'data': [parsed[date] for date in sorted(parsed.keys())],
        'params': params,
        'stations': stations
    }
    return render(request, 'webui/index.html', context)


def startDataRefresh(request):
    # if there is no other process running
    status = "busy"
    if Manager.isReady():
        Manager(run_by=Gatherer.UI).fireAndForget()
        status = "started"

    return JsonResponse({"refresh": status})


def checkDataRefresh(request):
    # if there is no other process running
    status = "working"
    if Manager.isReady():
        status = "ready"

    return JsonResponse({"refresh": status})


def get_class_for(norm):
    if (norm > 700):
        cls = "alarm"
    elif (norm > 400):
        cls = "dangr" # danger is a bootstrap class, so I8E
    elif (norm > 200):
        cls = "warn"
    elif (norm > 75):
        cls = "notice"
    else:
        cls = "ok"
    return cls
