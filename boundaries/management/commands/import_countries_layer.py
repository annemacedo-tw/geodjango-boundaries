from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from boundaries.models import Country, country_ibge_mapping


class Command(BaseCommand):
    help = 'Import village layer'

    def add_arguments(self, parser):
        parser.add_argument('shapefile_path', nargs='+', type=str)

    def handle(self, *args, **options):

        shapefile_path = options['shapefile_path'][0]
        lm = LayerMapping(Country, shapefile_path, country_ibge_mapping,
                          transform=True, encoding='iso-8859-1')

        lm.save(strict=True, verbose=True)

        self.stdout.write('Camada de países importada com sucesso! Caminho do arquivo fornecido: "%s"' % shapefile_path)
