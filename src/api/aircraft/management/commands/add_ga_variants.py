from django.core.management.base import BaseCommand
from aircraft.models import Aircraft, Manufacturer, Engine
from datetime import date


class Command(BaseCommand):
    help = 'Add additional GA aircraft variants to the database'

    def handle(self, *args, **options):
        # Get or create manufacturers
        cessna = Manufacturer.objects.get_or_create(
            name='Cessna', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        piper = Manufacturer.objects.get_or_create(
            name='Piper', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        beechcraft = Manufacturer.objects.get_or_create(
            name='Beechcraft', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        grumman = Manufacturer.objects.get_or_create(
            name='Grumman American', 
            defaults={'is_currently_manufacturing': False}
        )[0]
        
        champion = Manufacturer.objects.get_or_create(
            name='American Champion Aircraft', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        aeronca = Manufacturer.objects.get_or_create(
            name='Aeronca', 
            defaults={'is_currently_manufacturing': False}
        )[0]

        # GA aircraft variants data
        ga_aircraft = [
            # Additional Cessna variants
            {
                'manufacturer': cessna,
                'model': '140',
                'clean_stall_speed': 40.0,
                'top_speed': 125.0,
                'maneuvering_speed': 95.0,
                'max_takeoff_weight': 1450,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-85', 'horsepower': 85}
            },
            {
                'manufacturer': cessna,
                'model': '170',
                'clean_stall_speed': 43.0,
                'top_speed': 140.0,
                'maneuvering_speed': 100.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1948, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-145', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '180',
                'clean_stall_speed': 49.0,
                'top_speed': 170.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1953, 1, 1),
                'verification_source': 'AOPA aircraft specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '185',
                'clean_stall_speed': 50.0,
                'top_speed': 178.0,
                'maneuvering_speed': 145.0,
                'max_takeoff_weight': 3350,
                'seating_capacity': 6,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1961, 1, 1),
                'verification_source': 'AOPA aircraft specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-470-F', 'horsepower': 300}
            },

            # Piper Cherokee variants
            {
                'manufacturer': piper,
                'model': 'Cherokee 140',
                'clean_stall_speed': 55.0,
                'top_speed': 139.0,
                'maneuvering_speed': 125.0,
                'max_takeoff_weight': 2150,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1964, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2A', 'horsepower': 140}
            },
            {
                'manufacturer': piper,
                'model': 'Cherokee 150',
                'clean_stall_speed': 57.0,
                'top_speed': 141.0,
                'maneuvering_speed': 127.0,
                'max_takeoff_weight': 2150,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1968, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2A', 'horsepower': 150}
            },
            {
                'manufacturer': piper,
                'model': 'Cherokee 160',
                'clean_stall_speed': 57.0,
                'top_speed': 144.0,
                'maneuvering_speed': 129.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1962, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-D2A', 'horsepower': 160}
            },
            {
                'manufacturer': piper,
                'model': 'Cherokee 180',
                'clean_stall_speed': 59.0,
                'top_speed': 148.0,
                'maneuvering_speed': 132.0,
                'max_takeoff_weight': 2400,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1963, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A3A', 'horsepower': 180}
            },
            {
                'manufacturer': piper,
                'model': 'Cherokee 235',
                'clean_stall_speed': 63.0,  # Not MOSAIC eligible
                'top_speed': 160.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2900,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1963, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-540-B4B5', 'horsepower': 235}
            },

            # Piper J-3 Cub variants
            {
                'manufacturer': piper,
                'model': 'J-3 Cub',
                'clean_stall_speed': 38.0,
                'top_speed': 87.0,
                'maneuvering_speed': 70.0,
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1938, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'A-65', 'horsepower': 65}
            },
            {
                'manufacturer': piper,
                'model': 'Super Cub PA-18',
                'clean_stall_speed': 43.0,
                'top_speed': 130.0,
                'maneuvering_speed': 105.0,
                'max_takeoff_weight': 1750,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1949, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-A2B', 'horsepower': 150}
            },

            # Beechcraft variants
            {
                'manufacturer': beechcraft,
                'model': 'Musketeer',
                'clean_stall_speed': 57.0,
                'top_speed': 142.0,
                'maneuvering_speed': 120.0,
                'max_takeoff_weight': 2250,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1963, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2C', 'horsepower': 150}
            },
            {
                'manufacturer': beechcraft,
                'model': 'Sport 150',
                'clean_stall_speed': 56.0,
                'top_speed': 135.0,
                'maneuvering_speed': 115.0,
                'max_takeoff_weight': 2250,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1974, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2C', 'horsepower': 150}
            },

            # Grumman American variants
            {
                'manufacturer': grumman,
                'model': 'AA-1 Yankee',
                'clean_stall_speed': 60.0,
                'top_speed': 138.0,
                'maneuvering_speed': 125.0,
                'max_takeoff_weight': 1500,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1968, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-C2C', 'horsepower': 108}
            },
            {
                'manufacturer': grumman,
                'model': 'AA-5 Traveler',
                'clean_stall_speed': 57.0,
                'top_speed': 150.0,
                'maneuvering_speed': 125.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1972, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2G', 'horsepower': 150}
            },

            # American Champion variants
            {
                'manufacturer': champion,
                'model': 'Citabria 7ECA',
                'clean_stall_speed': 50.0,
                'top_speed': 115.0,
                'maneuvering_speed': 115.0,
                'max_takeoff_weight': 1650,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1964, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-A2B', 'horsepower': 150}
            },
            {
                'manufacturer': champion,
                'model': 'Citabria 7GCBC',
                'clean_stall_speed': 51.0,
                'top_speed': 122.0,
                'maneuvering_speed': 118.0,
                'max_takeoff_weight': 1800,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1967, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A2F', 'horsepower': 180}
            },
            {
                'manufacturer': champion,
                'model': 'Decathlon 8KCAB',
                'clean_stall_speed': 56.0,
                'top_speed': 135.0,
                'maneuvering_speed': 125.0,
                'max_takeoff_weight': 1800,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1970, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'AEIO-320-E2B', 'horsepower': 150}
            },

            # Aeronca variants
            {
                'manufacturer': aeronca,
                'model': 'Champion 7AC',
                'clean_stall_speed': 38.0,
                'top_speed': 100.0,
                'maneuvering_speed': 80.0,
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-85', 'horsepower': 85}
            },
            {
                'manufacturer': aeronca,
                'model': 'Champ 7BCM',
                'clean_stall_speed': 39.0,
                'top_speed': 105.0,
                'maneuvering_speed': 85.0,
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1947, 1, 1),
                'verification_source': 'Type Certificate Data Sheet',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-90', 'horsepower': 90}
            }
        ]

        def create_aircraft_with_engine(aircraft_data):
            """Create aircraft and associated engine"""
            engine_data = aircraft_data.pop('engine_specs')
            
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
            
            # Create or get aircraft
            aircraft, created = Aircraft.objects.get_or_create(
                manufacturer=aircraft_data['manufacturer'],
                model=aircraft_data['model'],
                defaults=aircraft_data
            )
            
            # Associate engine
            aircraft.engines.add(engine)
            
            return aircraft, created

        # Create all GA aircraft variants
        self.stdout.write('Creating GA aircraft variants...')
        created_count = 0
        for aircraft_data in ga_aircraft:
            aircraft, was_created = create_aircraft_with_engine(aircraft_data)
            if was_created:
                created_count += 1
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            endorsement_note = " (RG+VP endorsements required)" if aircraft.retractable_gear and aircraft.variable_pitch_prop else " (RG endorsement required)" if aircraft.retractable_gear else " (VP endorsement required)" if aircraft.variable_pitch_prop else ""
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}{endorsement_note}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(ga_aircraft)} GA aircraft variants ({created_count} new, {len(ga_aircraft) - created_count} existing)'
            )
        )