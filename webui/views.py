from django.shortcuts import render
from .models import Measurement, Parameter, Station


def index(request):
    data = Measurement.objects.all().order_by('date')
    selected = Parameter.objects.first().name
    if 'p' in request.GET:
        selected = request.GET['p']
    pType = Parameter.objects.get(name=selected)
    parsed = {}
    for entry in data:
        if entry.type == pType:
            if entry.date in parsed:
                parsed[entry.date][entry.station.name] = entry.value
            else:
                parsed[entry.date] = {
                    'date': entry.date.strftime('%H:%M:%S'),
                    entry.station.name: entry.value
                }

    context = {
        'data': [parsed[date] for date in sorted(parsed.keys())],
        'params': Parameter.objects.all(),
        'stations': Station.objects.all(),
        'selected': selected
    }
    return render(request, 'webui/index.html', context)
