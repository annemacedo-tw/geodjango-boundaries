from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from boundaries.models import City, argentinian_cities_mapping


class Command(BaseCommand):
    help = 'Import argentinian cities layer'

    def add_arguments(self, parser):
        parser.add_argument('shapefile_path', nargs='+', type=str)

    def handle(self, *args, **options):

        shapefile_path = options['shapefile_path'][0]
        lm = LayerMapping(City, shapefile_path, argentinian_cities_mapping,
                          transform=True, encoding='utf-8')

        lm.save(strict=True, verbose=True)

        self.stdout.write('Camada de países importada com sucesso! Caminho do arquivo fornecido: "%s"' % shapefile_path)
