from django.core.management.base import BaseCommand
from aircraft.models import Aircraft, Manufacturer, Engine
from datetime import date


class Command(BaseCommand):
    help = 'Seed the database with comprehensive aircraft data from all sources'

    def handle(self, *args, **options):
        self.stdout.write('Starting comprehensive aircraft database seeding...')
        
        # Create all manufacturers
        manufacturers = self.create_manufacturers()
        
        # Create all aircraft with engines
        aircraft_count = 0
        aircraft_count += self.create_cessna_variants(manufacturers['cessna'])
        aircraft_count += self.create_ga_variants(manufacturers)
        aircraft_count += self.create_mooney_variants(manufacturers['mooney'])
        aircraft_count += self.create_cessna_rg_variants(manufacturers['cessna'])
        aircraft_count += self.create_experimental_aircraft(manufacturers)
        aircraft_count += self.create_jets_military(manufacturers)
        aircraft_count += self.create_lsa_aircraft(manufacturers)
        aircraft_count += self.create_additional_ga_aircraft(manufacturers)
        aircraft_count += self.create_additional_mooney_variants(manufacturers['mooney_intl'])
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded database with {aircraft_count} aircraft entries'
            )
        )

    def create_manufacturers(self):
        """Create or get all manufacturers"""
        manufacturers = {}
        
        manufacturer_data = [
            ('Cessna', 'cessna', True),
            ('Piper', 'piper', True),
            ('Beechcraft', 'beechcraft', True),
            ('Mooney', 'mooney', False),
            ('Cirrus', 'cirrus', True),
            ('Diamond Aircraft', 'diamond', True),
            ('Kitfox Aircraft', 'kitfox', True),
            ('RANS Aircraft', 'rans', True),
            ("Van's Aircraft", 'vans', True),
            ('Zenith Aircraft', 'zenith', True),
            ('Murphy Aircraft', 'murphy', True),
            ('American Champion Aircraft', 'american_champion', True),
            ('Maule Air', 'maule', True),
            ('Just Aircraft', 'just_aircraft', True),
            ('CubCrafters', 'cubcrafters', True),
            ('Aviat Aircraft', 'aviat', True),
            ('Boeing', 'boeing', True),
            ('Airbus', 'airbus', True),
            ('Embraer', 'embraer', True),
            ('Bombardier', 'bombardier', True),
            ('Lockheed Martin', 'lockheed', True),
            ('Northrop Grumman', 'northrop', True),
            ('General Dynamics', 'general_dynamics', True),
            ('McDonnell Douglas', 'mcdonnell_douglas', False),
            # Additional manufacturers from populate_aircraft.py and update_mosaic_aircraft.py
            ('Tecnam', 'tecnam', True),
            ('Flight Design', 'flight_design', True),
            ('Czech Sport Aircraft', 'czech_sport', True),
            ('Icon Aircraft', 'icon', True),
            ('Pipistrel', 'pipistrel', True),
            ('Progressive Aerodyne', 'progressive', True),
            ('Taylorcraft', 'taylorcraft', True),
            ('Aeronca', 'aeronca', False),
            ('Grumman American', 'grumman', False),
            ('Mooney International', 'mooney_intl', False),
        ]
        
        for name, key, is_manufacturing in manufacturer_data:
            manufacturers[key] = Manufacturer.objects.get_or_create(
                name=name,
                defaults={'is_currently_manufacturing': is_manufacturing}
            )[0]
        
        self.stdout.write(f'Created/verified {len(manufacturers)} manufacturers')
        return manufacturers

    def create_aircraft_with_engine(self, aircraft_data):
        """Helper to create aircraft and associated engine"""
        engine_data = aircraft_data.pop('engine_specs')
        
        # Create or get engine
        engine, created = Engine.objects.get_or_create(
            manufacturer=engine_data['manufacturer'],
            model=engine_data['model'],
            defaults={
                'horsepower': min(engine_data['horsepower'], 400),  # Cap at model's max validator
                'fuel_type': engine_data.get('fuel_type', 'AVGAS'),
                'engine_type': engine_data.get('engine_type', 'PISTON'),
                'thrust_pounds': engine_data.get('thrust_pounds'),
                'displacement_liters': engine_data.get('displacement_liters')
            }
        )
        
        # Create or get aircraft
        aircraft, created = Aircraft.objects.get_or_create(
            manufacturer=aircraft_data['manufacturer'],
            model=aircraft_data['model'],
            defaults=aircraft_data
        )
        
        # Associate engine
        aircraft.engines.add(engine)
        
        return aircraft, created

    def create_cessna_variants(self, cessna):
        """Create Cessna aircraft variants"""
        aircraft_data = [
            # Cessna 140, 150, 152 and other singles
            {
                'manufacturer': cessna,
                'model': '140',
                'clean_stall_speed': 45.0,
                'top_speed': 110.0,
                'maneuvering_speed': 95.0,
                'max_takeoff_weight': 1450,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A-768',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-85-12', 'horsepower': 85}
            },
            {
                'manufacturer': cessna,
                'model': '150',
                'clean_stall_speed': 47.0,
                'top_speed': 109.0,
                'maneuvering_speed': 93.0,
                'max_takeoff_weight': 1600,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1958, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A5CE',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-200-A', 'horsepower': 100}
            },
            {
                'manufacturer': cessna,
                'model': '152',
                'clean_stall_speed': 48.0,
                'top_speed': 107.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 1670,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1977, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-L2C', 'horsepower': 110}
            },
            {
                'manufacturer': cessna,
                'model': '170',
                'clean_stall_speed': 48.0,
                'top_speed': 140.0,
                'maneuvering_speed': 112.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1948, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A-768',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-145-2', 'horsepower': 145}
            },
            
            # Cessna 172 specific variants
            {
                'manufacturer': cessna,
                'model': '172 (Original)',
                'clean_stall_speed': 50.0,
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 108.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1955, 11, 4),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300-A', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172A',
                'clean_stall_speed': 50.0,
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1960, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300-C', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172B',
                'clean_stall_speed': 50.0,
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2250,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1960, 12, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172C',
                'clean_stall_speed': 50.0,
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2250,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1962, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172D',
                'clean_stall_speed': 50.0,
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1963, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172E',
                'clean_stall_speed': 50.0,
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1964, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172F',
                'clean_stall_speed': 50.0,
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1965, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172G',
                'clean_stall_speed': 50.0,
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1966, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172H',
                'clean_stall_speed': 50.0,
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1967, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172I',
                'clean_stall_speed': 48.0,
                'top_speed': 124.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1968, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2D', 'horsepower': 150}
            },
            {
                'manufacturer': cessna,
                'model': '172K',
                'clean_stall_speed': 48.0,
                'top_speed': 124.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1969, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2D', 'horsepower': 150}
            },
            {
                'manufacturer': cessna,
                'model': '172L',
                'clean_stall_speed': 48.0,
                'top_speed': 124.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1971, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2D', 'horsepower': 150}
            },
            {
                'manufacturer': cessna,
                'model': '172M',
                'clean_stall_speed': 48.0,
                'top_speed': 124.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1973, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2D', 'horsepower': 150}
            },
            {
                'manufacturer': cessna,
                'model': '172N',
                'clean_stall_speed': 50.0,
                'top_speed': 126.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1977, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-H2AD', 'horsepower': 160}
            },
            {
                'manufacturer': cessna,
                'model': '172P',
                'clean_stall_speed': 50.0,
                'top_speed': 126.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2400,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1981, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-D2J', 'horsepower': 160}
            },
            {
                'manufacturer': cessna,
                'model': '172Q Cutlass',
                'clean_stall_speed': 52.0,
                'top_speed': 135.0,
                'maneuvering_speed': 108.0,
                'max_takeoff_weight': 2550,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1983, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A4N', 'horsepower': 180}
            },
            {
                'manufacturer': cessna,
                'model': '172R',
                'clean_stall_speed': 51.0,
                'top_speed': 140.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2450,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1996, 10, 3),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-L2A', 'horsepower': 160}
            },
            {
                'manufacturer': cessna,
                'model': '172S',
                'clean_stall_speed': 48.0,
                'top_speed': 140.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2550,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1998, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-L2A', 'horsepower': 180}
            },
            
            # Cessna 182 specific variants
            {
                'manufacturer': cessna,
                'model': '182 (Original)',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2550,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1956, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182A',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2650,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1957, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182B',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2650,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1958, 8, 22),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182C',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2650,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1959, 7, 8),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182D',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2650,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1960, 6, 14),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182E',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1961, 6, 27),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-R', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182F',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1962, 8, 1),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-R', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182G',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1963, 7, 19),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-R', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182H',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1964, 9, 17),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-R', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182J',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1965, 10, 20),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-R', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182K',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1966, 8, 3),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-R', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182L',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1967, 7, 28),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-R', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182M',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1968, 9, 19),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-R', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182N',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2950,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1969, 9, 17),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182P',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2950,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1972, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182Q',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2950,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1977, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182R',
                'clean_stall_speed': 54.0,
                'top_speed': 148.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 3100,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1980, 8, 29),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-U', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182S',
                'clean_stall_speed': 54.0,
                'top_speed': 145.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 3100,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1996, 10, 3),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-540-AB1A5', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '182T',
                'clean_stall_speed': 54.0,
                'top_speed': 145.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 3100,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2001, 2, 23),
                'verification_source': 'Type Certificate Data Sheet 3A13',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-540-AB1A5', 'horsepower': 230}
            },
            
            # Other Cessna singles
            {
                'manufacturer': cessna,
                'model': '180',
                'clean_stall_speed': 56.0,
                'top_speed': 170.0,
                'maneuvering_speed': 130.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1952, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A-768',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-U', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '185',
                'clean_stall_speed': 60.0,
                'top_speed': 178.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 3350,
                'seating_capacity': 6,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1960, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A7CE',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-520-D', 'horsepower': 300}
            },
            {
                'manufacturer': cessna,
                'model': '206 Stationair',
                'clean_stall_speed': 61.0,
                'top_speed': 174.0,
                'maneuvering_speed': 130.0,
                'max_takeoff_weight': 3600,
                'seating_capacity': 6,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1964, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-520-F', 'horsepower': 285}
            }
        ]
        
        count = 0
        self.stdout.write('Creating Cessna variants...')
        for aircraft_data in aircraft_data:
            aircraft, was_created = self.create_aircraft_with_engine(aircraft_data)
            if was_created:
                count += 1
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}')
        
        return count

    def create_ga_variants(self, manufacturers):
        """Create General Aviation aircraft variants"""
        aircraft_data = [
            # Piper Aircraft
            {
                'manufacturer': manufacturers['piper'],
                'model': 'J-3 Cub',
                'clean_stall_speed': 38.0,
                'top_speed': 87.0,
                'maneuvering_speed': 70.0,
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1938, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A-691',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'A-65-8', 'horsepower': 65}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Cherokee 140 (PA-28-140)',
                'clean_stall_speed': 55.0,
                'top_speed': 141.0,
                'maneuvering_speed': 125.0,
                'max_takeoff_weight': 2150,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1964, 1, 1),
                'verification_source': 'Cherokee 140 POH, Quizlet study materials, and Pilots of America forum',
                # V-Speed data from Cherokee 140 POH and pilot resources
                'vx_speed': 70.0,  # 74 mph best angle of climb
                'vy_speed': 80.0,  # 85 mph best rate of climb
                'vs0_speed': 47.0, # 55 mph stall with flaps/gear extended
                'vg_speed': 75.0,  # Estimated best glide speed
                'vfe_speed': 98.0, # 115 mph max flap extended speed
                'vno_speed': 120.0, # 140 mph max normal operating speed
                'vne_speed': 147.0, # 171 mph never exceed speed
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2A', 'horsepower': 140}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Cherokee 150 (PA-28-150)',
                'clean_stall_speed': 57.0,
                'top_speed': 135.0,
                'maneuvering_speed': 125.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1962, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A1CE',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2A', 'horsepower': 150}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Cherokee 160 (PA-28-160)',
                'clean_stall_speed': 57.0,
                'top_speed': 139.0,
                'maneuvering_speed': 129.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1962, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A1CE',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-B2B', 'horsepower': 160}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Cherokee 180 (PA-28-180)',
                'clean_stall_speed': 57.0,
                'top_speed': 148.0,
                'maneuvering_speed': 132.0,
                'max_takeoff_weight': 2400,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1962, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A1CE',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A4A', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Colt (PA-22-108)',
                'clean_stall_speed': 43.0,
                'top_speed': 108.0,
                'maneuvering_speed': 87.0,
                'max_takeoff_weight': 1650,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1961, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A9CE',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-C1B', 'horsepower': 108}
            },
            # Beechcraft
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'Musketeer',
                'clean_stall_speed': 60.0,
                'top_speed': 150.0,
                'maneuvering_speed': 130.0,
                'max_takeoff_weight': 2450,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1966, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A2CE',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A1A', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'Sport 150',
                'clean_stall_speed': 54.0,
                'top_speed': 122.0,
                'maneuvering_speed': 107.0,
                'max_takeoff_weight': 1675,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1979, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 2A5',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-L2C', 'horsepower': 115}
            },
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'Bonanza A36',
                'clean_stall_speed': 70.0,
                'top_speed': 176.0,
                'maneuvering_speed': 152.0,
                'max_takeoff_weight': 3650,
                'seating_capacity': 6,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1970, 3, 17),
                'verification_source': 'Beechcraft Bonanza A36 POH, FAA Type Certificate A-777',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-550-N', 'horsepower': 310}
            },
            # Cirrus Aircraft
            {
                'manufacturer': manufacturers['cirrus'],
                'model': 'SR20',
                'clean_stall_speed': 60.0,
                'top_speed': 200.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 3050,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1998, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A00004CH',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-360-ES', 'horsepower': 200}
            },
            # Diamond Aircraft
            {
                'manufacturer': manufacturers['diamond'],
                'model': 'DA20-C1',
                'clean_stall_speed': 44.0,
                'top_speed': 147.0,
                'maneuvering_speed': 111.0,
                'max_takeoff_weight': 1764,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1991, 1, 1),
                'verification_source': 'EASA Type Certificate A.064',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-240-B', 'horsepower': 125}
            },
            {
                'manufacturer': manufacturers['diamond'],
                'model': 'DA40-180',
                'clean_stall_speed': 51.0,
                'top_speed': 154.0,
                'maneuvering_speed': 118.0,
                'max_takeoff_weight': 2535,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1997, 1, 1),
                'verification_source': 'EASA Type Certificate A.063',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-M1A', 'horsepower': 180}
            }
        ]
        
        count = 0
        self.stdout.write('Creating GA variants...')
        for aircraft_data in aircraft_data:
            aircraft, was_created = self.create_aircraft_with_engine(aircraft_data)
            if was_created:
                count += 1
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}')
        
        return count

    def create_mooney_variants(self, mooney):
        """Create Mooney aircraft variants"""
        aircraft_data = [
            {
                'manufacturer': mooney,
                'model': 'M20',
                'clean_stall_speed': 65.0,
                'top_speed': 174.0,
                'maneuvering_speed': 132.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1955, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A3SW',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-B2B', 'horsepower': 150}
            },
            {
                'manufacturer': mooney,
                'model': 'M20A',
                'clean_stall_speed': 65.0,
                'top_speed': 174.0,
                'maneuvering_speed': 132.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1958, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A3SW',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-B2B', 'horsepower': 150}
            },
            {
                'manufacturer': mooney,
                'model': 'M20B',
                'clean_stall_speed': 62.0,
                'top_speed': 174.0,
                'maneuvering_speed': 132.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1961, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A3SW',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-B2B', 'horsepower': 150}
            },
            {
                'manufacturer': mooney,
                'model': 'M20C',
                'clean_stall_speed': 59.0,
                'top_speed': 174.0,
                'maneuvering_speed': 132.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1962, 1, 1),
                'verification_source': 'Mooneyspace.com forum discussion and 1977 POH',
                # V-Speed data from Mooneyspace forum and POH references
                'vx_speed': 69.5,  # 80 mph best angle of climb
                'vy_speed': 91.2,  # 105 mph best rate of climb (flaps retracted)
                'vs0_speed': 49.0,  # Full flaps + gear down stall speed
                'vg_speed': 75.0,   # Estimated best glide speed
                'vfe_speed': 108.6, # 125 mph flaps extended speed (post-1968)
                'vno_speed': 152.1, # 175 mph normal operating speed (post-1969)
                'vne_speed': 173.8, # 200 mph never exceed speed (post-1969)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2A', 'horsepower': 150}
            },
            {
                'manufacturer': mooney,
                'model': 'M20D',
                'clean_stall_speed': 59.0,
                'top_speed': 178.0,
                'maneuvering_speed': 143.0,
                'max_takeoff_weight': 2740,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1963, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A3SW',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A1A', 'horsepower': 180}
            }
        ]
        
        count = 0
        self.stdout.write('Creating Mooney variants...')
        for aircraft_data in aircraft_data:
            aircraft, was_created = self.create_aircraft_with_engine(aircraft_data)
            if was_created:
                count += 1
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            endorsement_note = " (RG+VP endorsements required)" if aircraft.retractable_gear and aircraft.variable_pitch_prop else " (RG endorsement required)" if aircraft.retractable_gear else " (VP endorsement required)" if aircraft.variable_pitch_prop else ""
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}{endorsement_note}')
        
        return count

    def create_cessna_rg_variants(self, cessna):
        """Create Cessna RG variants"""
        aircraft_data = [
            {
                'manufacturer': cessna,
                'model': '172RG Cutlass',
                'clean_stall_speed': 57.0,
                'top_speed': 140.0,
                'maneuvering_speed': 113.0,
                'max_takeoff_weight': 2650,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1980, 1, 1),
                'verification_source': 'Type Certificate Data Sheet and AOPA specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-F1A6', 'horsepower': 180}
            },
            {
                'manufacturer': cessna,
                'model': '182RG Skylane RG',
                'clean_stall_speed': 56.0,
                'top_speed': 173.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 3100,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1978, 1, 1),
                'verification_source': 'Type Certificate Data Sheet and AOPA specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-540-J3C5D', 'horsepower': 235}
            }
        ]
        
        count = 0
        self.stdout.write('Creating Cessna RG variants...')
        for aircraft_data in aircraft_data:
            aircraft, was_created = self.create_aircraft_with_engine(aircraft_data)
            if was_created:
                count += 1
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            endorsement_note = " (RG+VP endorsements required)" if aircraft.retractable_gear and aircraft.variable_pitch_prop else " (RG endorsement required)" if aircraft.retractable_gear else " (VP endorsement required)" if aircraft.variable_pitch_prop else ""
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}{endorsement_note}')
        
        return count

    def create_experimental_aircraft(self, manufacturers):
        """Create experimental aircraft"""
        aircraft_data = [
            # Kitfox Series
            {
                'manufacturer': manufacturers['kitfox'],
                'model': 'Series 7 STi',
                'clean_stall_speed': 28.0,
                'top_speed': 104.0,
                'maneuvering_speed': 85.0,
                'max_takeoff_weight': 1550,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2010, 1, 1),
                'verification_source': 'Manufacturer specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['kitfox'],
                'model': 'Series 7 Super Sport',
                'clean_stall_speed': 37.0,
                'top_speed': 104.0,
                'maneuvering_speed': 85.0,
                'max_takeoff_weight': 1550,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2010, 1, 1),
                'verification_source': 'Manufacturer specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['kitfox'],
                'model': 'Series 7 Speedster',
                'clean_stall_speed': 40.0,
                'top_speed': 130.0,
                'maneuvering_speed': 100.0,
                'max_takeoff_weight': 1550,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2015, 1, 1),
                'verification_source': 'Manufacturer specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '915iS', 'horsepower': 135}
            },
            # RANS Aircraft
            {
                'manufacturer': manufacturers['rans'],
                'model': 'S-6ES Coyote II',
                'clean_stall_speed': 35.0,
                'top_speed': 83.0,
                'maneuvering_speed': 70.0,
                'max_takeoff_weight': 1030,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1995, 1, 1),
                'verification_source': 'Manufacturer specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['rans'],
                'model': 'S-7LS Courier',
                'clean_stall_speed': 29.0,
                'top_speed': 96.0,
                'maneuvering_speed': 75.0,
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2000, 1, 1),
                'verification_source': 'Manufacturer specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            # Van's Aircraft
            {
                'manufacturer': manufacturers['vans'],
                'model': 'RV-3',
                'clean_stall_speed': 53.0,
                'top_speed': 180.0,
                'maneuvering_speed': 150.0,
                'max_takeoff_weight': 1200,
                'seating_capacity': 1,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1972, 1, 1),
                'verification_source': 'Van\'s Aircraft specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320', 'horsepower': 150}
            },
            {
                'manufacturer': manufacturers['vans'],
                'model': 'RV-9A',
                'clean_stall_speed': 47.0,
                'top_speed': 145.0,
                'maneuvering_speed': 120.0,
                'max_takeoff_weight': 1750,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2000, 1, 1),
                'verification_source': 'Van\'s Aircraft specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320', 'horsepower': 160}
            },
            {
                'manufacturer': manufacturers['vans'],
                'model': 'RV-12iS',
                'clean_stall_speed': 45.0,
                'top_speed': 138.0,
                'maneuvering_speed': 110.0,
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2009, 1, 1),
                'verification_source': 'Van\'s Aircraft specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            # Zenith Aircraft
            {
                'manufacturer': manufacturers['zenith'],
                'model': 'CH-701 STOL',
                'clean_stall_speed': 25.0,
                'top_speed': 100.0,
                'maneuvering_speed': 80.0,
                'max_takeoff_weight': 1250,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1995, 1, 1),
                'verification_source': 'Zenith Aircraft specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['zenith'],
                'model': 'CH-750 STOL',
                'clean_stall_speed': 30.0,
                'top_speed': 104.0,
                'maneuvering_speed': 85.0,
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2005, 1, 1),
                'verification_source': 'Zenith Aircraft specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            # Murphy Aircraft
            {
                'manufacturer': manufacturers['murphy'],
                'model': 'Rebel',
                'clean_stall_speed': 27.0,
                'top_speed': 104.0,
                'maneuvering_speed': 85.0,
                'max_takeoff_weight': 1750,
                'seating_capacity': 3,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1990, 1, 1),
                'verification_source': 'Murphy Aircraft specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320', 'horsepower': 160}
            },
            # American Champion
            {
                'manufacturer': manufacturers['american_champion'],
                'model': 'Scout 8GCBC',
                'clean_stall_speed': 47.0,
                'top_speed': 141.0,
                'maneuvering_speed': 115.0,
                'max_takeoff_weight': 2150,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1974, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-C1G', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['american_champion'],
                'model': 'Citabria 7ECA',
                'clean_stall_speed': 51.0,
                'top_speed': 126.0,
                'maneuvering_speed': 115.0,
                'max_takeoff_weight': 1650,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1964, 8, 10),
                'verification_source': 'American Champion Aircraft specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-L2C', 'horsepower': 115}
            },
            {
                'manufacturer': manufacturers['american_champion'],
                'model': 'Citabria 7GCBC',
                'clean_stall_speed': 51.0,
                'top_speed': 130.0,
                'maneuvering_speed': 120.0,
                'max_takeoff_weight': 1800,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1970, 1, 1),
                'verification_source': 'American Champion Aircraft specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-A2B', 'horsepower': 150}
            },
            {
                'manufacturer': manufacturers['american_champion'],
                'model': 'Decathlon 8KCAB',
                'clean_stall_speed': 54.0,
                'top_speed': 135.0,
                'maneuvering_speed': 122.0,
                'max_takeoff_weight': 1800,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1970, 1, 1),
                'verification_source': 'American Champion Aircraft specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'AEIO-320-E2B', 'horsepower': 150}
            },
            # Maule Air
            {
                'manufacturer': manufacturers['maule'],
                'model': 'M-7-235 Super Rocket',
                'clean_stall_speed': 35.0,
                'top_speed': 135.0,
                'maneuvering_speed': 110.0,
                'max_takeoff_weight': 2500,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1984, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-540-J1A5', 'horsepower': 235}
            },
            # Just Aircraft
            {
                'manufacturer': manufacturers['just_aircraft'],
                'model': 'SuperSTOL',
                'clean_stall_speed': 24.0,
                'top_speed': 100.0,
                'maneuvering_speed': 80.0,
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2018, 1, 1),
                'verification_source': 'Manufacturer specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            # CubCrafters
            {
                'manufacturer': manufacturers['cubcrafters'],
                'model': 'Carbon Cub EX-2',
                'clean_stall_speed': 30.0,
                'top_speed': 130.0,
                'maneuvering_speed': 105.0,
                'max_takeoff_weight': 1865,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2012, 1, 1),
                'verification_source': 'Manufacturer specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'Titan CC340', 'horsepower': 180}
            },
            # Aviat Aircraft
            {
                'manufacturer': manufacturers['aviat'],
                'model': 'Husky A-1C-180',
                'clean_stall_speed': 46.0,
                'top_speed': 135.0,
                'maneuvering_speed': 110.0,
                'max_takeoff_weight': 2250,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1987, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A1P', 'horsepower': 180}
            }
        ]
        
        count = 0
        self.stdout.write('Creating experimental aircraft...')
        for aircraft_data in aircraft_data:
            aircraft, was_created = self.create_aircraft_with_engine(aircraft_data)
            if was_created:
                count += 1
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}')
        
        return count

    def create_jets_military(self, manufacturers):
        """Create jet and military aircraft for reference"""
        aircraft_data = [
            # Commercial Jets
            {
                'manufacturer': manufacturers['boeing'],
                'model': '737-800',
                'clean_stall_speed': 135.0,
                'top_speed': 544.0,
                'maneuvering_speed': 320.0,
                'max_takeoff_weight': 174200,
                'seating_capacity': 189,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1998, 1, 1),
                'verification_source': 'Boeing specifications',
                'engine_specs': {'manufacturer': 'CFM International', 'model': 'CFM56-7B27', 'thrust_pounds': 27300, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
            },
            {
                'manufacturer': manufacturers['airbus'],
                'model': 'A320',
                'clean_stall_speed': 126.0,
                'top_speed': 544.0,
                'maneuvering_speed': 320.0,
                'max_takeoff_weight': 172000,
                'seating_capacity': 180,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1988, 1, 1),
                'verification_source': 'Airbus specifications',
                'engine_specs': {'manufacturer': 'CFM International', 'model': 'CFM56-5B', 'horsepower': 400, 'fuel_type': 'DIESEL', 'engine_type': 'PISTON'}
            },
            {
                'manufacturer': manufacturers['embraer'],
                'model': 'E-Jet 175',
                'clean_stall_speed': 108.0,
                'top_speed': 518.0,
                'maneuvering_speed': 300.0,
                'max_takeoff_weight': 85000,
                'seating_capacity': 88,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(2004, 1, 1),
                'verification_source': 'Embraer specifications',
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'CF34-8E', 'horsepower': 400, 'fuel_type': 'DIESEL', 'engine_type': 'PISTON'}
            },
            {
                'manufacturer': manufacturers['bombardier'],
                'model': 'CRJ-700',
                'clean_stall_speed': 105.0,
                'top_speed': 518.0,
                'maneuvering_speed': 290.0,
                'max_takeoff_weight': 75000,
                'seating_capacity': 78,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(2001, 1, 1),
                'verification_source': 'Bombardier specifications',
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'CF34-8C5', 'horsepower': 400, 'fuel_type': 'DIESEL', 'engine_type': 'PISTON'}
            },
            # Business Jets
            {
                'manufacturer': manufacturers['bombardier'],
                'model': 'Global 6000',
                'clean_stall_speed': 90.0,
                'top_speed': 594.0,
                'maneuvering_speed': 340.0,
                'max_takeoff_weight': 99500,
                'seating_capacity': 17,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(2012, 1, 1),
                'verification_source': 'Bombardier specifications',
                'engine_specs': {'manufacturer': 'Rolls-Royce', 'model': 'BR710A2-20', 'horsepower': 400, 'fuel_type': 'DIESEL', 'engine_type': 'PISTON'}
            },
            # Military Fighter Jets
            {
                'manufacturer': manufacturers['lockheed'],
                'model': 'F-16 Fighting Falcon',
                'clean_stall_speed': 140.0,
                'top_speed': 1500.0,
                'maneuvering_speed': 600.0,
                'max_takeoff_weight': 37500,
                'seating_capacity': 1,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1976, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'F110-GE-129', 'horsepower': 400, 'fuel_type': 'DIESEL', 'engine_type': 'PISTON'}
            },
            {
                'manufacturer': manufacturers['lockheed'],
                'model': 'F-22 Raptor',
                'clean_stall_speed': 120.0,
                'top_speed': 1500.0,
                'maneuvering_speed': 700.0,
                'max_takeoff_weight': 83500,
                'seating_capacity': 1,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1997, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'F119-PW-100', 'horsepower': 400, 'fuel_type': 'DIESEL', 'engine_type': 'PISTON'}
            },
            {
                'manufacturer': manufacturers['lockheed'],
                'model': 'F-35 Lightning II',
                'clean_stall_speed': 130.0,
                'top_speed': 1200.0,
                'maneuvering_speed': 650.0,
                'max_takeoff_weight': 70000,
                'seating_capacity': 1,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(2006, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'F135-PW-100', 'horsepower': 400, 'fuel_type': 'DIESEL', 'engine_type': 'PISTON'}
            },
            # Military Transport/Cargo
            {
                'manufacturer': manufacturers['lockheed'],
                'model': 'C-130 Hercules',
                'clean_stall_speed': 100.0,
                'top_speed': 366.0,
                'maneuvering_speed': 260.0,
                'max_takeoff_weight': 155000,
                'seating_capacity': 92,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1954, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'Rolls-Royce', 'model': 'T56-A-15', 'thrust_pounds': 4591, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            {
                'manufacturer': manufacturers['boeing'],
                'model': 'C-17 Globemaster III',
                'clean_stall_speed': 115.0,
                'top_speed': 590.0,
                'maneuvering_speed': 350.0,
                'max_takeoff_weight': 585000,
                'seating_capacity': 154,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1991, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'F117-PW-100', 'horsepower': 400, 'fuel_type': 'DIESEL', 'engine_type': 'PISTON'}
            },
            # Classic Military Aircraft
            {
                'manufacturer': manufacturers['mcdonnell_douglas'],
                'model': 'F-4 Phantom II',
                'clean_stall_speed': 180.0,
                'top_speed': 1485.0,
                'maneuvering_speed': 650.0,
                'max_takeoff_weight': 61795,
                'seating_capacity': 2,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1960, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'J79-GE-17', 'horsepower': 400, 'fuel_type': 'DIESEL', 'engine_type': 'PISTON'}
            },
            {
                'manufacturer': manufacturers['general_dynamics'],
                'model': 'F-111 Aardvark',
                'clean_stall_speed': 160.0,
                'top_speed': 1650.0,
                'maneuvering_speed': 700.0,
                'max_takeoff_weight': 100000,
                'seating_capacity': 2,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1967, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'TF30-P-100', 'horsepower': 400, 'fuel_type': 'DIESEL', 'engine_type': 'PISTON'}
            }
        ]
        
        count = 0
        self.stdout.write('Creating jet and military aircraft...')
        for aircraft_data in aircraft_data:
            aircraft, was_created = self.create_aircraft_with_engine(aircraft_data)
            if was_created:
                count += 1
            mosaic_status = "❌ Not MOSAIC"
            endorsement_note = " (RG+VP endorsements required)" if aircraft.retractable_gear and aircraft.variable_pitch_prop else " (RG endorsement required)" if aircraft.retractable_gear else " (VP endorsement required)" if aircraft.variable_pitch_prop else ""
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}{endorsement_note}')
        
        return count

    def create_lsa_aircraft(self, manufacturers):
        """Create LSA and sport pilot eligible aircraft"""
        aircraft_data = [
            # Current LSA aircraft from populate_aircraft.py and update_mosaic_aircraft.py
            {
                'manufacturer': manufacturers['tecnam'],
                'model': 'P2008-JC',
                'clean_stall_speed': 35.0,
                'top_speed': 118.0,
                'maneuvering_speed': 97.0,
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2007, 4, 12),
                'verification_source': 'Tecnam P2008-JC POH, FAA LSA certification documents',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['flight_design'],
                'model': 'CTLS',
                'clean_stall_speed': 39.0,
                'top_speed': 120.0,
                'maneuvering_speed': 97.0,
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2006, 11, 8),
                'verification_source': 'FlightDesignUSA specifications and Flight Design CTLS POH',
                # V-Speed data from FlightDesignUSA website and estimated from LSA performance
                'vx_speed': 55.0,   # Estimated best angle of climb
                'vy_speed': 65.0,   # Estimated best rate of climb
                'vs0_speed': 39.0,  # Confirmed stall speed landing configuration
                'vg_speed': 70.0,   # Estimated best glide speed
                'vfe_speed': 85.0,  # Estimated flaps extended speed
                'vno_speed': 120.0, # Estimated normal operating speed
                'vne_speed': 145.0, # Confirmed never exceed speed
                'cruise_speed': 115.0, # Confirmed cruise speed at 75% power
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['czech_sport'],
                'model': 'SportCruiser',
                'clean_stall_speed': 39.0,
                'top_speed': 120.0,
                'maneuvering_speed': 100.0,
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2004, 7, 29),
                'verification_source': 'SportCruiser POH, Czech Sport Aircraft specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['icon'],
                'model': 'A5',
                'clean_stall_speed': 45.0,
                'top_speed': 109.0,
                'maneuvering_speed': 87.0,
                'max_takeoff_weight': 1510,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2014, 7, 23),
                'verification_source': 'Icon A5 POH, FAA Special LSA certification',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912iS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['pipistrel'],
                'model': 'Virus SW 121',
                'clean_stall_speed': 37.0,
                'top_speed': 135.0,
                'maneuvering_speed': 108.0,
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2010, 3, 16),
                'verification_source': 'Pipistrel Virus SW 121 POH, Slovenian manufacturer specifications',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['progressive'],
                'model': 'SeaRey',
                'clean_stall_speed': 39.0,
                'top_speed': 115.0,
                'maneuvering_speed': 92.0,
                'max_takeoff_weight': 1430,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2005, 9, 14),
                'verification_source': 'Progressive Aerodyne SeaRey POH, FAA LSA amphibian certification',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['taylorcraft'],
                'model': 'BC-12D',
                'clean_stall_speed': 38.0,
                'top_speed': 105.0,
                'maneuvering_speed': 87.0,
                'max_takeoff_weight': 1200,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 3, 15),
                'verification_source': 'Taylorcraft BC-12D POH (1946), Continental A-65 engine specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'A-65-8', 'horsepower': 65}
            },
            {
                'manufacturer': manufacturers['aeronca'],
                'model': '7AC Champion',
                'clean_stall_speed': 38.0,
                'top_speed': 100.0,
                'maneuvering_speed': 87.0,
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 1, 1),
                'verification_source': 'Aeronca 7AC Champion specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'A-65-8', 'horsepower': 65}
            },
            {
                'manufacturer': manufacturers['aeronca'],
                'model': '7CCM',
                'clean_stall_speed': 40.0,
                'top_speed': 105.0,
                'maneuvering_speed': 90.0,
                'max_takeoff_weight': 1300,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1947, 1, 1),
                'verification_source': 'Aeronca 7CCM specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-85-12', 'horsepower': 85}
            },
            {
                'manufacturer': manufacturers['aeronca'],
                'model': 'Champ 7BCM',
                'clean_stall_speed': 38.0,
                'top_speed': 100.0,
                'maneuvering_speed': 87.0,
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 1, 1),
                'verification_source': 'Aeronca Champ 7BCM specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'A-65-8', 'horsepower': 65}
            },
            {
                'manufacturer': manufacturers['aeronca'],
                'model': 'Champion 7AC',
                'clean_stall_speed': 38.0,
                'top_speed': 100.0,
                'maneuvering_speed': 87.0,
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 1, 1),
                'verification_source': 'Aeronca Champion 7AC specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'A-65-8', 'horsepower': 65}
            }
        ]
        
        count = 0
        self.stdout.write('Creating LSA and sport pilot aircraft...')
        for aircraft_data in aircraft_data:
            aircraft, was_created = self.create_aircraft_with_engine(aircraft_data)
            if was_created:
                count += 1
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}')
        
        return count

    def create_additional_ga_aircraft(self, manufacturers):
        """Create additional GA aircraft from update_mosaic_aircraft.py"""
        aircraft_data = [
            # Additional aircraft that exceed MOSAIC limits
            {
                'manufacturer': manufacturers['cessna'],
                'model': '172S (newer models)',
                'clean_stall_speed': 63.0,
                'top_speed': 126.0,
                'maneuvering_speed': 99.0,
                'max_takeoff_weight': 2550,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1996, 7, 15),
                'verification_source': 'Cessna 172S POH, FAA Type Certificate 3A12 (amended)',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-L2A', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['cessna'],
                'model': '182T Skylane (newer models)',
                'clean_stall_speed': 65.0,
                'top_speed': 145.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 3110,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1996, 8, 15),
                'verification_source': 'Cessna 182T POH, FAA Type Certificate 3A10 (amended)',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-540-AB1A5', 'horsepower': 235}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Cherokee 180',
                'clean_stall_speed': 63.0,
                'top_speed': 139.0,
                'maneuvering_speed': 113.0,
                'max_takeoff_weight': 2400,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1963, 5, 14),
                'verification_source': 'Piper Cherokee 180 POH, FAA Type Certificate 3A12 (amended)',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A4A', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Cherokee 235',
                'clean_stall_speed': 65.0,
                'top_speed': 145.0,
                'maneuvering_speed': 125.0,
                'max_takeoff_weight': 2900,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1963, 1, 1),
                'verification_source': 'Piper Cherokee 235 specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-540-B4B5', 'horsepower': 235}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Super Cub PA-18',
                'clean_stall_speed': 43.0,
                'top_speed': 130.0,
                'maneuvering_speed': 110.0,
                'max_takeoff_weight': 1750,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1949, 1, 1),
                'verification_source': 'Piper Super Cub specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-B2A', 'horsepower': 150}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Archer III',
                'clean_stall_speed': 64.0,
                'top_speed': 126.0,
                'maneuvering_speed': 113.0,
                'max_takeoff_weight': 2550,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1995, 8, 22),
                'verification_source': 'Piper Archer III POH, FAA Type Certificate 3A12 (amended)',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-B1E', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Saratoga',
                'clean_stall_speed': 68.0,
                'top_speed': 167.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 3600,
                'seating_capacity': 6,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1980, 4, 9),
                'verification_source': 'Piper Saratoga POH, FAA Type Certificate A24SO',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-540-K1G5', 'horsepower': 300}
            },
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'Bonanza A36',
                'clean_stall_speed': 70.0,
                'top_speed': 176.0,
                'maneuvering_speed': 152.0,
                'max_takeoff_weight': 3650,
                'seating_capacity': 6,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1970, 3, 17),
                'verification_source': 'Beechcraft Bonanza A36 POH, FAA Type Certificate A-777',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-550-N', 'horsepower': 310}
            },
            {
                'manufacturer': manufacturers['grumman'],
                'model': 'Tiger AA-5B',
                'clean_stall_speed': 60.0,
                'top_speed': 139.0,
                'maneuvering_speed': 125.0,
                'max_takeoff_weight': 2400,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1975, 1, 1),
                'verification_source': 'Grumman Tiger AA-5B specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A4K', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['grumman'],
                'model': 'AA-5 Traveler',
                'clean_stall_speed': 58.0,
                'top_speed': 135.0,
                'maneuvering_speed': 120.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1972, 1, 1),
                'verification_source': 'Grumman Traveler AA-5 specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2G', 'horsepower': 150}
            },
            {
                'manufacturer': manufacturers['grumman'],
                'model': 'AA-1 Yankee',
                'clean_stall_speed': 55.0,
                'top_speed': 125.0,
                'maneuvering_speed': 115.0,
                'max_takeoff_weight': 1500,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1970, 1, 1),
                'verification_source': 'Grumman American AA-1 Yankee specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-C2C', 'horsepower': 108}
            },
            {
                'manufacturer': manufacturers['tecnam'],
                'model': 'P2006T',
                'clean_stall_speed': 58.0,
                'top_speed': 155.0,
                'maneuvering_speed': 122.0,
                'max_takeoff_weight': 2645,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(2012, 1, 1),
                'verification_source': 'Tecnam P2006T POH',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912S', 'horsepower': 100}
            }
        ]
        
        count = 0
        self.stdout.write('Creating additional GA aircraft...')
        for aircraft_data in aircraft_data:
            aircraft, was_created = self.create_aircraft_with_engine(aircraft_data)
            if was_created:
                count += 1
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}')
        
        return count

    def create_additional_mooney_variants(self, mooney_intl):
        """Create additional Mooney variants from database"""
        aircraft_data = [
            # Mooney International variants found in database
            {
                'manufacturer': mooney_intl,
                'model': 'M20E Super 21',
                'clean_stall_speed': 61.0,
                'top_speed': 177.0,
                'maneuvering_speed': 143.0,
                'max_takeoff_weight': 2740,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1964, 1, 1),
                'verification_source': 'Mooney M20E Super 21 specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A1A', 'horsepower': 180}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20F Executive',
                'clean_stall_speed': 59.0,
                'top_speed': 180.0,
                'maneuvering_speed': 143.0,
                'max_takeoff_weight': 2740,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1965, 1, 1),
                'verification_source': 'Mooney M20F Executive specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A1A', 'horsepower': 180}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20G Statesman',
                'clean_stall_speed': 62.0,
                'top_speed': 164.0,
                'maneuvering_speed': 138.0,
                'max_takeoff_weight': 2740,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1968, 1, 1),
                'verification_source': 'Mooney M20G Statesman specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A1B6', 'horsepower': 180}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20J 201',
                'clean_stall_speed': 61.0,
                'top_speed': 201.0,
                'maneuvering_speed': 150.0,
                'max_takeoff_weight': 2900,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1976, 1, 1),
                'verification_source': 'Mooney M20J 201 specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A3B6D', 'horsepower': 200}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20K 231',
                'clean_stall_speed': 65.0,
                'top_speed': 231.0,
                'maneuvering_speed': 160.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1979, 1, 1),
                'verification_source': 'Mooney M20K 231 specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-360-LB', 'horsepower': 210}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20L PFM',
                'clean_stall_speed': 62.0,
                'top_speed': 188.0,
                'maneuvering_speed': 145.0,
                'max_takeoff_weight': 3200,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1986, 1, 1),
                'verification_source': 'Mooney M20L PFM specifications',
                'engine_specs': {'manufacturer': 'Porsche', 'model': 'PFM 3200', 'horsepower': 217}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20M TLS',
                'clean_stall_speed': 66.0,
                'top_speed': 247.0,
                'maneuvering_speed': 175.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1989, 1, 1),
                'verification_source': 'Mooney M20M TLS specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-360-MB', 'horsepower': 270}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20R Ovation',
                'clean_stall_speed': 65.0,
                'top_speed': 197.0,
                'maneuvering_speed': 152.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1994, 1, 1),
                'verification_source': 'Mooney M20R Ovation specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-550-G', 'horsepower': 280}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20S Eagle',
                'clean_stall_speed': 61.0,
                'top_speed': 175.0,
                'maneuvering_speed': 145.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1995, 1, 1),
                'verification_source': 'Mooney M20S Eagle specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A3B6', 'horsepower': 200}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20TN Acclaim',
                'clean_stall_speed': 66.0,
                'top_speed': 242.0,
                'maneuvering_speed': 175.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(2006, 1, 1),
                'verification_source': 'Mooney M20TN Acclaim specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-550-G', 'horsepower': 310}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20V Acclaim Ultra',
                'clean_stall_speed': 66.0,
                'top_speed': 252.0,
                'maneuvering_speed': 175.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(2016, 1, 1),
                'verification_source': 'Mooney M20V Acclaim Ultra specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-550-G', 'horsepower': 310}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20U Ovation Ultra',
                'clean_stall_speed': 65.0,
                'top_speed': 197.0,
                'maneuvering_speed': 152.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(2016, 1, 1),
                'verification_source': 'Mooney M20U Ovation Ultra specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-550-G', 'horsepower': 280}
            }
        ]
        
        count = 0
        self.stdout.write('Creating additional Mooney variants...')
        for aircraft_data in aircraft_data:
            aircraft, was_created = self.create_aircraft_with_engine(aircraft_data)
            if was_created:
                count += 1
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            endorsement_note = " (RG+VP endorsements required)" if aircraft.retractable_gear and aircraft.variable_pitch_prop else " (RG endorsement required)" if aircraft.retractable_gear else " (VP endorsement required)" if aircraft.variable_pitch_prop else ""
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}{endorsement_note}')
        
        return count