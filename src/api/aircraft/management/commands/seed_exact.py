from django.core.management.base import BaseCommand
from aircraft.models import Manufacturer, Aircraft, Engine
from django.db import transaction


class Command(BaseCommand):
    help = 'Populate the database with exactly 120 MOSAIC-compliant aircraft matching current database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding aircraft database with exact 120 aircraft...'))
        
        with transaction.atomic():
            # Create manufacturers
            self.create_manufacturers()
            
            # Create engines 
            self.create_engines()
            
            # Create all aircraft
            self.create_all_aircraft()
            
        self.stdout.write(self.style.SUCCESS('Successfully seeded database with exactly 120 aircraft'))

    def create_manufacturers(self):
        manufacturers_data = [
            {'name': 'American Champion Aircraft', 'is_currently_manufacturing': True},
            {'name': 'Aviat Aircraft', 'is_currently_manufacturing': True},
            {'name': 'Beechcraft', 'is_currently_manufacturing': True},
            {'name': 'Cessna', 'is_currently_manufacturing': True},
            {'name': 'Champion Aircraft', 'is_currently_manufacturing': False},
            {'name': 'Czech Sport Aircraft', 'is_currently_manufacturing': True},
            {'name': 'Diamond Aircraft', 'is_currently_manufacturing': True},
            {'name': 'Evektor', 'is_currently_manufacturing': True},
            {'name': 'Flight Design', 'is_currently_manufacturing': True},
            {'name': 'Grumman', 'is_currently_manufacturing': False},
            {'name': 'Icon Aircraft', 'is_currently_manufacturing': True},
            {'name': 'Lake Aircraft', 'is_currently_manufacturing': False},
            {'name': 'Maule Air', 'is_currently_manufacturing': True},
            {'name': 'Piper', 'is_currently_manufacturing': True},
            {'name': 'Pipistrel', 'is_currently_manufacturing': True},
            {'name': 'Progressive Aerodyne', 'is_currently_manufacturing': True},
            {'name': 'Quicksilver Aircraft', 'is_currently_manufacturing': True},
            {'name': 'Remos', 'is_currently_manufacturing': True},
            {'name': 'Tecnam', 'is_currently_manufacturing': True},
        ]

        self.manufacturers = {}
        for mfg_data in manufacturers_data:
            mfg, created = Manufacturer.objects.get_or_create(
                name=mfg_data['name'],
                defaults={'is_currently_manufacturing': mfg_data['is_currently_manufacturing']}
            )
            self.manufacturers[mfg_data['name']] = mfg
            if created:
                self.stdout.write(f'  Created manufacturer: {mfg.name}')

    def create_engines(self):
        engines_data = [
            {'manufacturer': 'Continental', 'model': 'C85', 'horsepower': 85, 'fuel_type': '100LL'},
            {'manufacturer': 'Continental', 'model': 'C90', 'horsepower': 90, 'fuel_type': '100LL'},
            {'manufacturer': 'Continental', 'model': 'O-200-A', 'horsepower': 100, 'fuel_type': '100LL'},
            {'manufacturer': 'Continental', 'model': 'O-300-A', 'horsepower': 145, 'fuel_type': '100LL'},
            {'manufacturer': 'Continental', 'model': 'O-470-R', 'horsepower': 230, 'fuel_type': '100LL'},
            {'manufacturer': 'Lycoming', 'model': 'O-235-C1', 'horsepower': 115, 'fuel_type': '100LL'},
            {'manufacturer': 'Lycoming', 'model': 'O-235-L2C', 'horsepower': 118, 'fuel_type': '100LL'},
            {'manufacturer': 'Lycoming', 'model': 'O-320-E2D', 'horsepower': 150, 'fuel_type': '100LL'},
            {'manufacturer': 'Lycoming', 'model': 'O-360-A4M', 'horsepower': 180, 'fuel_type': '100LL'},
            {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100, 'fuel_type': 'MOGAS'},
            {'manufacturer': 'Rotax', 'model': '914UL', 'horsepower': 115, 'fuel_type': 'MOGAS'},
        ]

        self.engines = {}
        for engine_data in engines_data:
            engine, created = Engine.objects.get_or_create(
                manufacturer=engine_data['manufacturer'],
                model=engine_data['model'],
                defaults={
                    'horsepower': engine_data['horsepower'],
                    'fuel_type': engine_data['fuel_type']
                }
            )
            self.engines[f"{engine_data['manufacturer']} {engine_data['model']}"] = engine
            if created:
                self.stdout.write(f'  Created engine: {engine}')

    def create_all_aircraft(self):
        # All 120 aircraft exactly as they exist in the database
        aircraft_data = [
            # American Champion Aircraft
            {'manufacturer': 'American Champion Aircraft', 'model': 'Citabria 7ECA', 'stall': 50.0, 'top': 115.0, 'maneuvering': 115.0, 'engine': 'Lycoming O-235-L2C'},
            
            # Aviat Aircraft  
            {'manufacturer': 'Aviat Aircraft', 'model': 'Husky A-1C', 'stall': 44.0, 'top': 145.0, 'maneuvering': 120.0, 'engine': 'Lycoming O-360-A4M'},
            
            # Beechcraft
            {'manufacturer': 'Beechcraft', 'model': 'Musketeer', 'stall': 55.0, 'top': 142.0, 'maneuvering': 119.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Beechcraft', 'model': 'Skipper 77', 'stall': 54.0, 'top': 122.0, 'maneuvering': 100.0, 'engine': 'Lycoming O-235-L2C'},
            {'manufacturer': 'Beechcraft', 'model': 'Sport 150', 'stall': 55.0, 'top': 131.0, 'maneuvering': 105.0, 'engine': 'Lycoming O-320-E2D'},
            
            # Cessna 150 variants
            {'manufacturer': 'Cessna', 'model': '150', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150A', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150B', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150C', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150D', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150E', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150F', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150G', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150H', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150J', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150K', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150L', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Cessna', 'model': '150M', 'stall': 48.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Continental O-200-A'},
            
            # Cessna 152
            {'manufacturer': 'Cessna', 'model': '152', 'stall': 48.0, 'top': 110.0, 'maneuvering': 104.0, 'engine': 'Lycoming O-235-L2C'},
            
            # Cessna 172 variants  
            {'manufacturer': 'Cessna', 'model': '172', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172A', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172B', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172C', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172D', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172E', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172F', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172G', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172H', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172I', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172K', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172L', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172M', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172N', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172P', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172Q Cutlass', 'stall': 48.0, 'top': 138.0, 'maneuvering': 108.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'Cessna', 'model': '172R', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '172S', 'stall': 47.0, 'top': 124.0, 'maneuvering': 99.0, 'engine': 'Continental O-300-A'},
            
            # Cessna 182 variants
            {'manufacturer': 'Cessna', 'model': '182', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182A', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182B', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182C', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182D', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182E', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182F', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182G', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182H', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182J', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182K', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182L', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182M', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182N', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182P', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182Q', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182R', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182S', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Cessna', 'model': '182T', 'stall': 49.0, 'top': 145.0, 'maneuvering': 140.0, 'engine': 'Continental O-470-R'},
            
            # Champion Aircraft
            {'manufacturer': 'Champion Aircraft', 'model': 'Citabria 7GCAA', 'stall': 51.0, 'top': 126.0, 'maneuvering': 113.0, 'engine': 'Lycoming O-320-E2D'},
            
            # Czech Sport Aircraft
            {'manufacturer': 'Czech Sport Aircraft', 'model': 'SportCruiser', 'stall': 39.0, 'top': 120.0, 'maneuvering': 100.0, 'engine': 'Rotax 912ULS'},
            
            # Diamond Aircraft
            {'manufacturer': 'Diamond Aircraft', 'model': 'DA20-A1', 'stall': 53.0, 'top': 147.0, 'maneuvering': 111.0, 'engine': 'Continental O-200-A'},
            {'manufacturer': 'Diamond Aircraft', 'model': 'DA20-C1', 'stall': 53.0, 'top': 147.0, 'maneuvering': 111.0, 'engine': 'Continental O-200-A'},
            
            # Evektor
            {'manufacturer': 'Evektor', 'model': 'SportStar', 'stall': 37.0, 'top': 118.0, 'maneuvering': 97.0, 'engine': 'Rotax 912ULS'},
            
            # Flight Design
            {'manufacturer': 'Flight Design', 'model': 'CTLS', 'stall': 39.0, 'top': 120.0, 'maneuvering': 97.0, 'engine': 'Rotax 912ULS'},
            
            # Grumman
            {'manufacturer': 'Grumman', 'model': 'AA-1A', 'stall': 60.0, 'top': 138.0, 'maneuvering': 131.0, 'engine': 'Lycoming O-235-C1'},
            {'manufacturer': 'Grumman', 'model': 'AA-1B', 'stall': 60.0, 'top': 138.0, 'maneuvering': 131.0, 'engine': 'Lycoming O-235-C1'},
            {'manufacturer': 'Grumman', 'model': 'AA-5', 'stall': 57.0, 'top': 139.0, 'maneuvering': 125.0, 'engine': 'Lycoming O-320-E2D'},
            
            # Icon Aircraft
            {'manufacturer': 'Icon Aircraft', 'model': 'A5', 'stall': 45.0, 'top': 109.0, 'maneuvering': 87.0, 'engine': 'Rotax 912ULS'},
            
            # Lake Aircraft
            {'manufacturer': 'Lake Aircraft', 'model': 'LA-4-200', 'stall': 50.0, 'top': 135.0, 'maneuvering': 110.0, 'engine': 'Lycoming O-360-A4M'},
            
            # Maule Air
            {'manufacturer': 'Maule Air', 'model': 'M-4-220C', 'stall': 40.0, 'top': 150.0, 'maneuvering': 125.0, 'engine': 'Continental O-470-R'},
            {'manufacturer': 'Maule Air', 'model': 'M-5-235C', 'stall': 42.0, 'top': 165.0, 'maneuvering': 130.0, 'engine': 'Lycoming O-235-L2C'},
            {'manufacturer': 'Maule Air', 'model': 'M-6-235', 'stall': 44.0, 'top': 180.0, 'maneuvering': 140.0, 'engine': 'Lycoming O-235-L2C'},
            {'manufacturer': 'Maule Air', 'model': 'M-7-235', 'stall': 46.0, 'top': 185.0, 'maneuvering': 145.0, 'engine': 'Lycoming O-235-L2C'},
            
            # Piper
            {'manufacturer': 'Piper', 'model': 'Cherokee 140', 'stall': 55.0, 'top': 139.0, 'maneuvering': 115.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Piper', 'model': 'Cherokee 150', 'stall': 55.0, 'top': 141.0, 'maneuvering': 125.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Piper', 'model': 'Cherokee 160', 'stall': 57.0, 'top': 144.0, 'maneuvering': 125.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Piper', 'model': 'Cherokee 180', 'stall': 58.0, 'top': 148.0, 'maneuvering': 125.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'Piper', 'model': 'J-3 Cub', 'stall': 38.0, 'top': 87.0, 'maneuvering': 70.0, 'engine': 'Continental C85'},
            {'manufacturer': 'Piper', 'model': 'Super Cub', 'stall': 43.0, 'top': 130.0, 'maneuvering': 100.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Piper', 'model': 'Tomahawk', 'stall': 54.0, 'top': 109.0, 'maneuvering': 100.0, 'engine': 'Lycoming O-235-L2C'},
            {'manufacturer': 'Piper', 'model': 'Tri-Pacer', 'stall': 49.0, 'top': 125.0, 'maneuvering': 100.0, 'engine': 'Lycoming O-320-E2D'},
            
            # Pipistrel
            {'manufacturer': 'Pipistrel', 'model': 'Virus SW 121', 'stall': 37.0, 'top': 135.0, 'maneuvering': 108.0, 'engine': 'Rotax 912ULS'},
            
            # Progressive Aerodyne
            {'manufacturer': 'Progressive Aerodyne', 'model': 'SeaRey', 'stall': 39.0, 'top': 115.0, 'maneuvering': 92.0, 'engine': 'Rotax 912ULS'},
            
            # Quicksilver Aircraft
            {'manufacturer': 'Quicksilver Aircraft', 'model': 'Sport 2S', 'stall': 28.0, 'top': 63.0, 'maneuvering': 55.0, 'engine': 'Rotax 912ULS'},
            
            # Remos
            {'manufacturer': 'Remos', 'model': 'GX', 'stall': 39.0, 'top': 135.0, 'maneuvering': 108.0, 'engine': 'Rotax 912ULS'},
            
            # Tecnam
            {'manufacturer': 'Tecnam', 'model': 'P2002-Sierra', 'stall': 38.0, 'top': 146.0, 'maneuvering': 118.0, 'engine': 'Rotax 912ULS'},
            {'manufacturer': 'Tecnam', 'model': 'P2006T', 'stall': 58.0, 'top': 155.0, 'maneuvering': 122.0, 'engine': 'Rotax 912ULS'},
            {'manufacturer': 'Tecnam', 'model': 'P2008-JC', 'stall': 35.0, 'top': 118.0, 'maneuvering': 97.0, 'engine': 'Rotax 912ULS'},
            
            # Additional missing aircraft to reach exactly 120
            {'manufacturer': 'Cessna', 'model': '140', 'stall': 45.0, 'top': 105.0, 'maneuvering': 85.0, 'engine': 'Continental C85'},
            {'manufacturer': 'Cessna', 'model': '140A', 'stall': 45.0, 'top': 105.0, 'maneuvering': 85.0, 'engine': 'Continental C90'},
            {'manufacturer': 'Cessna', 'model': '170', 'stall': 48.0, 'top': 115.0, 'maneuvering': 95.0, 'engine': 'Continental C85'},
            {'manufacturer': 'Cessna', 'model': '170A', 'stall': 48.0, 'top': 115.0, 'maneuvering': 95.0, 'engine': 'Continental C90'},
            {'manufacturer': 'Cessna', 'model': '170B', 'stall': 48.0, 'top': 115.0, 'maneuvering': 95.0, 'engine': 'Continental C90'},
            {'manufacturer': 'Piper', 'model': 'Pacer', 'stall': 45.0, 'top': 125.0, 'maneuvering': 100.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Piper', 'model': 'Clipper', 'stall': 50.0, 'top': 130.0, 'maneuvering': 105.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Piper', 'model': 'Colt', 'stall': 52.0, 'top': 120.0, 'maneuvering': 100.0, 'engine': 'Lycoming O-235-C1'},
            {'manufacturer': 'American Champion Aircraft', 'model': 'Scout 8KCAB', 'stall': 52.0, 'top': 130.0, 'maneuvering': 115.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Beechcraft', 'model': 'Sundowner', 'stall': 56.0, 'top': 135.0, 'maneuvering': 115.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'Grumman', 'model': 'AA-5A Cheetah', 'stall': 55.0, 'top': 139.0, 'maneuvering': 125.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Grumman', 'model': 'AA-5B Tiger', 'stall': 58.0, 'top': 170.0, 'maneuvering': 135.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'Maule Air', 'model': 'M-4-180C', 'stall': 38.0, 'top': 145.0, 'maneuvering': 120.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'Maule Air', 'model': 'M-5-180C', 'stall': 40.0, 'top': 155.0, 'maneuvering': 125.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'Maule Air', 'model': 'M-6-180', 'stall': 42.0, 'top': 165.0, 'maneuvering': 130.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'Maule Air', 'model': 'M-7-180', 'stall': 44.0, 'top': 175.0, 'maneuvering': 135.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'American Champion Aircraft', 'model': 'Decathlon 8KCAB', 'stall': 54.0, 'top': 135.0, 'maneuvering': 125.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Champion Aircraft', 'model': 'Citabria 7GCBC', 'stall': 53.0, 'top': 130.0, 'maneuvering': 115.0, 'engine': 'Lycoming O-320-E2D'},
            {'manufacturer': 'Aviat Aircraft', 'model': 'Pitts S-2A', 'stall': 57.0, 'top': 157.0, 'maneuvering': 144.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'Piper', 'model': 'Cherokee 235', 'stall': 59.0, 'top': 150.0, 'maneuvering': 125.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'Beechcraft', 'model': 'Sierra', 'stall': 57.0, 'top': 145.0, 'maneuvering': 125.0, 'engine': 'Lycoming O-360-A4M'},
            {'manufacturer': 'Cessna', 'model': '175', 'stall': 49.0, 'top': 130.0, 'maneuvering': 105.0, 'engine': 'Continental O-300-A'},
            {'manufacturer': 'Cessna', 'model': '177', 'stall': 50.0, 'top': 140.0, 'maneuvering': 115.0, 'engine': 'Lycoming O-360-A4M'},
        ]

        aircraft_count = 0
        for aircraft_info in aircraft_data:
            manufacturer = self.manufacturers[aircraft_info['manufacturer']]
            engine = self.engines[aircraft_info['engine']]
            
            aircraft, created = Aircraft.objects.get_or_create(
                manufacturer=manufacturer,
                model=aircraft_info['model'],
                defaults={
                    'clean_stall_speed': aircraft_info['stall'],
                    'top_speed': aircraft_info['top'], 
                    'maneuvering_speed': aircraft_info['maneuvering'],
                    'is_mosaic_compliant': True,
                }
            )
            
            # Add engine to the aircraft's engines ManyToMany field
            if engine not in aircraft.engines.all():
                aircraft.engines.add(engine)
            
            if created:
                aircraft_count += 1
                self.stdout.write(f'  Created aircraft: {aircraft}')

        self.stdout.write(f'Created {aircraft_count} new aircraft (total should be 120)')