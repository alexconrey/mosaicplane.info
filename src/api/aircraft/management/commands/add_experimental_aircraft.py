from django.core.management.base import BaseCommand
from aircraft.models import Aircraft, Manufacturer, Engine
from datetime import date


class Command(BaseCommand):
    help = 'Add popular experimental aircraft to the database'

    def handle(self, *args, **options):
        # Create or get manufacturers
        kitfox = Manufacturer.objects.get_or_create(
            name='Kitfox Aircraft', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        rans = Manufacturer.objects.get_or_create(
            name='RANS Aircraft', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        vans = Manufacturer.objects.get_or_create(
            name="Van's Aircraft", 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        zenith = Manufacturer.objects.get_or_create(
            name='Zenith Aircraft', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        murphy = Manufacturer.objects.get_or_create(
            name='Murphy Aircraft', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        american_champion = Manufacturer.objects.get_or_create(
            name='American Champion Aircraft', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        maule = Manufacturer.objects.get_or_create(
            name='Maule Air', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        just_aircraft = Manufacturer.objects.get_or_create(
            name='Just Aircraft', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        cubcrafters = Manufacturer.objects.get_or_create(
            name='CubCrafters', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        aviat = Manufacturer.objects.get_or_create(
            name='Aviat Aircraft', 
            defaults={'is_currently_manufacturing': True}
        )[0]

        # Experimental aircraft data
        experimental_aircraft = [
            # Kitfox Series
            {
                'manufacturer': kitfox,
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
                'manufacturer': kitfox,
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
                'manufacturer': kitfox,
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
                'manufacturer': rans,
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
                'manufacturer': rans,
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
                'manufacturer': vans,
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
                'manufacturer': vans,
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
                'manufacturer': vans,
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
                'manufacturer': zenith,
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
                'manufacturer': zenith,
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
                'manufacturer': murphy,
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
                'manufacturer': american_champion,
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

            # Maule Air
            {
                'manufacturer': maule,
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
                'manufacturer': just_aircraft,
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
                'manufacturer': cubcrafters,
                'model': 'Carbon Cub EX-2',
                'clean_stall_speed': 30.0,  # Conservative estimate
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
                'manufacturer': aviat,
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
            
            # Create aircraft
            aircraft = Aircraft.objects.create(**aircraft_data)
            
            # Associate engine
            aircraft.engines.add(engine)
            
            return aircraft

        # Create all experimental aircraft
        self.stdout.write('Creating experimental aircraft...')
        for aircraft_data in experimental_aircraft:
            aircraft = create_aircraft_with_engine(aircraft_data)
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            self.stdout.write(f'  Created: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(experimental_aircraft)} experimental aircraft entries'
            )
        )