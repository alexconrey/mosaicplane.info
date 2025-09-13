from django.core.management.base import BaseCommand
from aircraft.models import Aircraft, Manufacturer, Engine
from datetime import date


class Command(BaseCommand):
    help = 'Add Mooney M20 variants to the database'

    def handle(self, *args, **options):
        # Create or get Mooney manufacturer
        mooney = Manufacturer.objects.get_or_create(
            name='Mooney International',
            defaults={'is_currently_manufacturing': True}
        )[0]

        # Mooney M20 variants data
        mooney_variants = [
            {
                'model': 'M20 (Original)',
                'clean_stall_speed': 62.0,
                'top_speed': 170.0,
                'maneuvering_speed': 140.0,
                'max_takeoff_weight': 2400,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1955, 1, 1),
                'verification_source': 'General M20 specifications research',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320', 'horsepower': 150}
            },
            {
                'model': 'M20A',
                'clean_stall_speed': 62.0,
                'top_speed': 172.0,
                'maneuvering_speed': 142.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1958, 1, 1),
                'verification_source': 'AOPA and aviation database research',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A1A', 'horsepower': 180}
            },
            {
                'model': 'M20B',
                'clean_stall_speed': 62.0,
                'top_speed': 172.0,
                'maneuvering_speed': 142.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1960, 1, 1),
                'verification_source': 'Aviation specifications research',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A1A', 'horsepower': 180}
            },
            {
                'model': 'M20C Ranger',
                'clean_stall_speed': 58.0,
                'top_speed': 175.0,
                'maneuvering_speed': 145.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1962, 1, 1),
                'verification_source': 'MooneySpace.com POH reference and AOPA',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A1D', 'horsepower': 180}
            },
            {
                'model': 'M20D Master',
                'clean_stall_speed': 58.0,
                'top_speed': 175.0,
                'maneuvering_speed': 145.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1963, 1, 1),
                'verification_source': 'Aviation specifications research',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A1D', 'horsepower': 180}
            },
            {
                'model': 'M20E Super 21',
                'clean_stall_speed': 50.0,
                'top_speed': 185.0,
                'maneuvering_speed': 150.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1964, 1, 1),
                'verification_source': 'Performance specifications research',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A1A', 'horsepower': 200}
            },
            {
                'model': 'M20F Executive 21',
                'clean_stall_speed': 50.0,
                'top_speed': 185.0,
                'maneuvering_speed': 150.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1965, 1, 1),
                'verification_source': 'Aviation specifications research',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A1A', 'horsepower': 200}
            },
            {
                'model': 'M20G Statesman',
                'clean_stall_speed': 52.0,
                'top_speed': 180.0,
                'maneuvering_speed': 148.0,
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1968, 1, 1),
                'verification_source': 'Aviation specifications research',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A1A', 'horsepower': 180}
            },
            {
                'model': 'M20J 201',
                'clean_stall_speed': 59.0,
                'top_speed': 195.0,
                'maneuvering_speed': 155.0,
                'max_takeoff_weight': 2900,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1977, 1, 1),
                'verification_source': 'AOPA aircraft fact sheets',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A3B6', 'horsepower': 200}
            },
            {
                'model': 'M20K 231',
                'clean_stall_speed': 61.0,
                'top_speed': 195.0,
                'maneuvering_speed': 155.0,
                'max_takeoff_weight': 2900,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1979, 1, 1),
                'verification_source': 'AOPA aircraft specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-360-MB1', 'horsepower': 210}
            },
            {
                'model': 'M20L PFM',
                'clean_stall_speed': 58.0,
                'top_speed': 190.0,
                'maneuvering_speed': 152.0,
                'max_takeoff_weight': 2900,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1988, 1, 1),
                'verification_source': 'Aviation specifications research',
                'engine_specs': {'manufacturer': 'Porsche', 'model': 'PFM 3200', 'horsepower': 217}
            },
            {
                'model': 'M20M TLS',
                'clean_stall_speed': 60.0,
                'top_speed': 200.0,
                'maneuvering_speed': 158.0,
                'max_takeoff_weight': 3200,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1989, 1, 1),
                'verification_source': 'Aviation specifications research',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'TIO-540-AF1A', 'horsepower': 270}
            },
            {
                'model': 'M20R Ovation',
                'clean_stall_speed': 53.0,
                'top_speed': 197.0,
                'maneuvering_speed': 160.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1994, 1, 1),
                'verification_source': 'Manufacturer and AOPA specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-550-G', 'horsepower': 280}
            },
            {
                'model': 'M20S Eagle',
                'clean_stall_speed': 55.0,
                'top_speed': 175.0,
                'maneuvering_speed': 145.0,
                'max_takeoff_weight': 2900,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1997, 1, 1),
                'verification_source': 'Aviation specifications research',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A3B6', 'horsepower': 200}
            },
            {
                'model': 'M20T Acclaim',
                'clean_stall_speed': 53.0,
                'top_speed': 242.0,
                'maneuvering_speed': 160.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(2006, 1, 1),
                'verification_source': 'Manufacturer specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-550-G', 'horsepower': 280}
            },
            {
                'model': 'M20U Ovation Ultra',
                'clean_stall_speed': 53.0,
                'top_speed': 242.0,
                'maneuvering_speed': 160.0,
                'max_takeoff_weight': 3380,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(2016, 1, 1),
                'verification_source': 'Wikipedia and manufacturer specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-550-G', 'horsepower': 280}
            },
            {
                'model': 'M20V Acclaim Ultra',
                'clean_stall_speed': 53.0,
                'top_speed': 242.0,
                'maneuvering_speed': 160.0,
                'max_takeoff_weight': 3380,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(2016, 1, 1),
                'verification_source': 'Wikipedia and manufacturer specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-550-G', 'horsepower': 280}
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
                manufacturer=mooney,
                **variant_data
            )
            
            # Associate engine
            aircraft.engines.add(engine)
            
            return aircraft

        # Create all Mooney variants
        self.stdout.write('Creating Mooney M20 variants...')
        for variant in mooney_variants:
            aircraft = create_aircraft_with_engine(variant)
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            endorsement_note = " (RG+VP endorsements required)" if aircraft.retractable_gear and aircraft.variable_pitch_prop else ""
            self.stdout.write(f'  Created: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}{endorsement_note}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(mooney_variants)} Mooney M20 variants'
            )
        )