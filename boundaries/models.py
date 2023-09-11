# -*- coding: utf-8 -*-

from django.db.models import Manager as GeoManager
from django.contrib.gis.db import models


class NamedModel(models.Model):
    name = models.CharField(max_length=255)

    geometry = models.MultiPolygonField()  # Multipolygon in NAD83
    objects = GeoManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Country(NamedModel):
    iso_code = models.CharField(max_length=4, blank=True)


class State(NamedModel):
    label = models.CharField(max_length=255)
    acronym = models.CharField(max_length=64, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country)


class City(NamedModel):
    label = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey(State, blank=True, null=True)
    country = models.ForeignKey(Country)


cities_ibge_mapping = {
    'name': 'NOME_MUNIC',
    'region': 'REGIão',
    'state': {'acronym': 'SIGLA'},
    'geometry': 'POLYGON',
}

# Mapping dictionaries for the models above.
state_ibge_mapping = {
    'acronym': 'SIGLA',
    'country': {'name': 'pais'},
    # 'geometry': 'MULTIPOLYGON',  # Will convert POLYGON features into MULTIPOLYGONS,
    'geometry': 'POLYGON',
}

country_ibge_mapping = {
    'name': 'name',
    'geometry': 'POLYGON',
}

argentinian_cities_mapping = {
    'name': 'FNA',
    'geometry': 'POLYGON'
}
