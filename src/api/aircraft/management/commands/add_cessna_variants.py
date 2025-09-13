from django.core.management.base import BaseCommand
from aircraft.models import Aircraft, Manufacturer, Engine
from datetime import date


class Command(BaseCommand):
    help = 'Add individual Cessna 172 and 182 variant records'

    def handle(self, *args, **options):
        # Get Cessna manufacturer
        cessna = Manufacturer.objects.get(name='Cessna')
        
        # Cessna 172 variants data
        cessna_172_variants = [
            {
                'model': '172 (Original)',
                'clean_stall_speed': 50.0,
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1955, 11, 4),
                'verification_source': 'Type Certificate Data Sheet 3A12',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300-A', 'horsepower': 145}
            },
            {
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
            }
        ]

        # Cessna 182 variants data
        cessna_182_variants = [
            {
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
            }
        ]

        def create_aircraft_with_engine(variant_data):
            """Create aircraft and associated engine"""
            engine_data = variant_data.pop('engine_specs')
            
            # Create or get engine
            engine, created = Engine.objects.get_or_create(
                manufacturer=engine_data['manufacturer'],
                model=engine_data['model'],
                defaults={
                    'horsepower': engine_data['horsepower'],
                    'fuel_type': 'AVGAS',
                    'engine_type': 'PISTON'
                }
            )
            
            # Create aircraft
            aircraft = Aircraft.objects.create(
                manufacturer=cessna,
                **variant_data
            )
            
            # Associate engine
            aircraft.engines.add(engine)
            
            return aircraft

        # Create all 172 variants
        self.stdout.write('Creating Cessna 172 variants...')
        for variant in cessna_172_variants:
            aircraft = create_aircraft_with_engine(variant)
            self.stdout.write(f'  Created: {aircraft.manufacturer.name} {aircraft.model}')

        # Create all 182 variants  
        self.stdout.write('Creating Cessna 182 variants...')
        for variant in cessna_182_variants:
            aircraft = create_aircraft_with_engine(variant)
            self.stdout.write(f'  Created: {aircraft.manufacturer.name} {aircraft.model}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(cessna_172_variants)} Cessna 172 variants '
                f'and {len(cessna_182_variants)} Cessna 182 variants'
            )
        )