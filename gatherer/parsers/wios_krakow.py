from abc import ABC, abstractmethod
import datetime
import multiprocessing

import pytz
import requests
from requests.packages.urllib3.util.url import Url

from gatherer.service import AbstractWorker
from webui.models import Measurement, Parameter, Station, Parser, Area
from time import sleep


class Common(AbstractWorker):
    def consume(self):
        # todo: get url from database
        req = requests.get(self.url)
        if req.status_code == 200:
            return req.json()
        return ""

    def process(self):
        if not self.json:
            return

        station = self.__saveToDb__()

        data = self.json["dane"]["forecast"]["dzisiaj"]["details"]
        for record in data:
            if record["fo_wskaznik"] == "pm10":
                date = pytz.timezone('CET').localize(datetime.datetime.now())
                Measurement(date=date, value=record["fo_wartosc"], station=station, type=Parameter.objects.get(name="PM10")).save()

        return

    def __saveToDb__(self):
        try:
            parserFromDb = Parser.objects.get(name=self.PARSER_NAME)
            return Station.objects.get(parser=parserFromDb)
        except Parser.DoesNotExist:
            parser = Parser(name=self.PARSER_NAME)
            parser.save()
            area = Area.objects.get(name="Nowa Huta", city="Kraków")
            station = Station(
                name="Nowa Huta",
                url=Url(self.url),
                street="Bulwarowa",
                area=area,
                parser=parser
            )
            station.save()

        return station


class Kurdwanow(Common):
    def name(self):
        return "Kurdwanów"


class NowaHuta(Common):
    def name(self):
        return "Nowa Huta"


class Krasinskiego(Common):
    def name(self):
        sleep(3)
        return "Aleja Krasińskiego"
