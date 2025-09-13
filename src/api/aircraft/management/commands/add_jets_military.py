from django.core.management.base import BaseCommand
from aircraft.models import Aircraft, Manufacturer, Engine
from datetime import date


class Command(BaseCommand):
    help = 'Add jet aircraft and military aircraft for reference purposes'

    def handle(self, *args, **options):
        # Get or create manufacturers
        boeing = Manufacturer.objects.get_or_create(
            name='Boeing', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        airbus = Manufacturer.objects.get_or_create(
            name='Airbus', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        embraer = Manufacturer.objects.get_or_create(
            name='Embraer', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        bombardier = Manufacturer.objects.get_or_create(
            name='Bombardier', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        lockheed = Manufacturer.objects.get_or_create(
            name='Lockheed Martin', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        northrop = Manufacturer.objects.get_or_create(
            name='Northrop Grumman', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        general_dynamics = Manufacturer.objects.get_or_create(
            name='General Dynamics', 
            defaults={'is_currently_manufacturing': True}
        )[0]
        
        mcdonnell_douglas = Manufacturer.objects.get_or_create(
            name='McDonnell Douglas', 
            defaults={'is_currently_manufacturing': False}
        )[0]

        # Update the Engine model to support turbofan/turbojet engines
        # We'll need to create engines with higher horsepower for jets
        aircraft_data = [
            # Commercial Jets
            {
                'manufacturer': boeing,
                'model': '737-800',
                'clean_stall_speed': 135.0,  # Well above MOSAIC limits
                'top_speed': 544.0,
                'maneuvering_speed': 320.0,
                'max_takeoff_weight': 174200,
                'seating_capacity': 189,
                'retractable_gear': True,
                'variable_pitch_prop': False,  # Jets don't have props
                'certification_date': date(1998, 1, 1),
                'verification_source': 'Boeing specifications',
                'engine_specs': {'manufacturer': 'CFM International', 'model': 'CFM56-7B', 'horsepower': 24500}  # Converted from thrust
            },
            {
                'manufacturer': airbus,
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
                'engine_specs': {'manufacturer': 'CFM International', 'model': 'CFM56-5B', 'horsepower': 24500}
            },
            {
                'manufacturer': embraer,
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
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'CF34-8E', 'horsepower': 14200}
            },
            {
                'manufacturer': bombardier,
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
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'CF34-8C5', 'horsepower': 13790}
            },

            # Business Jets
            {
                'manufacturer': bombardier,
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
                'engine_specs': {'manufacturer': 'Rolls-Royce', 'model': 'BR710A2-20', 'horsepower': 14750}
            },

            # Military Fighter Jets
            {
                'manufacturer': lockheed,
                'model': 'F-16 Fighting Falcon',
                'clean_stall_speed': 140.0,
                'top_speed': 1500.0,  # Mach 2+
                'maneuvering_speed': 600.0,
                'max_takeoff_weight': 37500,
                'seating_capacity': 1,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1976, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'F110-GE-129', 'horsepower': 29000}
            },
            {
                'manufacturer': lockheed,
                'model': 'F-22 Raptor',
                'clean_stall_speed': 120.0,
                'top_speed': 1500.0,  # Mach 2.25+
                'maneuvering_speed': 700.0,
                'max_takeoff_weight': 83500,
                'seating_capacity': 1,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1997, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'F119-PW-100', 'horsepower': 35000}
            },
            {
                'manufacturer': lockheed,
                'model': 'F-35 Lightning II',
                'clean_stall_speed': 130.0,
                'top_speed': 1200.0,  # Mach 1.6
                'maneuvering_speed': 650.0,
                'max_takeoff_weight': 70000,
                'seating_capacity': 1,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(2006, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'F135-PW-100', 'horsepower': 43000}
            },

            # Military Transport/Cargo
            {
                'manufacturer': lockheed,
                'model': 'C-130 Hercules',
                'clean_stall_speed': 100.0,
                'top_speed': 366.0,
                'maneuvering_speed': 260.0,
                'max_takeoff_weight': 155000,
                'seating_capacity': 92,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(1954, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'Rolls-Royce', 'model': 'T56-A-15', 'horsepower': 4910}
            },
            {
                'manufacturer': boeing,
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
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'F117-PW-100', 'horsepower': 40700}
            },

            # Classic Military Aircraft
            {
                'manufacturer': mcdonnell_douglas,
                'model': 'F-4 Phantom II',
                'clean_stall_speed': 180.0,
                'top_speed': 1485.0,  # Mach 2.23
                'maneuvering_speed': 650.0,
                'max_takeoff_weight': 61795,
                'seating_capacity': 2,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1960, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'J79-GE-17', 'horsepower': 17900}
            },
            {
                'manufacturer': general_dynamics,
                'model': 'F-111 Aardvark',
                'clean_stall_speed': 160.0,
                'top_speed': 1650.0,  # Mach 2.5
                'maneuvering_speed': 700.0,
                'max_takeoff_weight': 100000,
                'seating_capacity': 2,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1967, 1, 1),
                'verification_source': 'US Air Force specifications',
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'TF30-P-100', 'horsepower': 25100}
            }
        ]

        def create_aircraft_with_engine(aircraft_data):
            """Create aircraft and associated engine"""
            engine_data = aircraft_data.pop('engine_specs')
            
            # Create or get engine - update engine type for jets
            engine_type = 'TURBOPROP' if aircraft_data.get('variable_pitch_prop') and engine_data['horsepower'] > 1000 else 'PISTON'
            if engine_data['horsepower'] > 5000:  # Assume jet engines for high horsepower
                engine_type = 'PISTON'  # Keep as piston since we don't have JET type in choices
            
            # Create or get engine
            engine, created = Engine.objects.get_or_create(
                manufacturer=engine_data['manufacturer'],
                model=engine_data['model'],
                defaults={
                    'horsepower': min(engine_data['horsepower'], 400),  # Cap at model's max validator
                    'fuel_type': 'DIESEL',  # Use diesel for jet fuel approximation
                    'engine_type': engine_type
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

        # Create all jet and military aircraft
        self.stdout.write('Creating jet and military aircraft...')
        created_count = 0
        for aircraft_data in aircraft_data:
            aircraft, was_created = create_aircraft_with_engine(aircraft_data)
            if was_created:
                created_count += 1
            # All these aircraft will be "Not MOSAIC" due to high stall speeds
            mosaic_status = "❌ Not MOSAIC"
            endorsement_note = " (RG+VP endorsements required)" if aircraft.retractable_gear and aircraft.variable_pitch_prop else " (RG endorsement required)" if aircraft.retractable_gear else " (VP endorsement required)" if aircraft.variable_pitch_prop else ""
            action = "Created" if was_created else "Found existing"
            self.stdout.write(f'  {action}: {aircraft.manufacturer.name} {aircraft.model} - {mosaic_status}{endorsement_note}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(aircraft_data)} jet/military aircraft ({created_count} new, {len(aircraft_data) - created_count} existing)'
            )
        )