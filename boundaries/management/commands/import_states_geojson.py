from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from boundaries.models import Country, State
import json
import sys


class Command(BaseCommand):
    help = 'Import states GeoJSON from whoisonfirst.org'

    def add_arguments(self, parser):
        parser.add_argument('geojson_path', nargs='+', type=str)

    def handle(self, *args, **options):

        geojson_path = options['geojson_path']

        for geojson_file in geojson_path:
            print(geojson_file)
            with open(geojson_file) as f:
                jason = json.load(f)

            try:
                acronym = jason['properties']['abrv:eng_x_preferred'][0]
            except KeyError:
                acronym = jason['properties']['statoids:iso']
            geometry = GEOSGeometry(str(jason['geometry']))
            if geometry.geom_type == 'Polygon':
                geometry = MultiPolygon(geometry)
            name = jason['properties']['name:por_x_preferred'][0]
            iso_code = jason['properties']['iso:country']

            try:
                country = Country.objects.get(iso_code=iso_code)
            except Country.DoesNotExist:
                print('There is no country for this state')
                sys.exit(0)


            try:
                state = State.objects.get(country=country, acronym=acronym)
                state.geometry = geometry
                state.name = name
                state.save()
            except State.DoesNotExist:
                state = State.objects.create(country=country,
                                             acronym=acronym,
                                             geometry=geometry,
                                             name=name)
                state.save()

            self.stdout.write('''Estado importado com sucesso! 
                                 Caminho do arquivo fornecido: "%s"
                                 Estado é %s''' % (geojson_file, name))

        self.stdout.write('Estados Importados')
