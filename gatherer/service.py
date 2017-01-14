import datetime
import multiprocessing
import pytz

from webui.models import Measurement, Parameter, Station, Parser, Area
from pip._vendor.requests.packages.urllib3.util.url import Url

"""pip install requests"""
import requests
from abc import ABC, abstractmethod


class AbstractWorker(ABC, multiprocessing.Process):
    json = ""

    def run(self):
        self.json = self.consume()
        self.process()
        return

    @abstractmethod
    def consume(self):
        pass

    @abstractmethod
    def process(self):
        pass


class ForecastWorker(AbstractWorker):
    url = "http://powietrze.malopolska.pl/_powietrzeapi/api/dane?act=danemiasta&ci_id=1"  # Krakow
    PARSER_NAME = "powietrze-malopolska"

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


class Manager:
    workers = [
        ForecastWorker()
    ]

    def run(self):
        for worker in self.workers:
            worker.start()
            worker.join()
