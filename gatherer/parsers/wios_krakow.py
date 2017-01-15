from abc import ABC, abstractmethod
import datetime, json, multiprocessing, pytz, requests
from datetime import date, datetime, timezone
from requests.packages.urllib3.util.url import Url

from gatherer.service import AbstractWorker
from webui.models import Measurement, Parameter, Station, Parser, Area
from time import sleep


class Common(AbstractWorker):
    station = None
    url     = None
    pm_type = None
    day     = None

    def __init__(self, pm_type, day, station):
        super().__init__()
        self.day     = day
        self.pm_type = Parameter.objects.get(name=pm_type.upper())
        self.station = station
        self.url     = Parser.objects.get(name="wios_krakow").url

    def consume(self):
        headers = {'Accept': 'application/json'}
        payload = {
            "measType": "Auto",
            "viewType": "Parameter",
            "dateRange": "Day",
            "date": self.day.strftime('%d.%m.%Y'),
            "viewTypeEntityId": self.pm_type.name.lower(),
            "channels": [self.getChannelFor(self.pm_type.name.lower())]
        }

        output = None
        req = requests.post(self.url, data={"query": json.dumps(payload)}, headers=headers)
        if req.status_code == 200:
            output = req.json()

        return output

    def process(self):
        if not self.json:
            return

        # first flush any Measurements for that date/station/param
        Measurement.objects.filter(
            date__startswith=self.day.strftime('%Y-%m-%d'),
            station=self.station,
            type=self.pm_type
        ).all().delete()

        # now process the new data
        for day in self.json["data"]["series"]:
            for record in day["data"]:
                utc_time = datetime.fromtimestamp(int(record[0]), timezone.utc)
                local_time = utc_time.astimezone()
                value  = record[1]

                Measurement(date=local_time, value=value, station=self.station, type=self.pm_type).save()


    def getChannelFor(self, pm_type):
        return self.channels[pm_type]


class Kurdwanow(Common):
    channels = {
        "pm10": 148,
        "pm2.5": 242,
    }


class NowaHuta(Common):
    channels = {
        "pm10": 57,
        "pm2.5": 211,
    }


class Krasinskiego(Common):
    channels = {
        "pm10": 46,
        "pm2.5": 202,
    }
