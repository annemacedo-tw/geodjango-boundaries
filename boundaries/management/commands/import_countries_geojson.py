from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from boundaries.models import Country
import json
import ipdb


class Command(BaseCommand):
    help = 'Import GeoJSON Country Data from whoisonfirst.org'

    def add_arguments(self, parser):
        parser.add_argument('geojson_path', nargs='+', type=str)

    def handle(self, *args, **options):

        for geojson_file in options['geojson_path']:
            with open(geojson_file) as f:
                jason = json.load(f)

            geometry = GEOSGeometry(str(jason['geometry']))
            if geometry.geom_type == 'Polygon':
                geometry = MultiPolygon(geometry)
            name = jason['properties']['name:por_x_preferred'][0]
            iso_code = jason['properties']['iso:country']

            try:
                country = Country.objects.get(name=name)
                country.geometry = geometry
                country.iso_code = iso_code
                country.save()
            except Country.DoesNotExist:
                country = Country(name=name, geometry=geometry, iso_code=iso_code)
                country.save()

            self.stdout.write('''País importado com sucesso! 
                                 Caminho do arquivo fornecido: "%s"
                                 País é "%s"''' % (geojson_file, name))

        self.stdout.write('Comando terminado com sucesso')
