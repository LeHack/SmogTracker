from django.utils import timezone
from django.db import models


class Area(models.Model):
    name = models.CharField('nazwa', max_length=100)
    city = models.CharField('miasto', max_length=100)

    class Meta:
        verbose_name = "obszar"
        verbose_name_plural = "obszary"

    def __str__(self):
        return self.name


class Parser(models.Model):
    name = models.CharField('nazwa', max_length=100)

    def __str__(self):
        return self.name


class Station(models.Model):
    name    = models.CharField('nazwa', max_length=100)
    street  = models.CharField('ulica', max_length=100)
    added   = models.DateField('data dodania', default=timezone.now)
    url     = models.URLField('adres zasobu')
    area    = models.ForeignKey(Area, related_name='stations')
    parser  = models.ForeignKey(Parser, related_name='stations')

    class Meta:
        verbose_name = "stacja"
        verbose_name_plural = "stacje"

    def __str__(self):
        return self.name


class Parameter(models.Model):
    name        = models.CharField('nazwa', max_length=100)
    description = models.CharField('opis', max_length=1024)
    norm        = models.FloatField('norma godzinowa (µg)')

    class Meta:
        verbose_name = "parametr"
        verbose_name_plural = "parametry"

    def __str__(self):
        return self.name


class Measurement(models.Model):
    date    = models.DateTimeField('czas pomiaru')
    value   = models.FloatField('wartość')
    type    = models.ForeignKey(Parameter, related_name='measurements')
    station = models.ForeignKey(Station, related_name='measurements')

    class Meta:
        verbose_name = "pomiar"
        verbose_name_plural = "pomiary"

    def __str__(self):
        return "%s [%s]".format(self.type, self.date.strftime('%Y-%m-%d %H:%M:%S'))
