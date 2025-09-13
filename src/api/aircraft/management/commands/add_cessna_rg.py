from django.core.management.base import BaseCommand
from aircraft.models import Aircraft, Manufacturer, Engine
from datetime import date


class Command(BaseCommand):
    help = 'Add Cessna 172RG and 182RG retractable gear variants'

    def handle(self, *args, **options):
        # Get or create Cessna manufacturer
        cessna = Manufacturer.objects.get_or_create(
            name='Cessna', 
            defaults={'is_currently_manufacturing': True}
        )[0]

        # Cessna RG variants data
        cessna_rg_variants = [
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

        # Create all Cessna RG variants
        self.stdout.write('Creating Cessna RG variants...')
        created_count = 0
        for aircraft_data in cessna_rg_variants:
            aircraft, was_created = create_aircraft_with_engine(aircraft_data)
            if was_created:
                created_count += 1
            mosaic_status = "✅ Sport Pilot" if aircraft.sport_pilot_eligible else "⚠️ Private Pilot" if aircraft.is_mosaic_compliant else "❌ Not MOSAIC"
            endorsement_note = " (RG+VP endorsements required)" if aircraft.retractable_gear and aircraft.variable_pitch_prop else " (RG endorsement required)" if aircraft.retractable_gear else " (VP endorsement required)" if aircraft.variable_pitch_prop else ""
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}{endorsement_note}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(cessna_rg_variants)} Cessna RG variants ({created_count} new, {len(cessna_rg_variants) - created_count} existing)'
            )
        )