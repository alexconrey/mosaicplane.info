from django.core.management.base import BaseCommand
from aircraft.models import Manufacturer, Aircraft


class Command(BaseCommand):
    help = 'Populate the database with MOSAIC-compliant aircraft data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating aircraft database...'))

        # Create manufacturers
        manufacturers_data = [
            # Current LSA manufacturers
            {'name': 'American Champion Aircraft', 'is_currently_manufacturing': True},
            {'name': 'Tecnam', 'is_currently_manufacturing': True},
            {'name': 'Flight Design', 'is_currently_manufacturing': True},
            {'name': 'Evektor', 'is_currently_manufacturing': True},
            {'name': 'Progressive Aerodyne', 'is_currently_manufacturing': True},
            {'name': 'Quicksilver Aircraft', 'is_currently_manufacturing': True},
            {'name': 'Czech Sport Aircraft', 'is_currently_manufacturing': True},
            {'name': 'Remos', 'is_currently_manufacturing': True},
            {'name': 'Icon Aircraft', 'is_currently_manufacturing': True},
            {'name': 'Pipistrel', 'is_currently_manufacturing': True},
            # Manufacturers that could benefit from MOSAIC expansion
            {'name': 'Cessna', 'is_currently_manufacturing': True},
            {'name': 'Piper', 'is_currently_manufacturing': True},
            {'name': 'Cirrus', 'is_currently_manufacturing': True},
            {'name': 'Diamond Aircraft', 'is_currently_manufacturing': True},
            # Legacy manufacturers
            {'name': 'Maule Air', 'is_currently_manufacturing': True},
            {'name': 'Aviat Aircraft', 'is_currently_manufacturing': True},
        ]

        manufacturers = {}
        for mfg_data in manufacturers_data:
            mfg, created = Manufacturer.objects.get_or_create(
                name=mfg_data['name'],
                defaults={'is_currently_manufacturing': mfg_data['is_currently_manufacturing']}
            )
            manufacturers[mfg_data['name']] = mfg
            if created:
                self.stdout.write(f'  Created manufacturer: {mfg.name}')

        # Create aircraft data - focusing on likely MOSAIC-compliant aircraft
        aircraft_data = [
            # Current LSA that would remain compliant
            {
                'manufacturer': 'Tecnam',
                'model': 'P2008-JC',
                'clean_stall_speed': 35.0,
                'top_speed': 118.0,
                'maneuvering_speed': 97.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'Flight Design',
                'model': 'CTLS',
                'clean_stall_speed': 39.0,
                'top_speed': 120.0,
                'maneuvering_speed': 97.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'Czech Sport Aircraft',
                'model': 'SportCruiser',
                'clean_stall_speed': 39.0,
                'top_speed': 120.0,
                'maneuvering_speed': 100.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'Icon Aircraft',
                'model': 'A5',
                'clean_stall_speed': 45.0,
                'top_speed': 109.0,
                'maneuvering_speed': 87.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'Pipistrel',
                'model': 'Virus SW 121',
                'clean_stall_speed': 37.0,
                'top_speed': 135.0,
                'maneuvering_speed': 108.0,
                'is_mosaic_compliant': True
            },
            # Aircraft that could become MOSAIC-compliant under expanded rules
            {
                'manufacturer': 'Cessna',
                'model': '150',
                'clean_stall_speed': 48.0,
                'top_speed': 109.0,
                'maneuvering_speed': 100.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'Cessna',
                'model': '152',
                'clean_stall_speed': 48.0,
                'top_speed': 110.0,
                'maneuvering_speed': 104.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'Piper',
                'model': 'J-3 Cub',
                'clean_stall_speed': 38.0,
                'top_speed': 87.0,
                'maneuvering_speed': 70.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'American Champion Aircraft',
                'model': 'Citabria 7ECA',
                'clean_stall_speed': 50.0,
                'top_speed': 115.0,
                'maneuvering_speed': 115.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'Aviat Aircraft',
                'model': 'Husky A-1C',
                'clean_stall_speed': 44.0,
                'top_speed': 145.0,
                'maneuvering_speed': 120.0,
                'is_mosaic_compliant': True
            },
            # More modern aircraft that could benefit from MOSAIC
            {
                'manufacturer': 'Diamond Aircraft',
                'model': 'DA20-C1',
                'clean_stall_speed': 53.0,
                'top_speed': 147.0,
                'maneuvering_speed': 111.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'Tecnam',
                'model': 'P2006T',
                'clean_stall_speed': 58.0,
                'top_speed': 155.0,
                'maneuvering_speed': 122.0,
                'is_mosaic_compliant': True
            },
            # Experimental aircraft that could be included
            {
                'manufacturer': 'Progressive Aerodyne',
                'model': 'SeaRey',
                'clean_stall_speed': 39.0,
                'top_speed': 115.0,
                'maneuvering_speed': 92.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'Quicksilver Aircraft',
                'model': 'Sport 2S',
                'clean_stall_speed': 28.0,
                'top_speed': 63.0,
                'maneuvering_speed': 55.0,
                'is_mosaic_compliant': True
            },
            {
                'manufacturer': 'Remos',
                'model': 'GX',
                'clean_stall_speed': 39.0,
                'top_speed': 135.0,
                'maneuvering_speed': 108.0,
                'is_mosaic_compliant': True
            }
        ]

        aircraft_count = 0
        for aircraft_info in aircraft_data:
            manufacturer = manufacturers[aircraft_info['manufacturer']]
            aircraft, created = Aircraft.objects.get_or_create(
                manufacturer=manufacturer,
                model=aircraft_info['model'],
                defaults={
                    'clean_stall_speed': aircraft_info['clean_stall_speed'],
                    'top_speed': aircraft_info['top_speed'],
                    'maneuvering_speed': aircraft_info['maneuvering_speed'],
                    'is_mosaic_compliant': aircraft_info['is_mosaic_compliant']
                }
            )
            if created:
                aircraft_count += 1
                self.stdout.write(f'  Created aircraft: {aircraft}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database with {len(manufacturers)} manufacturers '
                f'and {aircraft_count} aircraft'
            )
        )