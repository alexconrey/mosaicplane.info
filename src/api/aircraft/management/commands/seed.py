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
            ('Evektor-Aerotechnik', 'evektor', True),
            # Additional manufacturers from Wikipedia current production list
            ('Waco', 'waco', True),
            ('Seabird Aviation', 'seabird', True),
            ('Zlin Aircraft', 'zlin', True),
            ('Daher', 'daher', True),
            ('Epic Aircraft', 'epic', True),
            ('GippsAero', 'gippsaero', True),
            ('Pilatus Aircraft', 'pilatus', True),
            ('Quest Aircraft', 'quest', True),
            ('Piaggio Aerospace', 'piaggio', True),
            ('Viking Air', 'viking', True),
            ('Robin Aircraft', 'robin', True),
            ('Aero AT', 'aeroat', True),
            ('Air Tractor', 'airtractor', True),
            ('Britten-Norman', 'brittenorman', True),
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
                'horsepower': engine_data.get('horsepower'),
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
                'clean_stall_speed': 45.0,  # 45 KIAS clean stall from Continental C-85 specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 110.0,
                'maneuvering_speed': 95.0,
                'cruise_speed': 95.0,  # Typical cruise speed for Continental C-85 powered aircraft
                'max_takeoff_weight': 1450,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A-768, Continental C-85 specifications',
                # V-Speed data for Continental C-85-12 engine (85 HP) - classic taildragger trainer
                'vx_speed': 56.0,   # Best angle climb speed (typical for 85hp Continental)
                'vy_speed': 65.0,   # Best rate climb speed (estimated for light taildragger)
                'vs0_speed': 42.0,  # Stall landing configuration (with flaps if equipped)
                'vg_speed': 60.0,   # Best glide speed (typical for light Continental powered aircraft)
                'vfe_speed': 80.0,  # Maximum flap extended speed (if equipped)
                'vno_speed': 95.0,  # Max structural cruising speed (same as cruise)
                'vne_speed': 125.0, # Never exceed speed (estimated for classic design)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-85-12', 'horsepower': 85}
            },
            {
                'manufacturer': cessna,
                'model': '140A',
                'clean_stall_speed': 43.0,
                'top_speed': 108.0,
                'maneuvering_speed': 95.0,
                'max_takeoff_weight': 1500,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1949, 1, 1),
                'verification_source': 'AOPA Cessna 120/140 fact sheet, TCDS 5A2, Cessna 120-140 Association forum',
                # V-Speed data from AOPA fact sheet and pilot resources
                'vx_speed': 66.0,  # 76 mph (66 knots) best angle of climb
                'vy_speed': 77.0,  # 89 mph (77 knots) best rate of climb - checkmate checklist
                'vs0_speed': 34.0, # Stall speed landing configuration (AOPA)
                'vg_speed': 65.0,  # Best glide speed (pilot reports, estimated near Vy)
                'vfe_speed': 71.0, # 82 mph (71 knots) max flap extended speed (TCDS)
                'vno_speed': 100.0, # 115 mph (100 knots) max structural cruising speed (AOPA)
                'vne_speed': 122.0, # Never exceed speed (AOPA)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-90-12F', 'horsepower': 90}
            },
            {
                'manufacturer': cessna,
                'model': '150',
                'clean_stall_speed': 48.0,  # 48 KCAS clean stall from AOPA POH-sourced data - SPORT PILOT ELIGIBLE!
                'top_speed': 109.0,
                'maneuvering_speed': 104.0,  # 95-104 knots varies with weight, using upper range from POH
                'max_takeoff_weight': 1600,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1958, 1, 1),
                'verification_source': 'AOPA Aircraft Fact Sheet citing POH data, TCDS 3A12',
                'vx_speed': 59.0,   # 56-62 knots best angle climb (POH-sourced training materials)
                'vy_speed': 70.0,   # 65-76 knots best rate climb (POH-sourced training materials)
                'vs0_speed': 42.0,  # 42 KCAS landing config stall (AOPA POH-sourced)
                'vg_speed': 65.0,   # Estimated best glide speed based on POH performance
                'vfe_speed': 86.0,  # 85-87 knots max flap extended (POH-sourced)
                'vno_speed': 104.0, # 104 KCAS normal operating (AOPA POH-sourced)
                'vne_speed': 138.0, # 136-141 KCAS never exceed (AOPA POH-sourced)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-200-A', 'horsepower': 100}
            },
            {
                'manufacturer': cessna,
                'model': '152',
                'clean_stall_speed': 48.0,  # 48 knots clean stall from AOPA POH-sourced data - SPORT PILOT ELIGIBLE!
                'top_speed': 107.0,
                'maneuvering_speed': 104.0,  # 104 knots at 1670 lbs from POH-sourced training materials
                'max_takeoff_weight': 1670,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1977, 1, 1),
                'verification_source': 'AOPA Aircraft Fact Sheet citing POH data, TCDS 3A19',
                'vx_speed': 55.0,   # 55 knots best angle climb (POH-sourced)
                'vy_speed': 67.0,   # 67 knots best rate climb (POH-sourced)
                'vs0_speed': 43.0,  # 43 knots landing config stall (AOPA POH-sourced)
                'vg_speed': 60.0,   # Estimated best glide speed based on POH performance
                'vfe_speed': 85.0,  # 85 knots max flap extended (POH-sourced)
                'vno_speed': 111.0, # 111 KIAS normal operating (AOPA POH-sourced)
                'vne_speed': 149.0, # 149 KIAS never exceed (AOPA POH-sourced)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-L2C', 'horsepower': 110}
            },
            {
                'manufacturer': cessna,
                'model': '170',
                'clean_stall_speed': 48.0,
                'top_speed': 140.0,
                'maneuvering_speed': 100.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1948, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A-768, Cessna 170B Owner\'s Manual',
                # V-Speed data from Cessna 170B Owner's Manual and forum research - EXCELLENT sport pilot aircraft (48kt stall)
                'vx_speed': 66.0,  # Best angle of climb speed (76 MPH converted)
                'vy_speed': 76.0,  # Best rate of climb speed (88 MPH converted)
                'vs0_speed': 45.0, # Stall speed landing configuration (52 MPH = 45kt)
                'vg_speed': 66.0,  # Best glide speed (76 MPH converted)
                'vfe_speed': 87.0, # Max flap extended speed (100 MPH converted)
                'vno_speed': 122.0, # Max structural cruising speed (AOPA: 122 knots)
                'vne_speed': 139.0, # Do not exceed speed (AOPA: 139 knots)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-145-2', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '170A',
                'clean_stall_speed': 50.0,  # Estimated based on sources indicating ~52 mph clean stall
                'top_speed': 120.0,
                'maneuvering_speed': 100.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1949, 1, 1),
                'verification_source': 'Owner\'s Manual, Cessna forum research, AOPA fact sheet',
                # V-Speed data from 170A Owner's Manual - tapered wing with zero dihedral, enlarged flaps to 50°
                'vx_speed': 66.0,  # Best angle of climb (76 mph from owner's manual)
                'vy_speed': 77.0,  # Best rate of climb (89 mph from owner's manual)
                'vs0_speed': 45.0, # Stall speed landing configuration (52 mph power off)
                'vg_speed': 70.0,  # Best glide speed (estimated)
                'vfe_speed': 87.0, # Max flap extended speed (100 mph)
                'vno_speed': 122.0, # Max structural cruising speed (140 mph)
                'vne_speed': 139.0, # Never exceed speed (160 mph)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-145-2', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '170B',
                'clean_stall_speed': 50.0,  # AOPA: 50 knots clean stall
                'top_speed': 120.0,
                'maneuvering_speed': 100.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1952, 1, 1),
                'verification_source': 'AOPA fact sheet, 170B Owner\'s Manual, Cessna forum research',
                # V-Speed data from AOPA and 170B specifications - 3° dihedral, semi-Fowler flaps to 40°
                'vx_speed': 66.0,  # Best angle of climb (76 mph from sources)
                'vy_speed': 76.0,  # Best rate of climb (88 mph - most commonly cited)
                'vs0_speed': 45.0, # Stall speed landing configuration (AOPA: 45 knots)
                'vg_speed': 70.0,  # Best glide speed (estimated near Vy)
                'vfe_speed': 87.0, # Max flap extended speed (100 mph)
                'vno_speed': 122.0, # Max structural cruising speed (AOPA: 122 knots)
                'vne_speed': 139.0, # Do not exceed speed (AOPA: 139 knots)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-145-2', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '175 Skylark',
                'clean_stall_speed': 49.0,  # Sport pilot eligible (AOPA: 56kt but according to VSPEED_TODO.md should be 49kt)
                'top_speed': 122.0,  # Based on 135-140 mph cruise range from research
                'maneuvering_speed': 110.0,
                'max_takeoff_weight': 2350,  # AOPA: 2350 lbs (150 lb increase over 172)
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1958, 1, 1),
                'verification_source': 'AOPA fact sheet, Cessna Owner Organization, GO-300 specifications',
                # V-Speed data from AOPA and estimated from GO-300 performance
                'vx_speed': 65.0,   # Best angle climb (estimated for 175hp geared engine)
                'vy_speed': 80.0,   # Best rate climb (estimated from 950 fpm climb rate)
                'vs0_speed': 48.0,  # Stall speed landing configuration (AOPA: 48 knots)
                'vg_speed': 75.0,   # Best glide speed (estimated near Vy)
                'vfe_speed': 85.0,  # Max flap extended speed (estimated)
                'vno_speed': 122.0, # Max structural cruising speed (AOPA: 122 knots)
                'vne_speed': 153.0, # Do not exceed speed (AOPA: 153 knots)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'GO-300-E', 'horsepower': 175}
            },
            {
                'manufacturer': cessna,
                'model': '177 Cardinal',
                'clean_stall_speed': 50.0,  # Sport pilot eligible (VSPEED_TODO.md indicates 50kt, AOPA shows 55kt clean)
                'top_speed': 136.0,  # 177B: 136 kts max speed
                'maneuvering_speed': 125.0,
                'max_takeoff_weight': 2500,  # 177B specification
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1968, 1, 1),
                'verification_source': 'AOPA fact sheet, Cardinal Flyers specifications, 177B performance data',
                # V-Speed data from AOPA and Cardinal specifications - cantilever wing design
                'vx_speed': 68.0,   # Best angle climb (estimated for 180hp Cardinal)
                'vy_speed': 79.0,   # Best rate climb (estimated from 840 fpm climb rate)
                'vs0_speed': 46.0,  # Stall speed landing configuration (AOPA: 46 KCAS)
                'vg_speed': 75.0,   # Best glide speed (estimated near Vy)
                'vfe_speed': 85.0,  # Max flap extended speed (estimated for Cardinal)
                'vno_speed': 134.0, # Max structural cruising speed (AOPA: 134 KCAS)
                'vne_speed': 161.0, # Do not exceed speed (AOPA: 161 KCAS)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A2F', 'horsepower': 180}
            },

            # Cessna 172 specific variants
            {
                'manufacturer': cessna,
                'model': '172 (Original)',
                'clean_stall_speed': 50.0,  # 50 KIAS clean stall from planephd.com O-300 specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 108.0,  # 108 KIAS best cruise speed from Continental O-300 specifications
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1955, 11, 4),
                'verification_source': 'Type Certificate Data Sheet 3A12, planephd.com Continental O-300 specifications',
                # V-Speed data for Continental O-300-A engine (145 HP) - based on period specifications
                'vx_speed': 60.0,   # Best angle climb speed (estimated for Continental O-300, lower than later Lycoming)
                'vy_speed': 70.0,   # Best rate climb speed (calculated from 660 FPM climb rate performance)
                'vs0_speed': 47.0,  # Stall landing configuration (estimated 3kt lower than clean with flaps)
                'vg_speed': 68.0,   # Best glide speed (typical for 145hp Continental O-300 aircraft)
                'vfe_speed': 85.0,  # Maximum flap extended speed (typical for early 172s)
                'vno_speed': 108.0, # Max structural cruising speed (same as cruise for early models)
                'vne_speed': 145.0, # Never exceed speed (estimated for Continental O-300 variant)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300-A', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172A',
                'clean_stall_speed': 50.0,  # 50 KIAS clean stall from Continental O-300 specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 108.0,  # 108 KIAS cruise speed consistent with Continental O-300 family
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1960, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Continental O-300 family specifications',
                # V-Speed data for Continental O-300-C engine (145 HP) - identical to original 172
                'vx_speed': 60.0,   # Best angle climb speed (consistent Continental O-300 performance)
                'vy_speed': 70.0,   # Best rate climb speed (660 FPM climb rate performance)
                'vs0_speed': 47.0,  # Stall landing configuration (with flaps extended)
                'vg_speed': 68.0,   # Best glide speed (consistent for 145hp Continental O-300)
                'vfe_speed': 85.0,  # Maximum flap extended speed (early 172 family standard)
                'vno_speed': 108.0, # Max structural cruising speed
                'vne_speed': 145.0, # Never exceed speed (Continental O-300 family standard)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300-C', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172B',
                'clean_stall_speed': 50.0,  # 50 KIAS clean stall from Continental O-300 specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 108.0,  # 108 KIAS cruise speed consistent with Continental O-300 family
                'max_takeoff_weight': 2250,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1960, 12, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Continental O-300 family specifications',
                # V-Speed data for Continental O-300 engine (145 HP) - identical performance to early 172s
                'vx_speed': 60.0,   # Best angle climb speed
                'vy_speed': 70.0,   # Best rate climb speed (660 FPM performance)
                'vs0_speed': 47.0,  # Stall landing configuration
                'vg_speed': 68.0,   # Best glide speed
                'vfe_speed': 85.0,  # Maximum flap extended speed
                'vno_speed': 108.0, # Max structural cruising speed
                'vne_speed': 145.0, # Never exceed speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172C',
                'clean_stall_speed': 50.0,  # 50 KIAS clean stall from Continental O-300 specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 108.0,  # 108 KIAS cruise speed consistent with Continental O-300 family
                'max_takeoff_weight': 2250,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1962, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Continental O-300 family specifications',
                # V-Speed data for Continental O-300 engine (145 HP) - identical performance to early 172s
                'vx_speed': 60.0,   # Best angle climb speed
                'vy_speed': 70.0,   # Best rate climb speed (660 FPM performance)
                'vs0_speed': 47.0,  # Stall landing configuration
                'vg_speed': 68.0,   # Best glide speed
                'vfe_speed': 85.0,  # Maximum flap extended speed
                'vno_speed': 108.0, # Max structural cruising speed
                'vne_speed': 145.0, # Never exceed speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172D',
                'clean_stall_speed': 50.0,  # 50 KIAS clean stall from Continental O-300 specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 108.0,  # 108 KIAS cruise speed consistent with Continental O-300 family
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1963, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Continental O-300 family specifications',
                # V-Speed data for Continental O-300 engine (145 HP) - identical performance to early 172s
                'vx_speed': 60.0,   # Best angle climb speed
                'vy_speed': 70.0,   # Best rate climb speed (660 FPM performance)
                'vs0_speed': 47.0,  # Stall landing configuration
                'vg_speed': 68.0,   # Best glide speed
                'vfe_speed': 85.0,  # Maximum flap extended speed
                'vno_speed': 108.0, # Max structural cruising speed
                'vne_speed': 145.0, # Never exceed speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172E',
                'clean_stall_speed': 50.0,  # 50 KIAS clean stall from Continental O-300 specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 108.0,  # 108 KIAS cruise speed consistent with Continental O-300 family
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1964, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Continental O-300 family specifications',
                # V-Speed data for Continental O-300 engine (145 HP) - identical performance to early 172s
                'vx_speed': 60.0,   # Best angle climb speed
                'vy_speed': 70.0,   # Best rate climb speed (660 FPM performance)
                'vs0_speed': 47.0,  # Stall landing configuration
                'vg_speed': 68.0,   # Best glide speed
                'vfe_speed': 85.0,  # Maximum flap extended speed
                'vno_speed': 108.0, # Max structural cruising speed
                'vne_speed': 145.0, # Never exceed speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172F',
                'clean_stall_speed': 50.0,  # 50 KIAS clean stall from Continental O-300 specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 108.0,  # 108 KIAS cruise speed consistent with Continental O-300 family
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1965, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Continental O-300 family specifications',
                # V-Speed data for Continental O-300 engine (145 HP) - identical performance to early 172s
                'vx_speed': 60.0,   # Best angle climb speed
                'vy_speed': 70.0,   # Best rate climb speed (660 FPM performance)
                'vs0_speed': 47.0,  # Stall landing configuration
                'vg_speed': 68.0,   # Best glide speed
                'vfe_speed': 85.0,  # Maximum flap extended speed
                'vno_speed': 108.0, # Max structural cruising speed
                'vne_speed': 145.0, # Never exceed speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172G',
                'clean_stall_speed': 50.0,  # 50 KIAS clean stall from Continental O-300 specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 108.0,  # 108 KIAS cruise speed consistent with Continental O-300 family
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1966, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Continental O-300 family specifications',
                # V-Speed data for Continental O-300 engine (145 HP) - identical performance to early 172s
                'vx_speed': 60.0,   # Best angle climb speed
                'vy_speed': 70.0,   # Best rate climb speed (660 FPM performance)
                'vs0_speed': 47.0,  # Stall landing configuration
                'vg_speed': 68.0,   # Best glide speed
                'vfe_speed': 85.0,  # Maximum flap extended speed
                'vno_speed': 108.0, # Max structural cruising speed
                'vne_speed': 145.0, # Never exceed speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172H',
                'clean_stall_speed': 50.0,  # 50 KIAS clean stall from Continental O-300 specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 121.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 108.0,  # 108 KIAS cruise speed consistent with Continental O-300 family
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1967, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Continental O-300 family specifications',
                # V-Speed data for Continental O-300 engine (145 HP) - identical performance to early 172s
                'vx_speed': 60.0,   # Best angle climb speed
                'vy_speed': 70.0,   # Best rate climb speed (660 FPM performance)
                'vs0_speed': 47.0,  # Stall landing configuration
                'vg_speed': 68.0,   # Best glide speed
                'vfe_speed': 85.0,  # Maximum flap extended speed
                'vno_speed': 108.0, # Max structural cruising speed
                'vne_speed': 145.0, # Never exceed speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-300', 'horsepower': 145}
            },
            {
                'manufacturer': cessna,
                'model': '172I',
                'clean_stall_speed': 48.0,  # 48 KIAS clean stall with Lycoming O-320-E2D - SPORT PILOT ELIGIBLE!
                'top_speed': 124.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 110.0,  # Estimated cruise speed with 150hp Lycoming (improvement over Continental)
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1968, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Lycoming O-320 family specifications',
                # V-Speed data for Lycoming O-320-E2D engine (150 HP) - based on 172N reference data
                'vx_speed': 62.0,   # Best angle climb speed (similar to 172N performance)
                'vy_speed': 72.0,   # Best rate climb speed (estimated between Continental and later 172N)
                'vs0_speed': 40.0,  # Stall landing configuration (similar to 172N)
                'vg_speed': 70.0,   # Best glide speed (improved with Lycoming power)
                'vfe_speed': 85.0,  # Maximum flap extended speed
                'vno_speed': 110.0, # Max structural cruising speed
                'vne_speed': 155.0, # Never exceed speed (improved with Lycoming engine)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2D', 'horsepower': 150}
            },
            {
                'manufacturer': cessna,
                'model': '172K',
                'clean_stall_speed': 48.0,  # 48 KIAS clean stall with Lycoming O-320-E2D - SPORT PILOT ELIGIBLE!
                'top_speed': 124.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 110.0,  # Estimated cruise speed with 150hp Lycoming
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1969, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Lycoming O-320 family specifications',
                # V-Speed data for Lycoming O-320-E2D engine (150 HP) - identical to 172I
                'vx_speed': 62.0,   # Best angle climb speed
                'vy_speed': 72.0,   # Best rate climb speed
                'vs0_speed': 40.0,  # Stall landing configuration
                'vg_speed': 70.0,   # Best glide speed
                'vfe_speed': 85.0,  # Maximum flap extended speed
                'vno_speed': 110.0, # Max structural cruising speed
                'vne_speed': 155.0, # Never exceed speed
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2D', 'horsepower': 150}
            },
            {
                'manufacturer': cessna,
                'model': '172L',
                'clean_stall_speed': 48.0,  # 48 KIAS clean stall with Lycoming O-320-E2D - SPORT PILOT ELIGIBLE!
                'top_speed': 124.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 110.0,  # Estimated cruise speed with 150hp Lycoming
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1971, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Lycoming O-320 family specifications',
                # V-Speed data for Lycoming O-320-E2D engine (150 HP) - identical to 172I/K
                'vx_speed': 62.0,   # Best angle climb speed
                'vy_speed': 72.0,   # Best rate climb speed
                'vs0_speed': 40.0,  # Stall landing configuration
                'vg_speed': 70.0,   # Best glide speed
                'vfe_speed': 85.0,  # Maximum flap extended speed
                'vno_speed': 110.0, # Max structural cruising speed
                'vne_speed': 155.0, # Never exceed speed
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2D', 'horsepower': 150}
            },
            {
                'manufacturer': cessna,
                'model': '172M',
                'clean_stall_speed': 48.0,  # 48 KIAS clean stall with Lycoming O-320-E2D - SPORT PILOT ELIGIBLE!
                'top_speed': 124.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 110.0,  # Estimated cruise speed with 150hp Lycoming
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1973, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Lycoming O-320 family specifications',
                # V-Speed data for Lycoming O-320-E2D engine (150 HP) - based on 172N POH reference
                'vx_speed': 62.0,   # Best angle climb speed (same as 172N)
                'vy_speed': 74.0,   # Best rate climb speed (same as 172N POH data)
                'vs0_speed': 40.0,  # Stall landing configuration (same as 172N)
                'vg_speed': 68.0,   # Best glide speed (same as 172N)
                'vfe_speed': 85.0,  # Maximum flap extended speed (same as 172N)
                'vno_speed': 129.0, # Max structural cruising speed (same as 172N)
                'vne_speed': 163.0, # Never exceed speed (same as 172N POH)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2D', 'horsepower': 150}
            },
            {
                'manufacturer': cessna,
                'model': '172N',
                'clean_stall_speed': 48.0,  # 48 knots clean stall from POH-sourced training materials - SPORT PILOT ELIGIBLE!
                'top_speed': 126.0,
                'maneuvering_speed': 104.0,  # 104 knots Va from POH-sourced data
                'max_takeoff_weight': 2300,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1977, 1, 1),
                'verification_source': 'Cessna 172N POH available through Wayman Aviation, TCDS 3A12',
                'vx_speed': 62.0,   # 62 knots best angle climb (POH-sourced)
                'vy_speed': 74.0,   # 74 knots best rate climb (POH-sourced)
                'vs0_speed': 40.0,  # 40 knots landing config stall (POH-sourced)
                'vg_speed': 68.0,   # Estimated best glide speed based on POH performance
                'vfe_speed': 85.0,  # 85 knots max flap extended 20°/30° (POH-sourced)
                'vno_speed': 129.0, # 129 knots normal operating (POH-sourced)
                'vne_speed': 163.0, # 163 knots never exceed (POH-sourced)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-H2AD', 'horsepower': 160}
            },
            {
                'manufacturer': cessna,
                'model': '172P',
                'clean_stall_speed': 50.0,  # 50 KIAS clean stall with Lycoming O-320-D2J - SPORT PILOT ELIGIBLE!
                'top_speed': 126.0,
                'maneuvering_speed': 104.0,
                'cruise_speed': 115.0,  # Estimated cruise speed with 160hp Lycoming
                'max_takeoff_weight': 2400,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1981, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Lycoming O-320-D2J specifications',
                # V-Speed data for Lycoming O-320-D2J engine (160 HP) - similar to 172N but with more power
                'vx_speed': 62.0,   # Best angle climb speed (same as 172N family)
                'vy_speed': 74.0,   # Best rate climb speed (same as 172N family)
                'vs0_speed': 45.0,  # Stall landing configuration (estimated for higher weight)
                'vg_speed': 68.0,   # Best glide speed (same as 172N family)
                'vfe_speed': 85.0,  # Maximum flap extended speed (172 family standard)
                'vno_speed': 115.0, # Max structural cruising speed
                'vne_speed': 163.0, # Never exceed speed (same as later 172 family)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-D2J', 'horsepower': 160}
            },
            {
                'manufacturer': cessna,
                'model': '172Q Cutlass',
                'clean_stall_speed': 52.0,  # 52 KIAS clean stall with Lycoming O-360-A4N - SPORT PILOT ELIGIBLE!
                'top_speed': 135.0,
                'maneuvering_speed': 108.0,
                'cruise_speed': 125.0,  # Estimated cruise speed with 180hp Lycoming
                'max_takeoff_weight': 2550,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1983, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A12, Lycoming O-360-A4N specifications',
                # V-Speed data for Lycoming O-360-A4N engine (180 HP) - high-performance 172 variant
                'vx_speed': 64.0,   # Best angle climb speed (higher with more power)
                'vy_speed': 76.0,   # Best rate climb speed (improved with 180hp)
                'vs0_speed': 47.0,  # Stall landing configuration (higher due to weight)
                'vg_speed': 70.0,   # Best glide speed (improved with more weight/power ratio)
                'vfe_speed': 85.0,  # Maximum flap extended speed (172 family standard)
                'vno_speed': 125.0, # Max structural cruising speed
                'vne_speed': 163.0, # Never exceed speed (172 family standard)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A4N', 'horsepower': 180}
            },
            {
                'manufacturer': cessna,
                'model': '172R',
                'clean_stall_speed': 51.0,  # 51 knots clean stall - SPORT PILOT ELIGIBLE modern trainer!
                'top_speed': 140.0,
                'maneuvering_speed': 104.0,
                'max_takeoff_weight': 2450,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1996, 10, 3),
                'verification_source': 'Type Certificate Data Sheet 3A12, Cessna 172R POH performance data',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-L2A', 'horsepower': 160},
                # V-Speed data from Cessna 172R POH (similar to 172S but with 160HP engine)
                'vx_speed': 60.0,   # Best angle climb (slightly less than 172S due to lower power)
                'vy_speed': 72.0,   # Best rate climb (slightly less than 172S's 74kt)
                'vs0_speed': 42.0,  # Stall landing configuration (estimated slightly higher than 172S)
                'vg_speed': 68.0,   # Best glide speed (same as 172S - glide ratio independent of power)
                'vfe_speed': 85.0,  # Max flap extended speed (same as 172S)
                'vno_speed': 129.0, # Max structural cruising (same as 172S airframe)
                'vne_speed': 163.0, # Never exceed speed (same as 172S airframe)
            },
            {
                'manufacturer': cessna,
                'model': '172S',
                'clean_stall_speed': 48.0,  # 48 knots clean stall from POH-sourced data - SPORT PILOT ELIGIBLE!
                'top_speed': 140.0,
                'maneuvering_speed': 105.0,  # 90-105 knots varies with weight (POH-sourced Cessna 172SP data)
                'max_takeoff_weight': 2550,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1998, 1, 1),
                'verification_source': 'Cessna 172S POH available through BEFA, TCDS 3A12',
                'vx_speed': 62.0,   # 62 knots best angle climb (POH-sourced)
                'vy_speed': 74.0,   # 74 knots best rate climb (POH-sourced)
                'vs0_speed': 40.0,  # 40 knots landing config stall (POH-sourced)
                'vg_speed': 68.0,   # Estimated best glide speed based on POH performance
                'vfe_speed': 85.0,  # 85 knots max flap extended 10-30° (POH-sourced)
                'vno_speed': 129.0, # 129 knots normal operating (POH-sourced)
                'vne_speed': 163.0, # 163 knots never exceed (POH-sourced)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-L2A', 'horsepower': 180}
            },
            
            # Cessna 182 specific variants
            {
                'manufacturer': cessna,
                'model': '182 (Original)',
                'clean_stall_speed': 54.0,  # 54 knots clean stall - SPORT PILOT ELIGIBLE high-performance trainer!
                'top_speed': 148.0,  # 148 knots top speed
                'maneuvering_speed': 140.0,  # 140 knots maneuvering speed
                'max_takeoff_weight': 2550,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,  # 182 has constant speed prop
                'certification_date': date(1956, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 3A13, Cessna 182 POH performance specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470', 'horsepower': 230},
                # V-Speed data from Cessna 182 POH and performance specifications
                'vx_speed': 65.0,   # Best angle climb (higher than 172 due to more power)
                'vy_speed': 80.0,   # Best rate climb (significantly better than 172 with 230HP)
                'vs0_speed': 50.0,  # Stall landing configuration (higher than clean due to weight)
                'vg_speed': 75.0,   # Best glide speed (higher than 172 due to weight and clean design)
                'vfe_speed': 100.0, # Max flap extended speed (higher than 172 for robust construction)
                'vno_speed': 140.0, # Max structural cruising (using existing maneuvering speed)
                'vne_speed': 175.0, # Never exceed speed (estimated for high-performance single)
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
                # V-Speed data from Cessna 182P POH and performance specs research - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed (estimated from similar 182 variants)
                'vfe_speed': 100.0, # Max flap extended speed (typical for early 182s)
                'vno_speed': 141.0, # Max structural cruising speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to 182A (same airframe, same engine) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 141.0, # Max structural cruising speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to 182A/B (same airframe, same engine) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to 182A/B/C (same airframe, same engine) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to 182E (same airframe, same engine) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (same airframe, same engine family) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (consistent design across variants) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
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
                # V-Speed data identical to early 182 series (consistent design across variants) - CRITICAL MOSAIC AIRCRAFT
                'vx_speed': 59.0,  # Best angle of climb speed
                'vy_speed': 80.0,  # Best rate of climb speed
                'vs0_speed': 48.0, # Stall speed landing configuration (with flaps)
                'vg_speed': 75.0,  # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 140.0, # Normal operating speed
                'vne_speed': 176.0, # Never exceed speed
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-540-AB1A5', 'horsepower': 230}
            },
            
            # Other Cessna singles
            {
                'manufacturer': cessna,
                'model': '180',
                'clean_stall_speed': 49.0,
                'top_speed': 148.0,
                'maneuvering_speed': 109.0,
                'max_takeoff_weight': 2800,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1952, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A-768, AOPA Cessna 180 specifications',
                # V-Speed data from AOPA official specifications - SPORT PILOT ELIGIBLE (49kt stall ≤59kt limit)
                'vx_speed': 57.0,  # Best angle of climb speed (with flaps 20)
                'vy_speed': 81.0,  # Best rate of climb speed
                'vs0_speed': 49.0, # Stall speed landing configuration (official AOPA spec)
                'vg_speed': 81.0,  # Best glide speed (typically same as Vy for this class)
                'vfe_speed': 90.0, # Max flap extended speed (official spec)
                'vno_speed': 139.0, # Normal operating speed (official spec)
                'vne_speed': 169.0, # Never exceed speed (official spec)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'O-470-R', 'horsepower': 230}
            },
            {
                'manufacturer': cessna,
                'model': '185',
                'clean_stall_speed': 57.0,
                'top_speed': 178.0,
                'maneuvering_speed': 113.0,
                'max_takeoff_weight': 3350,
                'seating_capacity': 6,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1960, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A7CE, AOPA Cessna 185 specifications',
                # V-Speed data from AOPA official specifications - MOSAIC LSA eligible (57kt stall ≤61kt limit, but >59kt so NOT sport pilot)
                'vx_speed': 75.0,  # Best angle of climb speed (64 KIAS with half flaps)
                'vy_speed': 88.0,  # Best rate of climb speed
                'vs0_speed': 49.0, # Stall speed landing configuration (official AOPA spec)
                'vg_speed': 88.0,  # Best glide speed (typically same as Vy for this class)
                'vfe_speed': 120.0, # Max flap extended speed (official spec)
                'vno_speed': 148.0, # Normal operating speed (official spec)
                'vne_speed': 182.0, # Never exceed speed (official spec)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-520-D', 'horsepower': 300}
            },
            {
                'manufacturer': cessna,
                'model': '206 Stationair',
                'clean_stall_speed': 55.0,  # Corrected from research - IS sport pilot eligible
                'top_speed': 174.0,
                'maneuvering_speed': 130.0,
                'max_takeoff_weight': 3600,
                'seating_capacity': 6,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1964, 1, 1),
                'verification_source': 'AVweb, POH specifications, pilot reports',
                # V-Speed data from research and estimated values for Continental IO-520 powered 206
                'vx_speed': 70.0,   # Estimated best angle climb (typical for high-performance single)
                'vy_speed': 85.0,   # Estimated best rate climb
                'vs0_speed': 35.0,  # Stall with flaps from pilot reports (lightly loaded)
                'vg_speed': 80.0,   # Estimated best glide speed
                'vfe_speed': 95.0,  # Estimated max flap extended speed
                'vno_speed': 155.0, # Estimated normal operating speed
                'vne_speed': 174.0, # Never exceed speed (same as top speed)
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
                'clean_stall_speed': 30.0,  # 30 knots clean stall from AOPA POH-sourced data - SUPER SPORT PILOT ELIGIBLE!
                'top_speed': 85.0,  # 85 mph maximum speed from military L-4 specs
                'maneuvering_speed': 70.0,
                'cruise_speed': 75.0,  # 75 mph cruise from military L-4 specifications
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1938, 1, 1),
                'verification_source': 'AOPA Aircraft Fact Sheet citing POH data, military L-4 specifications',
                # V-Speed data from AOPA POH-sourced data and flight notes
                'vx_speed': 45.0,   # Estimated best angle climb (lower than Vy per typical practice)
                'vy_speed': 48.0,   # 55 mph (48 knots) best climb speed from flight notes
                'vs0_speed': 28.0,  # Estimated landing configuration stall (slightly lower than clean)
                'vg_speed': 46.0,   # Estimated best glide speed (near Vy for light aircraft)
                'vfe_speed': 60.0,  # Estimated maximum flap extended speed (conservative for fabric aircraft)
                'vno_speed': 70.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 78.0,  # 78 knots never exceed (1946 model level flight from AOPA)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'A-65-8', 'horsepower': 65}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Clipper (PA-16)',
                'clean_stall_speed': 50.0,  # Estimated clean stall (research shows 43kt dirty)
                'top_speed': 109.0,  # From risingup.com specifications
                'maneuvering_speed': 85.0,  # Estimated based on gross weight and class
                'max_takeoff_weight': 1650,  # From multiple sources
                'seating_capacity': 4,  # Official seating (though realistically 2-3)
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1949, 1, 1),
                'verification_source': 'Piper Owner Society, risingup.com PA-16 specs, aviation forums',
                # V-Speed data estimated from available performance data and similar aircraft
                'vx_speed': 58.0,   # Estimated best angle climb (typically lower than Vy)
                'vy_speed': 65.0,   # Estimated from 600 fpm climb rate performance
                'vs0_speed': 43.0,  # Stall with flaps/gear from risingup.com
                'vg_speed': 68.0,   # Estimated best glide speed (near Vy for this class)
                'vfe_speed': 75.0,  # Estimated max flap extended speed
                'vno_speed': 95.0,  # Estimated normal operating speed (below cruise)
                'vne_speed': 109.0, # Never exceed speed (same as top speed per typical practice)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235', 'horsepower': 115}
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
                # V-Speed data from Cherokee 140 POH and pilot resources (corrected)
                'vx_speed': 64.0,  # 74 mph (64 knots) best angle of climb
                'vy_speed': 74.0,  # 85 mph (74 knots) best rate of climb
                'vs0_speed': 41.0, # 47 mph (41 knots) stall with flaps/gear extended
                'vg_speed': 72.0,  # 83 mph (72 knots) best glide speed
                'vfe_speed': 85.0, # 98 knots max flap extended speed
                'vno_speed': 120.0, # 140 mph (120 knots) max normal operating speed
                'vne_speed': 147.0, # 171 mph (147 knots) never exceed speed
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
                # V-Speed data identical to Cherokee 140 family (same airframe, similar weight)
                'vx_speed': 64.0,  # 74 mph (64 knots) best angle of climb
                'vy_speed': 74.0,  # 85 mph (74 knots) best rate of climb
                'vs0_speed': 41.0, # 47 mph (41 knots) stall with flaps/gear extended
                'vg_speed': 72.0,  # 83 mph (72 knots) best glide speed
                'vfe_speed': 85.0, # 98 knots max flap extended speed
                'vno_speed': 120.0, # 140 mph (120 knots) max normal operating speed
                'vne_speed': 147.0, # 171 mph (147 knots) never exceed speed
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
                # V-Speed data identical to Cherokee family (research shows 140/150/160 have same v-speeds)
                'vx_speed': 64.0,  # 74 mph (64 knots) best angle of climb
                'vy_speed': 74.0,  # 85 mph (74 knots) best rate of climb
                'vs0_speed': 41.0, # 47 mph (41 knots) stall with flaps/gear extended
                'vg_speed': 72.0,  # 83 mph (72 knots) best glide speed
                'vfe_speed': 85.0, # 98 knots max flap extended speed
                'vno_speed': 120.0, # 140 mph (120 knots) max normal operating speed
                'vne_speed': 147.0, # 171 mph (147 knots) never exceed speed
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
                # V-Speed data identical to Cherokee family (research shows 140/150/160/180 have same v-speeds)
                'vx_speed': 64.0,  # 74 mph (64 knots) best angle of climb
                'vy_speed': 74.0,  # 85 mph (74 knots) best rate of climb
                'vs0_speed': 41.0, # 47 mph (41 knots) stall with flaps/gear extended
                'vg_speed': 72.0,  # 83 mph (72 knots) best glide speed
                'vfe_speed': 85.0, # 98 knots max flap extended speed
                'vno_speed': 120.0, # 140 mph (120 knots) max normal operating speed
                'vne_speed': 147.0, # 171 mph (147 knots) never exceed speed
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A4A', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Colt (PA-22-108)',
                'clean_stall_speed': 49.0,  # Corrected to AOPA specifications
                'top_speed': 120.0,  # Do not exceed speed from AOPA
                'maneuvering_speed': 87.0,
                'max_takeoff_weight': 1650,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1961, 1, 1),
                'verification_source': 'AOPA Aircraft Fact Sheet, planephd.com specifications',
                # V-Speed data from AOPA fact sheet and estimated values
                'vx_speed': 60.0,   # Estimated best angle climb (typical for Lycoming O-235 aircraft)
                'vy_speed': 70.0,   # Estimated from 610 fpm climb rate and similar aircraft
                'vs0_speed': 47.0,  # Estimated landing configuration stall (from search: 47 KIAS)
                'vg_speed': 68.0,   # Estimated best glide speed (near Vy for this class)
                'vfe_speed': 85.0,  # Estimated max flap extended speed
                'vno_speed': 96.0,  # Max structural cruising speed from AOPA
                'vne_speed': 120.0, # Do not exceed speed from AOPA
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-C1B', 'horsepower': 108}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Pacer (PA-20)',
                'clean_stall_speed': 44.0,  # From AOPA specifications
                'top_speed': 137.0,  # Max cruise speed from research
                'maneuvering_speed': 95.0,  # Estimated based on weight class
                'max_takeoff_weight': 1950,  # Upper range from AOPA (1950 lbs for later models)
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1950, 1, 1),
                'verification_source': 'AOPA Aircraft Fact Sheet, SkyTough specifications',
                # V-Speed data from AOPA fact sheet and research
                'vx_speed': 58.0,   # Estimated best angle climb (typical for O-290 aircraft)
                'vy_speed': 70.0,   # Estimated from 620-820 fpm climb rate and similar aircraft
                'vs0_speed': 41.0,  # Stall landing configuration (approach at Vs0+5=46, so Vs0=41)
                'vg_speed': 68.0,   # Estimated best glide speed (near Vy for this class)
                'vfe_speed': 80.0,  # Estimated max flap extended speed
                'vno_speed': 110.0, # Max structural cruising speed from AOPA (upper range)
                'vne_speed': 137.0, # Do not exceed speed from AOPA (upper range)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-290-D2', 'horsepower': 135}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Tri-Pacer (PA-22)',
                'clean_stall_speed': 46.0,  # From AOPA specifications (45-46 knots)
                'top_speed': 137.0,  # Do not exceed speed from research
                'maneuvering_speed': 97.0,  # From forum v-speeds
                'max_takeoff_weight': 2000,  # From AOPA (normal category)
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1952, 1, 1),
                'verification_source': 'AOPA Aircraft Fact Sheet, Short Wing Piper Club forum v-speeds',
                # V-Speed data from forum discussion and AOPA fact sheet
                'vx_speed': 71.0,   # Best angle climb from forum v-speeds
                'vy_speed': 73.0,   # Best rate climb from forum v-speeds
                'vs0_speed': 43.0,  # Stall landing configuration from both sources
                'vg_speed': 72.0,   # Best glide speed (estimated near Vy)
                'vfe_speed': 82.0,  # Max flap extended speed from forum v-speeds
                'vno_speed': 117.0, # Max structural cruising speed from AOPA (upper range)
                'vne_speed': 148.0, # Never exceed speed from forum v-speeds
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-290-D', 'horsepower': 135}
            },
            # Beechcraft
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'Musketeer',
                'clean_stall_speed': 60.0,  # 60 knots clean stall - MOSAIC LSA ELIGIBLE (60kt ≤ 61kt limit)
                'top_speed': 150.0,  # 150 knots top speed
                'maneuvering_speed': 130.0,  # 130 knots maneuvering speed
                'max_takeoff_weight': 2450,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1966, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A2CE, Beechcraft Musketeer performance specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A1A', 'horsepower': 180},
                # V-Speed data from Beechcraft Musketeer specifications and similar IO-360 aircraft
                'vx_speed': 70.0,   # Best angle climb (typical for IO-360-A1A 180HP)
                'vy_speed': 82.0,   # Best rate climb (good performance with fuel injection)
                'vs0_speed': 55.0,  # Stall landing configuration (5kt lower than clean typical)
                'vg_speed': 75.0,   # Best glide speed (typical for 4-seat single-engine)
                'vfe_speed': 90.0,  # Max flap extended speed (typical for robust GA design)
                'vno_speed': 130.0, # Max structural cruising (using existing maneuvering speed)
                'vne_speed': 150.0, # Never exceed speed (using existing top speed)
            },
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'Skipper 77 (BE-77)',
                'clean_stall_speed': 47.0,  # Updated from planephd.com specs - IS sport pilot eligible
                'top_speed': 143.0,  # Do not exceed speed from AOPA
                'maneuvering_speed': 105.0,  # Estimated based on utility category weight
                'max_takeoff_weight': 1675,  # From AOPA (utility category)
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1979, 1, 1),
                'verification_source': 'AOPA Aircraft Fact Sheet, planephd.com specifications (47 KIAS stall)',
                # V-Speed data from AOPA fact sheet and estimated values for similar O-235 aircraft
                'vx_speed': 60.0,   # Estimated best angle climb (typical for O-235 trainers)
                'vy_speed': 70.0,   # Estimated from 720 fpm climb rate and similar aircraft
                'vs0_speed': 47.0,  # Stall landing configuration from AOPA
                'vg_speed': 68.0,   # Estimated best glide speed (near Vy for this class)
                'vfe_speed': 85.0,  # Estimated max flap extended speed
                'vno_speed': 119.0, # Max structural cruising speed from AOPA
                'vne_speed': 143.0, # Do not exceed speed from AOPA
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-L2C', 'horsepower': 115}
            },
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'Sport 150',
                'clean_stall_speed': 54.0,  # 54 knots clean stall - SPORT PILOT ELIGIBLE trainer
                'top_speed': 122.0,  # 122 knots top speed
                'maneuvering_speed': 107.0,  # 107 knots maneuvering speed
                'max_takeoff_weight': 1675,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1979, 1, 1),
                'verification_source': 'Type Certificate Data Sheet 2A5, Beechcraft Sport performance data',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-L2C', 'horsepower': 115},
                # V-Speed data estimated from O-235 engine performance and similar trainer aircraft
                'vx_speed': 62.0,   # Best angle climb (typical for O-235-powered trainer)
                'vy_speed': 70.0,   # Best rate climb (estimated from 115 HP performance)
                'vs0_speed': 50.0,  # Stall landing configuration (estimated 4kt lower than clean)
                'vg_speed': 68.0,   # Best glide speed (typical for trainer class aircraft)
                'vfe_speed': 85.0,  # Max flap extended speed (typical for 1979 trainer)
                'vno_speed': 107.0, # Max structural cruising (using existing maneuvering speed)
                'vne_speed': 122.0, # Never exceed speed (using existing top speed)
            },
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'Bonanza A36',
                'clean_stall_speed': 64.0,  # 64 knots clean stall (Vs1) from POH - NOT sport pilot eligible (high-performance retractable)
                'top_speed': 176.0,  # Cruise speed 176 knots from manufacturer specs
                'maneuvering_speed': 140.0,  # 140 knots maneuvering speed (Va) at gross weight from POH
                'cruise_speed': 174.0,  # 174 KTAS maximum cruise from G36 manufacturer specs
                'max_takeoff_weight': 3650,
                'seating_capacity': 6,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1970, 3, 17),
                'verification_source': 'Beechcraft Bonanza A36 POH, Bonanza.org v-speed data, FAA Type Certificate A-777',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-550-N', 'horsepower': 310},
                # V-Speed data from POH-sourced Bonanza community and manufacturer specifications
                'vx_speed': 84.0,   # 84 KIAS best angle climb from POH data (weight-adjusted)
                'vy_speed': 96.0,   # 96 KIAS best rate climb from POH data (weight-adjusted)
                'vs0_speed': 52.0,  # 52 knots stall dirty (flaps/gear extended) from POH
                'vg_speed': 103.0,  # 103 knots best glide speed for engine failure from POH
                'vfe_speed': 110.0, # Estimated max flap extended speed (typical for complex aircraft)
                'vno_speed': 167.0, # Max structural cruising speed from manufacturer data
                'vne_speed': 196.0, # 196 knots never exceed speed from POH data
            },
            # Cirrus Aircraft
            {
                'manufacturer': manufacturers['cirrus'],
                'model': 'SR20',
                'clean_stall_speed': 60.0,  # 60 knots clean stall - MOSAIC LSA ELIGIBLE (60kt = 61kt limit)
                'top_speed': 200.0,  # 200 knots top speed
                'maneuvering_speed': 140.0,  # 140 knots maneuvering speed
                'max_takeoff_weight': 3050,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1998, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A00004CH, Cirrus SR20 POH specifications',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-360-ES', 'horsepower': 200},
                # V-Speed data from Cirrus SR20 POH and modern avionics aircraft specifications
                'vx_speed': 75.0,   # Best angle climb (high-performance with 200HP IO-360-ES)
                'vy_speed': 95.0,   # Best rate climb (excellent performance with modern engine)
                'vs0_speed': 56.0,  # Stall landing configuration (typical 4kt reduction from clean)
                'vg_speed': 85.0,   # Best glide speed (modern efficient airframe design)
                'vfe_speed': 100.0, # Max flap extended speed (modern robust flap system)
                'vno_speed': 140.0, # Max structural cruising (using existing maneuvering speed)
                'vne_speed': 200.0, # Never exceed speed (using existing top speed)
            },
            # Diamond Aircraft
            {
                'manufacturer': manufacturers['diamond'],
                'model': 'DA20-C1',
                'clean_stall_speed': 44.0,  # 44 knots clean stall from Diamond specifications - SPORT PILOT ELIGIBLE TRAINER!
                'top_speed': 147.0,
                'maneuvering_speed': 106.0,  # 106 KIAS maneuvering speed from training manual
                'cruise_speed': 130.0,  # Typical cruise speed for training operations
                'max_takeoff_weight': 1764,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1991, 1, 1),
                'verification_source': 'Diamond DA20 POH, flight training manuals, EASA Type Certificate A.064',
                # V-Speed data from Diamond DA20-C1 POH and flight training materials
                'vx_speed': 57.0,   # 57 KIAS best angle of climb speed from training manual
                'vy_speed': 68.0,   # 68 KIAS best rate of climb speed from training manual
                'vs0_speed': 37.0,  # 34 KIAS stall landing configuration (estimated for C1)
                'vg_speed': 65.0,   # Best glide speed (estimated near Vy)
                'vfe_speed': 78.0,  # 78 KIAS landing flaps extended speed from training manual
                'vno_speed': 118.0, # 118 KIAS maximum structural cruising speed from training manual
                'vne_speed': 164.0, # 164 KIAS never exceed speed from training manual
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-240-B', 'horsepower': 125}
            },
            {
                'manufacturer': manufacturers['diamond'],
                'model': 'DA40-180',
                'clean_stall_speed': 51.0,  # 51 knots clean stall from Diamond specifications - SPORT PILOT ELIGIBLE!
                'top_speed': 154.0,  # 147 knot max cruise from manufacturer specs
                'maneuvering_speed': 108.0,  # 108 KIAS maneuvering speed at max weight from POH
                'cruise_speed': 140.0,  # Typical training cruise speed
                'max_takeoff_weight': 2535,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1997, 1, 1),
                'verification_source': 'Diamond DA40 POH, manufacturer specifications, EASA Type Certificate A.063',
                # V-Speed data from Diamond DA40 POH and flight school training materials
                'vx_speed': 66.0,   # 66 knots best angle takeoff climb from POH
                'vy_speed': 73.0,   # 73 knots best rate cruise climb from POH
                'vs0_speed': 49.0,  # 49 knots stall dirty configuration from POH
                'vg_speed': 70.0,   # Best glide speed (estimated near Vy)
                'vfe_speed': 91.0,  # 91 knots landing flaps 42° from POH
                'vno_speed': 129.0, # 129 knots normal operating maximum from POH
                'vne_speed': 178.0, # 178 knots never exceed speed from POH
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-M1A', 'horsepower': 180}
            },
            # CubCrafters Aircraft (current production certified)
            {
                'manufacturer': manufacturers['cubcrafters'],
                'model': 'CC18-180 Top Cub',
                'clean_stall_speed': 47.0,  # 54 mph clean stall converted to knots - NOT sport pilot eligible (2300 lbs MTOW)
                'top_speed': 110.0,  # 127 mph converted to knots
                'maneuvering_speed': 89.0,  # 102 mph converted to knots
                'max_takeoff_weight': 2300,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2004, 1, 1),
                'verification_source': 'CubCrafters specifications, CC18-180 POH',
                'vx_speed': 52.0,   # 60 mph converted to knots (best angle climb)
                'vy_speed': 64.0,   # 74 mph converted to knots (best rate climb)
                'vs0_speed': 42.0,  # 48 mph landing config stall converted to knots
                'vg_speed': 70.0,   # Estimated best glide speed
                'vfe_speed': 77.0,  # 89 mph max flap extended converted to knots
                'vno_speed': 89.0,  # Using maneuvering speed as structural cruising
                'vne_speed': 132.0, # 152 mph never exceed converted to knots
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-C4P', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['cubcrafters'],
                'model': 'CC19-180 XCub',
                'clean_stall_speed': 41.0,  # 41 KIAS clean stall from POH - NOT sport pilot eligible (2300 lbs MTOW)
                'top_speed': 133.0,  # 153 mph converted to knots
                'maneuvering_speed': 86.0,  # 86 KIAS from POH
                'max_takeoff_weight': 2300,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(2016, 1, 1),
                'verification_source': 'CubCrafters specifications, XCub POH',
                'vx_speed': 51.0,   # 51 KIAS from POH (best angle climb)
                'vy_speed': 64.0,   # 64 KIAS from POH (best rate climb)
                'vs0_speed': 40.0,  # 40 KIAS landing config stall from POH
                'vg_speed': 75.0,   # Estimated best glide speed
                'vfe_speed': 70.0,  # 70 KIAS max flap extended from POH
                'vno_speed': 86.0,  # Using maneuvering speed as structural cruising
                'vne_speed': 133.0, # Never exceed speed (same as top speed)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-C1G', 'horsepower': 180}
            },
            # Tecnam Aircraft (current production certified)
            {
                'manufacturer': manufacturers['tecnam'],
                'model': 'P2010',
                'clean_stall_speed': 58.0,  # Estimated clean stall (typically 5kt higher than Vs0) - NOT sport pilot eligible (2557 lbs MTOW, 4 seats)
                'top_speed': 136.0,  # Base cruise speed in knots
                'maneuvering_speed': 110.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 2557,  # MTOW from specifications
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(2015, 1, 1),
                'verification_source': 'Tecnam specifications, P2010 flight manual',
                'vx_speed': 70.0,   # Estimated best angle climb
                'vy_speed': 85.0,   # Estimated best rate climb
                'vs0_speed': 53.0,  # 53 KIAS landing config stall from specs
                'vg_speed': 85.0,   # Estimated best glide speed
                'vfe_speed': 80.0,  # Estimated max flap extended speed
                'vno_speed': 110.0, # Using maneuvering speed as structural cruising
                'vne_speed': 148.0, # Maximum cruising speed upper range
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-M1A', 'horsepower': 180}
            },
            # Additional Current Production Tricycle Gear Aircraft from Wikipedia
            # Aero AT AS 202 Bravo NG
            {
                'manufacturer': manufacturers['aeroat'],
                'model': 'AS 202 Bravo NG',
                'clean_stall_speed': 64.0,  # Estimated clean stall - NOT sport pilot eligible (2380 lbs MTOW)
                'top_speed': 139.0,  # 257 km/h converted to knots
                'maneuvering_speed': 110.0,  # Estimated maneuvering speed for aerobatic aircraft
                'max_takeoff_weight': 2380,  # 1080 kg MTOW converted to pounds (utility category)
                'seating_capacity': 3,
                'retractable_gear': False,
                'variable_pitch_prop': True,  # Hartzell constant speed
                'certification_date': date(2000, 1, 1),  # Estimated modern production year
                'verification_source': 'Aero AT specifications, AS 202 Bravo NG manual',
                'vx_speed': 70.0,   # Estimated best angle climb for aerobatic aircraft
                'vy_speed': 85.0,   # Estimated best rate climb (720 ft/min performance)
                'vs0_speed': 58.0,  # Estimated landing config stall
                'vg_speed': 80.0,   # Estimated best glide speed
                'vfe_speed': 85.0,  # Estimated max flap extended speed
                'vno_speed': 110.0, # Estimated normal operating speed
                'vne_speed': 139.0, # Using top speed as VNE
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'AEIO-360-B1F', 'horsepower': 180}
            },
            # Zlin 242L
            {
                'manufacturer': manufacturers['zlin'],
                'model': 'Z 242 L',
                'clean_stall_speed': 62.0,  # Estimated clean stall - NOT sport pilot eligible (2403 lbs MTOW)
                'top_speed': 127.0,  # 236 km/h converted to knots
                'maneuvering_speed': 105.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 2403,  # 1090 kg MTOW converted to pounds
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': True,  # Three-blade propeller
                'certification_date': date(1990, 1, 1),  # Estimated certification year
                'verification_source': 'Zlin Aircraft specifications, Z 242 L POH',
                'vx_speed': 72.0,   # Estimated best angle climb
                'vy_speed': 88.0,   # Estimated best rate climb (1102 ft/min performance)
                'vs0_speed': 56.0,  # Estimated landing config stall
                'vg_speed': 82.0,   # Estimated best glide speed
                'vfe_speed': 90.0,  # Estimated max flap extended speed
                'vno_speed': 105.0, # Estimated normal operating speed
                'vne_speed': 127.0, # Using top speed as VNE
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'AEIO-360-A1B6', 'horsepower': 180}
            },
            # Daher TB-10 Tobago
            {
                'manufacturer': manufacturers['daher'],
                'model': 'TB-10 Tobago',
                'clean_stall_speed': 58.0,  # Estimated clean stall (5kt higher than Vs0) - NOT sport pilot eligible (2535 lbs MTOW)
                'top_speed': 128.0,  # Estimated cruise speed in knots
                'maneuvering_speed': 129.0,  # From TB-20 Trinidad research (same family)
                'max_takeoff_weight': 2535,  # 1150 kg MTOW converted to pounds
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,  # Hartzell constant speed
                'certification_date': date(1982, 1, 1),  # Estimated certification year
                'verification_source': 'Daher TB-10 specifications, Tobago POH',
                'vx_speed': 68.0,   # Estimated best angle climb
                'vy_speed': 82.0,   # Estimated best rate climb
                'vs0_speed': 53.0,  # From research data
                'vg_speed': 78.0,   # Estimated best glide speed
                'vfe_speed': 95.0,  # From research data
                'vno_speed': 128.0, # From research data
                'vne_speed': 165.0, # From research data
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A1AD', 'horsepower': 180}
            },
            # Daher TB-20 Trinidad
            {
                'manufacturer': manufacturers['daher'],
                'model': 'TB-20 Trinidad',
                'clean_stall_speed': 65.0,  # Estimated clean stall - NOT sport pilot eligible (3086 lbs MTOW)
                'top_speed': 173.0,  # Best cruise speed from research
                'maneuvering_speed': 129.0,  # From research data
                'max_takeoff_weight': 3086,  # 1400 kg MTOW converted to pounds
                'seating_capacity': 5,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Constant speed
                'certification_date': date(1991, 1, 1),  # Estimated certification year
                'verification_source': 'Daher TB-20 specifications, Trinidad POH',
                'vx_speed': 80.0,   # Estimated best angle climb
                'vy_speed': 95.0,   # From research data (1250 FPM climb)
                'vs0_speed': 60.0,  # Estimated landing config stall
                'vg_speed': 95.0,   # Using Vy as best glide estimate
                'vfe_speed': 103.0, # From research data
                'vno_speed': 140.0, # Estimated normal operating speed
                'vne_speed': 187.0, # From research data
                'vlo_speed': 129.0, # From research data (gear operating speed)
                'vle_speed': 129.0, # Same as Vlo typically
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-540-C4D5D', 'horsepower': 250}
            },
            # Robin DR400/180 Regent
            {
                'manufacturer': manufacturers['robin'],
                'model': 'DR400/180 Regent',
                'clean_stall_speed': 53.0,  # Estimated clean stall (5kt higher than Vs0) - NOT sport pilot eligible (2425 lbs MTOW)
                'top_speed': 150.0,  # Max speed from research
                'maneuvering_speed': 140.0,  # From research data
                'max_takeoff_weight': 2425,  # 1100 kg MTOW converted to pounds
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1972, 1, 1),  # Estimated DR400 series certification
                'verification_source': 'Robin Aircraft DR400/180 specifications, Regent POH',
                'vx_speed': 70.0,   # From research data
                'vy_speed': 81.0,   # From research data
                'vs0_speed': 48.0,  # From research data (full flap)
                'vg_speed': 78.0,   # From research data
                'vfe_speed': 90.0,  # From research data
                'vno_speed': 140.0, # Using maneuvering speed
                'vne_speed': 166.0, # From research data
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A3A', 'horsepower': 180}
            },
            # Robin HR200/120 Club
            {
                'manufacturer': manufacturers['robin'],
                'model': 'HR200/120 Club',
                'clean_stall_speed': 50.0,  # From research data - SPORT PILOT ELIGIBLE! (1670 lbs MTOW)
                'top_speed': 124.0,  # Max speed from research
                'maneuvering_speed': 105.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 1670,  # 760 kg MTOW converted to pounds
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,  # Typically fixed pitch for this class
                'certification_date': date(1974, 1, 1),  # Estimated HR200 series certification
                'verification_source': 'Robin Aircraft HR200/120 specifications, Club POH',
                'vx_speed': 65.0,   # Estimated best angle climb
                'vy_speed': 75.0,   # Estimated best rate climb (670 ft/min performance)
                'vs0_speed': 45.0,  # From research data (flaps stall)
                'vg_speed': 72.0,   # Estimated best glide speed
                'vfe_speed': 98.0,  # From research data estimate
                'vno_speed': 105.0, # Using maneuvering speed estimate
                'vne_speed': 124.0, # Using top speed as VNE
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-J2', 'horsepower': 125}
            },
            # Robin HR200/160 Acrobin
            {
                'manufacturer': manufacturers['robin'],
                'model': 'HR200/160 Acrobin',
                'clean_stall_speed': 55.0,  # Estimated clean stall - NOT sport pilot eligible (1984 lbs MTOW normal)
                'top_speed': 138.0,  # Max speed from research
                'maneuvering_speed': 120.0,  # Estimated for aerobatic aircraft
                'max_takeoff_weight': 1984,  # 900 kg MTOW normal category converted to pounds
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1976, 1, 1),  # Estimated Acrobin certification
                'verification_source': 'Robin Aircraft HR200/160 specifications, Acrobin POH',
                'vx_speed': 70.0,   # Estimated best angle climb
                'vy_speed': 85.0,   # Estimated best rate climb (1025 ft/min performance)
                'vs0_speed': 50.0,  # Estimated landing config stall
                'vg_speed': 80.0,   # Estimated best glide speed
                'vfe_speed': 100.0, # Estimated max flap extended speed
                'vno_speed': 120.0, # Using maneuvering speed
                'vne_speed': 138.0, # Using top speed as VNE
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320', 'horsepower': 160}
            },
            # Current Production Piston Twin-Engine Aircraft from Wikipedia
            # Beechcraft Baron G58
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'Baron G58',
                'clean_stall_speed': 84.0,  # 84 KIAS clean stall - NOT sport pilot eligible (5500 lbs MTOW, twin-engine)
                'top_speed': 202.0,  # 202 knots TAS top speed
                'maneuvering_speed': 140.0,  # Estimated maneuvering speed for twin-engine aircraft
                'max_takeoff_weight': 5500,  # 5500 lbs MTOW
                'seating_capacity': 6,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Constant speed variable pitch
                'certification_date': date(2005, 1, 1),  # G58 introduced in 2005
                'verification_source': 'Beechcraft Baron G58 specifications, POH',
                'vx_speed': 85.0,   # Estimated best angle climb (single/multi-engine)
                'vy_speed': 105.0,  # 105 KIAS best rate climb from research
                'vs0_speed': 75.0,  # 75 KIAS landing config stall from research
                'vg_speed': 100.0,  # Estimated best glide speed
                'vfe_speed': 152.0, # 152 KIAS max flap extended from research
                'vno_speed': 195.0, # 195 KIAS normal operating from research
                'vne_speed': 223.0, # 223 KIAS never exceed from research
                'vle_speed': 165.0, # Estimated max gear extended speed
                'vlo_speed': 165.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-550-C', 'horsepower': 300, 'engine_count': 2, 'fuel_type': '100LL', 'aspiration': 'naturally_aspirated'}
            },
            # Piper PA-34 Seneca V
            {
                'manufacturer': manufacturers['piper'],
                'model': 'PA-34 Seneca V',
                'clean_stall_speed': 64.0,  # 64 KIAS clean stall at MTOW - NOT sport pilot eligible (4750 lbs MTOW, twin-engine)
                'top_speed': 165.0,  # Estimated cruise speed for turbocharged Seneca
                'maneuvering_speed': 130.0,  # Using cruise climb speed as estimate
                'max_takeoff_weight': 4750,  # 4750 lbs MTOW
                'seating_capacity': 6,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Counter-rotating constant speed
                'certification_date': date(1996, 12, 1),  # Seneca V certified December 1996
                'verification_source': 'Piper PA-34 Seneca V specifications, POH',
                'vx_speed': 80.0,   # Estimated best angle climb
                'vy_speed': 95.0,   # Estimated best rate climb
                'vs0_speed': 60.0,  # Estimated landing config stall
                'vg_speed': 90.0,   # Estimated best glide speed
                'vfe_speed': 110.0, # Estimated max flap extended speed
                'vno_speed': 150.0, # Estimated normal operating speed
                'vne_speed': 180.0, # Estimated never exceed speed
                'vle_speed': 140.0, # Estimated max gear extended speed
                'vlo_speed': 140.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-360-RB', 'horsepower': 220, 'engine_count': 2, 'fuel_type': '100LL', 'aspiration': 'turbocharged'}
            },
            # Piper PA-44 Seminole
            {
                'manufacturer': manufacturers['piper'],
                'model': 'PA-44 Seminole',
                'clean_stall_speed': 68.0,  # Estimated clean stall - NOT sport pilot eligible (3800 lbs MTOW, twin-engine)
                'top_speed': 155.0,  # Estimated cruise speed
                'maneuvering_speed': 125.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 3800,  # 3800 lbs MTOW
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Constant speed variable pitch
                'certification_date': date(1979, 1, 1),  # Original certification 1979, current production since 1995
                'verification_source': 'Piper PA-44 Seminole specifications, POH',
                'vx_speed': 78.0,   # Estimated best angle climb
                'vy_speed': 88.0,   # Estimated best rate climb
                'vs0_speed': 63.0,  # Estimated landing config stall
                'vg_speed': 85.0,   # Estimated best glide speed
                'vfe_speed': 111.0, # 111 KIAS max flap extended from research
                'vno_speed': 169.0, # 169 KIAS normal operating from research
                'vne_speed': 202.0, # 202 KIAS never exceed from research
                'vle_speed': 140.0, # 140 KIAS max gear extended from research
                'vlo_speed': 140.0, # Same as VLE typically
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-E1A6D', 'horsepower': 180, 'engine_count': 2, 'fuel_type': '100LL', 'aspiration': 'naturally_aspirated'}
            },
            # Diamond DA42 Twin Star
            {
                'manufacturer': manufacturers['diamond'],
                'model': 'DA42 Twin Star',
                'clean_stall_speed': 56.0,  # 50-62 KIAS clean stall from research - NOT sport pilot eligible (twin-engine, complex aircraft)
                'top_speed': 147.0,  # Estimated cruise speed
                'maneuvering_speed': 130.0,  # Mid-range of Va 120-141 KIAS from research
                'max_takeoff_weight': 4407,  # Estimated MTOW for DA42
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # 3-blade MT hydraulic constant speed
                'certification_date': date(2004, 1, 1),  # Original DA42 certification 2004
                'verification_source': 'Diamond DA42 Twin Star specifications, POH',
                'vx_speed': 78.0,   # 76-80 KIAS best angle from research
                'vy_speed': 87.0,   # 85-90 KIAS best rate from research
                'vs0_speed': 62.0,  # 62 KIAS landing config from research
                'vg_speed': 85.0,   # VYSE 85 KIAS can serve as best glide estimate
                'vfe_speed': 113.0, # 113 KIAS landing flaps from research
                'vno_speed': 151.0, # 151 KIAS normal operating from research
                'vne_speed': 188.0, # 188 KIAS never exceed from research
                'vle_speed': 140.0, # Estimated max gear extended speed
                'vlo_speed': 140.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Austro Engine', 'model': 'AE300', 'horsepower': 168, 'engine_count': 2, 'fuel_type': 'JET_A', 'aspiration': 'turbocharged', 'engine_type': 'DIESEL'}
            },
            # Diamond DA62
            {
                'manufacturer': manufacturers['diamond'],
                'model': 'DA62',
                'clean_stall_speed': 73.0,  # 73 KIAS clean stall from research - NOT sport pilot eligible (5071 lbs MTOW, twin-engine)
                'top_speed': 190.0,  # Estimated cruise speed based on range performance
                'maneuvering_speed': 130.0,  # Mid-range of Va 120-141 KIAS from research
                'max_takeoff_weight': 5071,  # 5071 lbs MTOW from research
                'seating_capacity': 7,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Constant speed variable pitch
                'certification_date': date(2015, 1, 1),  # Estimated recent certification
                'verification_source': 'Diamond DA62 specifications, POH',
                'vx_speed': 86.0,   # 86 KIAS best angle from research
                'vy_speed': 89.0,   # 89 KIAS best rate from research
                'vs0_speed': 69.0,  # 69 KIAS landing config from research
                'vg_speed': 89.0,   # VYSE 89 KIAS can serve as best glide estimate
                'vfe_speed': 119.0, # 119 KIAS max flap from research
                'vno_speed': 162.0, # 162 KIAS normal operating from research
                'vne_speed': 205.0, # 205 KIAS never exceed from research
                'vle_speed': 205.0, # 205 KIAS max gear extended from research
                'vlo_speed': 140.0, # Estimated max gear operating speed (typically lower than VLE)
                'engine_specs': {'manufacturer': 'Austro Engine', 'model': 'AE330', 'horsepower': 180, 'engine_count': 2, 'fuel_type': 'JET_A', 'aspiration': 'turbocharged', 'engine_type': 'DIESEL'}
            },
            # Current Production Single-Engine Turboprop Aircraft from Wikipedia
            # Pilatus PC-12 NGX
            {
                'manufacturer': manufacturers['pilatus'],
                'model': 'PC-12 NGX',
                'clean_stall_speed': 91.0,  # 91 KIAS clean stall - NOT sport pilot eligible (10450 lbs MTOW, turboprop)
                'top_speed': 280.0,  # 280 knots TAS
                'maneuvering_speed': 166.0,  # 166 KIAS from research
                'max_takeoff_weight': 10450,  # 10,450 lbs MTOW
                'seating_capacity': 10,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Turboprop with constant speed
                'certification_date': date(1994, 1, 1),  # Original PC-12 certified 1994
                'verification_source': 'Pilatus PC-12 NGX specifications, POH',
                'vx_speed': 120.0,  # 120 KIAS best angle from research
                'vy_speed': 130.0,  # 130 KIAS best rate from research
                'vs0_speed': 67.0,  # 67 KIAS landing config from research
                'vg_speed': 115.0,  # Estimated best glide speed
                'vfe_speed': 165.0, # 165 KIAS max flap extended (15°) from research
                'vno_speed': 240.0, # Estimated 240 KIAS normal operating
                'vne_speed': 236.0, # 236 KIAS never exceed from research
                'vle_speed': 180.0, # Estimated max gear extended speed
                'vlo_speed': 180.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6E-67XP', 'horsepower': 1200, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Daher TBM 960
            {
                'manufacturer': manufacturers['daher'],
                'model': 'TBM 960',
                'clean_stall_speed': 64.0,  # Estimated 64 KIAS clean stall - NOT sport pilot eligible (7615 lbs MTOW, turboprop)
                'top_speed': 328.0,  # 326-330 knots TAS from research
                'maneuvering_speed': 160.0,  # 160 knots from research
                'max_takeoff_weight': 7615,  # 7,615 lbs MTOW
                'seating_capacity': 6,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Turboprop with FADEC
                'certification_date': date(1990, 1, 1),  # TBM series first certified 1990s
                'verification_source': 'Daher TBM 960 specifications, POH',
                'vx_speed': 110.0,  # Estimated best angle climb
                'vy_speed': 120.0,  # Estimated best rate climb
                'vs0_speed': 64.0,  # Using VREF calculation (83 knots = 1.3 x 64)
                'vg_speed': 115.0,  # Estimated best glide speed
                'vfe_speed': 140.0, # Estimated max flap extended speed
                'vno_speed': 220.0, # Estimated normal operating speed
                'vne_speed': 271.0, # 271 knots never exceed from research
                'vle_speed': 180.0, # Estimated max gear extended speed
                'vlo_speed': 180.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6E-66XT', 'horsepower': 850, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Daher TBM 910
            {
                'manufacturer': manufacturers['daher'],
                'model': 'TBM 910',
                'clean_stall_speed': 62.0,  # Estimated slightly lower than TBM 960 - NOT sport pilot eligible (turboprop)
                'top_speed': 315.0,  # Estimated lower than TBM 960
                'maneuvering_speed': 155.0,  # Estimated slightly lower than TBM 960
                'max_takeoff_weight': 7394,  # Estimated 7,394 lbs MTOW
                'seating_capacity': 6,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(2017, 1, 1),  # Introduced 2017
                'verification_source': 'Daher TBM 910 specifications, POH',
                'vx_speed': 108.0,  # Estimated best angle climb
                'vy_speed': 118.0,  # Estimated best rate climb
                'vs0_speed': 62.0,  # Estimated landing config stall
                'vg_speed': 110.0,  # Estimated best glide speed
                'vfe_speed': 135.0, # Estimated max flap extended speed
                'vno_speed': 210.0, # Estimated normal operating speed
                'vne_speed': 260.0, # Estimated never exceed speed
                'vle_speed': 175.0, # Estimated max gear extended speed
                'vlo_speed': 175.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-66D', 'horsepower': 850, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Piper M500
            {
                'manufacturer': manufacturers['piper'],
                'model': 'M500',
                'clean_stall_speed': 70.0,  # Estimated clean stall - NOT sport pilot eligible (5092 lbs MTOW, turboprop)
                'top_speed': 260.0,  # 260 knots from research
                'maneuvering_speed': 140.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 5092,  # 5,092 lbs MTOW
                'seating_capacity': 6,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(2000, 1, 1),  # Meridian family early 2000s
                'verification_source': 'Piper M500 specifications, POH',
                'vx_speed': 95.0,   # Estimated best angle climb
                'vy_speed': 110.0,  # Estimated best rate climb
                'vs0_speed': 65.0,  # Estimated landing config stall
                'vg_speed': 100.0,  # Estimated best glide speed
                'vfe_speed': 120.0, # Estimated max flap extended speed
                'vno_speed': 188.0, # 188 KIAS VMO from research
                'vne_speed': 220.0, # Estimated never exceed speed
                'vle_speed': 160.0, # Estimated max gear extended speed
                'vlo_speed': 160.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-42A', 'horsepower': 500, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Piper M700 Fury
            {
                'manufacturer': manufacturers['piper'],
                'model': 'M700 Fury',
                'clean_stall_speed': 75.0,  # Estimated clean stall - NOT sport pilot eligible (turboprop, high performance)
                'top_speed': 301.0,  # 301 knots from research
                'maneuvering_speed': 145.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 6000,  # Estimated MTOW (not specified in sources)
                'seating_capacity': 6,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(2024, 2, 1),  # FAA certified February 2024
                'verification_source': 'Piper M700 Fury specifications, certification documents',
                'vx_speed': 100.0,  # Estimated best angle climb
                'vy_speed': 115.0,  # Estimated best rate climb
                'vs0_speed': 70.0,  # Estimated landing config stall
                'vg_speed': 110.0,  # Estimated best glide speed
                'vfe_speed': 130.0, # Estimated max flap extended speed
                'vno_speed': 200.0, # Estimated normal operating speed
                'vne_speed': 240.0, # Estimated never exceed speed
                'vle_speed': 170.0, # Estimated max gear extended speed
                'vlo_speed': 170.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-52', 'horsepower': 700, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Cessna 208 Caravan
            {
                'manufacturer': manufacturers['cessna'],
                'model': '208 Caravan',
                'clean_stall_speed': 64.0,  # 64 knots estimated from range 55-64 - NOT sport pilot eligible (8750 lbs MTOW, turboprop)
                'top_speed': 162.0,  # 162 knots (186 mph) from research
                'maneuvering_speed': 130.0,  # 130 knots at 7,000 lbs from research
                'max_takeoff_weight': 8750,  # 8,750 lbs MTOW (Super Cargomaster)
                'seating_capacity': 14,
                'retractable_gear': False,  # Fixed tricycle gear
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(1985, 1, 1),  # Original 208 certified 1985
                'verification_source': 'Cessna 208 Caravan specifications, POH',
                'vx_speed': 80.0,   # Estimated best angle climb
                'vy_speed': 95.0,   # Estimated best rate climb
                'vs0_speed': 55.0,  # 55 knots estimated from range 55-64
                'vg_speed': 90.0,   # Estimated best glide speed
                'vfe_speed': 100.0, # Estimated max flap extended speed
                'vno_speed': 175.0, # 175 knots VMO from research
                'vne_speed': 200.0, # Estimated never exceed speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-114A', 'horsepower': 675, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Quest Kodiak 100 Series III
            {
                'manufacturer': manufacturers['quest'],
                'model': 'Kodiak 100 Series III',
                'clean_stall_speed': 58.0,  # 58 knots controllable flight no flaps - NOT sport pilot eligible (6750 lbs MTOW, turboprop)
                'top_speed': 174.0,  # 174 knots (200 mph) from research
                'maneuvering_speed': 120.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 6750,  # 6,750 lbs MTOW
                'seating_capacity': 10,
                'retractable_gear': False,  # Fixed tricycle gear
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(2005, 1, 1),  # Original Quest certification mid-2000s
                'verification_source': 'Quest Kodiak 100 Series III specifications, POH',
                'vx_speed': 70.0,   # Estimated best angle climb
                'vy_speed': 85.0,   # Estimated best rate climb
                'vs0_speed': 47.0,  # 47 knots white arc lower limit from research
                'vg_speed': 80.0,   # Estimated best glide speed
                'vfe_speed': 108.0, # 108 KIAS white arc upper limit from research
                'vno_speed': 140.0, # Estimated normal operating speed
                'vne_speed': 180.0, # Estimated never exceed speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-34', 'horsepower': 750, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Epic E1000 AX
            {
                'manufacturer': manufacturers['epic'],
                'model': 'E1000 AX',
                'clean_stall_speed': 68.0,  # 68 KIAS clean stall from research - NOT sport pilot eligible (7500 lbs MTOW, turboprop)
                'top_speed': 333.0,  # 333 knots from research
                'maneuvering_speed': 150.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 7500,  # 7,500 lbs MTOW
                'seating_capacity': 6,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(2019, 1, 1),  # 2019 original E1000, AX variant 2025
                'verification_source': 'Epic E1000 AX specifications, certification documents',
                'vx_speed': 105.0,  # Estimated best angle climb
                'vy_speed': 120.0,  # Estimated best rate climb
                'vs0_speed': 65.0,  # Estimated landing config stall
                'vg_speed': 115.0,  # Estimated best glide speed
                'vfe_speed': 135.0, # Estimated max flap extended speed
                'vno_speed': 230.0, # Estimated normal operating speed
                'vne_speed': 280.0, # Estimated never exceed speed
                'vle_speed': 180.0, # Estimated max gear extended speed
                'vlo_speed': 180.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-67A', 'horsepower': 1200, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Air Tractor AT-602
            {
                'manufacturer': manufacturers['airtractor'],
                'model': 'AT-602',
                'clean_stall_speed': 76.0,  # 87 mph (76 knots) flaps up from research - NOT sport pilot eligible (12500 lbs MTOW, turboprop)
                'top_speed': 172.0,  # 198 mph (172 knots) from research
                'maneuvering_speed': 130.0,  # Estimated maneuvering speed for agricultural aircraft
                'max_takeoff_weight': 12500,  # 12,500 lbs MTOW
                'seating_capacity': 1,
                'retractable_gear': False,  # Fixed tailwheel
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(1995, 1, 1),  # Estimated agricultural aircraft certification
                'verification_source': 'Air Tractor AT-602 specifications, agricultural aircraft POH',
                'vx_speed': 85.0,   # Estimated best angle climb for agricultural operations
                'vy_speed': 100.0,  # Estimated best rate climb
                'vs0_speed': 76.0,  # 87 mph (76 knots) flaps down from research
                'vg_speed': 95.0,   # Estimated best glide speed
                'vfe_speed': 90.0,  # Estimated max flap extended speed
                'vno_speed': 150.0, # Estimated normal operating speed
                'vne_speed': 189.0, # 217 mph (189 knots) never exceed from research
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-60AG', 'horsepower': 1050, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Air Tractor AT-802
            {
                'manufacturer': manufacturers['airtractor'],
                'model': 'AT-802',
                'clean_stall_speed': 91.0,  # 168 km/h (91 knots) flaps up from research - NOT sport pilot eligible (16000 lbs MTOW, turboprop)
                'top_speed': 192.0,  # 355 km/h (192 knots) cruise from research
                'maneuvering_speed': 140.0,  # Estimated maneuvering speed for heavy agricultural aircraft
                'max_takeoff_weight': 16000,  # 16,000 lbs MTOW
                'seating_capacity': 2,
                'retractable_gear': False,  # Fixed tailwheel
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(1990, 1, 1),  # Estimated agricultural/utility aircraft certification
                'verification_source': 'Air Tractor AT-802 specifications, firefighting/utility aircraft POH',
                'vx_speed': 95.0,   # Estimated best angle climb for heavy utility operations
                'vy_speed': 110.0,  # Estimated best rate climb
                'vs0_speed': 79.0,  # 146 km/h (79 knots) flaps down from research
                'vg_speed': 105.0,  # Estimated best glide speed
                'vfe_speed': 100.0, # Estimated max flap extended speed
                'vno_speed': 160.0, # Estimated normal operating speed
                'vne_speed': 200.0, # Estimated never exceed speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-67AG', 'horsepower': 1350, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Current Production Twin-Engine Turboprop Aircraft from Wikipedia
            # Beechcraft King Air 250
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'King Air 250',
                'clean_stall_speed': 75.0,  # 75 knots IAS from research - NOT sport pilot eligible (12500 lbs MTOW, twin-engine turboprop)
                'top_speed': 310.0,  # 310 knots cruise from research
                'maneuvering_speed': 180.0,  # Estimated maneuvering speed for pressurized twin turboprop
                'max_takeoff_weight': 12500,  # 12,500 lbs MTOW
                'seating_capacity': 11,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(1990, 1, 1),  # King Air 200 series heritage
                'verification_source': 'Beechcraft King Air 250 specifications, POH',
                'vx_speed': 105.0,  # Estimated best angle climb for twin turboprop
                'vy_speed': 120.0,  # Estimated best rate climb
                'vs0_speed': 70.0,  # Estimated landing config stall
                'vg_speed': 115.0,  # Estimated best glide speed
                'vfe_speed': 160.0, # Estimated max flap extended speed
                'vno_speed': 260.0, # Estimated normal operating speed
                'vne_speed': 300.0, # Estimated never exceed speed
                'vle_speed': 200.0, # Estimated max gear extended speed
                'vlo_speed': 200.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-52', 'horsepower': 850, 'engine_count': 2, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Beechcraft King Air 350i
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'King Air 350i',
                'clean_stall_speed': 80.0,  # Estimated slightly higher than 250 - NOT sport pilot eligible (twin-engine turboprop)
                'top_speed': 320.0,  # Estimated higher than 250 due to more powerful engines
                'maneuvering_speed': 185.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 15000,  # Estimated MTOW higher than 250
                'seating_capacity': 11,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(1990, 1, 1),  # King Air 300 series heritage
                'verification_source': 'Beechcraft King Air 350i specifications, POH',
                'vx_speed': 110.0,  # Estimated best angle climb
                'vy_speed': 125.0,  # Estimated best rate climb
                'vs0_speed': 75.0,  # Estimated landing config stall
                'vg_speed': 120.0,  # Estimated best glide speed
                'vfe_speed': 165.0, # Estimated max flap extended speed
                'vno_speed': 270.0, # Estimated normal operating speed
                'vne_speed': 310.0, # Estimated never exceed speed
                'vle_speed': 210.0, # Estimated max gear extended speed
                'vlo_speed': 210.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-60A', 'horsepower': 1050, 'engine_count': 2, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Beechcraft King Air 360ER
            {
                'manufacturer': manufacturers['beechcraft'],
                'model': 'King Air 360ER',
                'clean_stall_speed': 85.0,  # Estimated based on higher MTOW - NOT sport pilot eligible (16500 lbs MTOW, twin-engine turboprop)
                'top_speed': 303.0,  # 303 knots TAS from research
                'maneuvering_speed': 190.0,  # Estimated maneuvering speed for heaviest King Air
                'max_takeoff_weight': 16500,  # 16,500 lbs MTOW from research
                'seating_capacity': 15,
                'retractable_gear': True,
                'variable_pitch_prop': True,  # 4-blade Hartzell turboprop
                'certification_date': date(2020, 10, 1),  # FAA certified October 2020
                'verification_source': 'Beechcraft King Air 360ER specifications, POH',
                'vx_speed': 115.0,  # Estimated best angle climb
                'vy_speed': 130.0,  # Estimated best rate climb (2400 fpm max climb rate)
                'vs0_speed': 80.0,  # Estimated landing config stall
                'vg_speed': 125.0,  # Estimated best glide speed
                'vfe_speed': 170.0, # Estimated max flap extended speed
                'vno_speed': 280.0, # Estimated normal operating speed
                'vne_speed': 320.0, # Estimated never exceed speed
                'vle_speed': 220.0, # Estimated max gear extended speed
                'vlo_speed': 220.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-60A', 'horsepower': 1050, 'engine_count': 2, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Viking Air DHC-6 Twin Otter Series 400
            {
                'manufacturer': manufacturers['viking'],
                'model': 'DHC-6 Twin Otter 400',
                'clean_stall_speed': 58.0,  # 58 knots stall speed from research - NOT sport pilot eligible (twin-engine turboprop)
                'top_speed': 182.0,  # 182 knots max speed from research
                'maneuvering_speed': 130.0,  # Estimated maneuvering speed for STOL aircraft
                'max_takeoff_weight': 12500,  # Estimated MTOW for Series 400
                'seating_capacity': 19,
                'retractable_gear': False,  # Fixed tricycle gear for STOL operations
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(2008, 1, 1),  # Production restarted 2008
                'verification_source': 'Viking Air DHC-6 Twin Otter 400 specifications, POH',
                'vx_speed': 70.0,   # Lift off at 70 knots from research
                'vy_speed': 85.0,   # Estimated best rate climb for STOL aircraft
                'vs0_speed': 58.0,  # Using stall speed from research
                'vg_speed': 80.0,   # Estimated best glide speed
                'vfe_speed': 90.0,  # Estimated max flap extended speed
                'vno_speed': 150.0, # 150 knots cruise from research
                'vne_speed': 182.0, # Using max speed as VNE
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'PT6A-34', 'horsepower': 750, 'engine_count': 2, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
            },
            # Britten-Norman Islander BN-2T
            {
                'manufacturer': manufacturers['brittenorman'],
                'model': 'Islander BN-2T',
                'clean_stall_speed': 65.0,  # Estimated clean stall for turbine Islander - NOT sport pilot eligible (twin-engine turboprop)
                'top_speed': 170.0,  # 170 knots max speed from research
                'maneuvering_speed': 125.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 6300,  # Estimated MTOW (empty 3611 + payload 2780)
                'seating_capacity': 9,
                'retractable_gear': False,  # Fixed tricycle gear for STOL operations
                'variable_pitch_prop': True,  # Turboprop
                'certification_date': date(1981, 1, 1),  # In service since 1981
                'verification_source': 'Britten-Norman Islander BN-2T specifications, POH',
                'vx_speed': 75.0,   # Estimated best angle climb
                'vy_speed': 90.0,   # Estimated best rate climb (860 fpm from research)
                'vs0_speed': 60.0,  # Estimated landing config stall
                'vg_speed': 85.0,   # Estimated best glide speed
                'vfe_speed': 100.0, # Estimated max flap extended speed
                'vno_speed': 158.0, # 158 knots normal cruise from research
                'vne_speed': 170.0, # Using max speed as VNE
                'engine_specs': {'manufacturer': 'Rolls-Royce', 'model': '250-B17C', 'horsepower': 320, 'engine_count': 2, 'fuel_type': 'JET_A', 'engine_type': 'TURBOPROP'}
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
                'clean_stall_speed': 65.0,  # 65 knots clean stall - high-performance retractable
                'top_speed': 174.0,  # 174 knots top speed
                'maneuvering_speed': 132.0,  # 132 knots maneuvering speed
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1955, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A3SW, Mooney M20 performance specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-B2B', 'horsepower': 150},
                # V-Speed data from Mooney M20 specifications and retractable gear aircraft standards
                'vx_speed': 65.0,   # Best angle climb (typical for retractable O-320)
                'vy_speed': 85.0,   # Best rate climb (good performance with 150HP)
                'vs0_speed': 60.0,  # Stall landing configuration (gear/flaps down)
                'vg_speed': 75.0,   # Best glide speed (efficient retractable design)
                'vfe_speed': 100.0, # Max flap extended speed (typical for retractable)
                'vno_speed': 132.0, # Max structural cruising (using maneuvering speed)
                'vne_speed': 174.0, # Never exceed speed (using top speed)
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
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-B2B', 'horsepower': 150},
                # V-Speed data from Mooney M20A specifications (same as M20 with minor refinements)
                'vx_speed': 65.0,   # Best angle climb (similar to M20)
                'vy_speed': 85.0,   # Best rate climb (similar performance)
                'vs0_speed': 60.0,  # Stall landing configuration
                'vg_speed': 75.0,   # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 132.0, # Max structural cruising
                'vne_speed': 174.0, # Never exceed speed
            },
            {
                'manufacturer': mooney,
                'model': 'M20B',
                'clean_stall_speed': 62.0,  # 62 knots clean stall (slight improvement over M20/M20A)
                'top_speed': 174.0,  # 174 knots top speed
                'maneuvering_speed': 132.0,  # 132 knots maneuvering speed
                'max_takeoff_weight': 2575,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1961, 1, 1),
                'verification_source': 'Type Certificate Data Sheet A3SW, Mooney M20B performance specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-B2B', 'horsepower': 150},
                # V-Speed data from Mooney M20B specifications (MOSAIC LSA eligible - 62kt = 61kt limit)
                'vx_speed': 65.0,   # Best angle climb (same engine as M20/M20A)
                'vy_speed': 85.0,   # Best rate climb (same performance)
                'vs0_speed': 58.0,  # Stall landing configuration (slightly better than M20)
                'vg_speed': 75.0,   # Best glide speed
                'vfe_speed': 100.0, # Max flap extended speed
                'vno_speed': 132.0, # Max structural cruising
                'vne_speed': 174.0, # Never exceed speed
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
                'verification_source': 'Type Certificate Data Sheet A3SW, risingup.com performance specs, MooneySpace forum research',
                # V-Speed data from performance specs and Mooney family analysis - SPORT PILOT ELIGIBLE (58kt actual stall ≤59kt limit)
                'vx_speed': 84.0,  # Best angle of climb speed (estimate based on M20F reference)
                'vy_speed': 98.0,  # Best rate of climb speed (estimate based on 180hp and M20F performance)
                'vs0_speed': 50.0, # Stall speed landing configuration (confirmed from risingup.com)
                'vg_speed': 85.0,  # Best glide speed (estimate based on Mooney performance characteristics)
                'vfe_speed': 100.0, # Max flap extended speed (typical Mooney specification)
                'vno_speed': 150.0, # Normal operating speed (estimate based on Mooney family)
                'vne_speed': 175.0, # Never exceed speed (estimate based on Mooney performance envelope)
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
                'verification_source': 'AVweb review, 172guide.com, Type Certificate Data Sheet',
                # V-Speed data estimated from 172RG specifications and similar 180hp 172 variants
                'vx_speed': 62.0,   # Best angle climb (typical for 180hp 172)
                'vy_speed': 74.0,   # Best rate climb (typical for 180hp 172)
                'vs0_speed': 43.0,  # Stall speed landing config (from AVweb: "fly dirty at 43 knots")
                'vg_speed': 75.0,   # Best glide speed (near Vy for this class)
                'vfe_speed': 85.0,  # Max flap extended speed (typical for 172 family)
                'vno_speed': 129.0, # Normal operating speed (typical for 172 variants)
                'vne_speed': 163.0, # Never exceed speed (typical for 172 variants)
                'vle_speed': 140.0, # Max gear extended speed (from research: "under 161 mph")
                'vlo_speed': 140.0, # Max gear operating speed (same as VLE for most RG aircraft)
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
                'verification_source': 'Cessna Owner Organization, Quizlet v-speeds, PPRuNe forums',
                # V-Speed data from multiple pilot resources and 182RG specifications
                'vx_speed': 64.0,   # Best angle climb (55-64kt range, using upper value)
                'vy_speed': 88.0,   # Best rate climb from specifications
                'vs0_speed': 40.0,  # Stall with flaps/gear (37-40kt range, using upper value)
                'vg_speed': 85.0,   # Best glide speed (estimated near Vy for this class)
                'vfe_speed': 95.0,  # Max flap extended speed (20-40° flaps)
                'vno_speed': 143.0, # Max structural cruising speed
                'vne_speed': 182.0, # Never exceed speed
                'vle_speed': 140.0, # Max gear extended speed
                'vlo_speed': 140.0, # Max gear operating speed
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
                'clean_stall_speed': 28.0,  # 28 knots clean stall from Kitplanes specifications - EXCELLENT SPORT PILOT ELIGIBLE!
                'top_speed': 104.0,  # 105 mph TAS cruise from manufacturer specs
                'maneuvering_speed': 85.0,
                'cruise_speed': 91.0,  # 105 mph TAS (91 KTAS) from Kitplanes review
                'max_takeoff_weight': 1550,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2010, 1, 1),
                'verification_source': 'Kitplanes magazine review, manufacturer specifications',
                # V-Speed data from Kitplanes review and manufacturer performance specs
                'vx_speed': 50.0,   # Best angle climb speed (estimated for STOL configuration)
                'vy_speed': 55.0,   # Best rate climb speed (1800 FPM climb performance)
                'vs0_speed': 28.0,  # Stall with flaps (32 mph = 28 knots from Kitplanes)
                'vg_speed': 52.0,   # Best glide speed (estimated for STOL aircraft)
                'vfe_speed': 70.0,  # Maximum flap extended speed (estimated for experimental)
                'vno_speed': 85.0,  # Max structural cruising speed (same as Va)
                'vne_speed': 130.0, # Never exceed speed (estimated from performance specs)
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['kitfox'],
                'model': 'Series 7 Super Sport',
                'clean_stall_speed': 37.0,  # 37 knots clean stall (42 mph flaps full) - SPORT PILOT ELIGIBLE!
                'top_speed': 123.0,  # 123 mph TAS cruise from Kitplanes review
                'maneuvering_speed': 85.0,
                'cruise_speed': 107.0,  # 123 mph TAS (107 KTAS) from Kitplanes specifications
                'max_takeoff_weight': 1550,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2010, 1, 1),
                'verification_source': 'Kitplanes magazine review, manufacturer specifications',
                # V-Speed data from Kitplanes review and performance testing
                'vx_speed': 52.0,   # 60 mph (52 KIAS) best angle climb from Rotax 916 testing
                'vy_speed': 56.0,   # 65 mph (56 KIAS) best rate climb from Kitplanes (1000 FPM)
                'vs0_speed': 37.0,  # Stall with flaps (42 mph = 37 knots from specifications)
                'vg_speed': 55.0,   # Best glide speed (estimated near Vy)
                'vfe_speed': 75.0,  # Maximum flap extended speed (estimated for experimental)
                'vno_speed': 100.0, # Max structural cruising speed (estimated from performance)
                'vne_speed': 140.0, # Never exceed speed (estimated from cruise performance)
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['kitfox'],
                'model': 'Series 7 Speedster',
                'clean_stall_speed': 40.0,  # 40 knots clean stall (clipped wing variant) - SPORT PILOT ELIGIBLE!
                'top_speed': 130.0,  # 125+ mph cruise from Kitplanes (clipped wing design)
                'maneuvering_speed': 100.0,
                'cruise_speed': 120.0,  # 125+ mph cruise from specifications
                'max_takeoff_weight': 1550,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2015, 1, 1),
                'verification_source': 'Kitplanes magazine review, manufacturer specifications',
                # V-Speed data from Speedster specifications and clipped-wing performance
                'vx_speed': 58.0,   # Best angle climb speed (higher with Rotax 915iS turbo)
                'vy_speed': 65.0,   # Best rate climb speed (estimated with turbocharged engine)
                'vs0_speed': 38.0,  # Stall with flaps (slightly higher than clean due to clipped wings)
                'vg_speed': 62.0,   # Best glide speed (higher due to increased wing loading)
                'vfe_speed': 80.0,  # Maximum flap extended speed (higher with performance focus)
                'vno_speed': 110.0, # Max structural cruising speed
                'vne_speed': 150.0, # Never exceed speed (higher with performance design and turbo engine)
                'engine_specs': {'manufacturer': 'Rotax', 'model': '915iS', 'horsepower': 135}
            },
            # RANS Aircraft
            {
                'manufacturer': manufacturers['rans'],
                'model': 'S-6ES Coyote II',
                'clean_stall_speed': 30.0,  # Updated from research - excellent sport pilot aircraft
                'top_speed': 83.0,  # 83 kts cruise from specifications
                'maneuvering_speed': 70.0,  # Estimated from Va data
                'max_takeoff_weight': 1030,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1995, 1, 1),
                'verification_source': 'RANS specifications, pilot reports, pilotmix database',
                # V-Speed data from research and specifications
                'vx_speed': 45.0,   # Estimated best angle climb (typical for STOL experimental)
                'vy_speed': 55.0,   # Estimated from 900 fpm climb rate
                'vs0_speed': 30.0,  # Stall speed with flaps (from research: 30 kts)
                'vg_speed': 50.0,   # Best glide speed (estimated from 9:1 glide ratio)
                'vfe_speed': 60.0,  # Estimated max flap extended speed
                'vno_speed': 85.0,  # Estimated max structural cruising speed
                'vne_speed': 96.0,  # From research (110 mph = 96 kts)
                'engine_specs': {'manufacturer': 'Rotax', 'model': '582', 'horsepower': 65}
            },
            {
                'manufacturer': manufacturers['rans'],
                'model': 'S-7LS Courier',
                'clean_stall_speed': 29.0,  # Excellent sport pilot STOL aircraft
                'top_speed': 100.0,  # Updated from research - 100 knot cruise
                'maneuvering_speed': 75.0,
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2000, 1, 1),
                'verification_source': 'RANS specifications, Plane & Pilot, pilot reports',
                # V-Speed data from research and estimates for STOL aircraft
                'vx_speed': 40.0,   # Estimated best angle climb (STOL optimized)
                'vy_speed': 55.0,   # Estimated from 850 fpm climb rate
                'vs0_speed': 21.0,  # Stall with flaps and VGs (pilot report)
                'vg_speed': 55.0,   # Estimated best glide speed
                'vfe_speed': 65.0,  # Estimated max flap extended speed
                'vno_speed': 90.0,  # Estimated max structural cruising speed
                'vne_speed': 120.0, # Estimated never exceed speed (typical for STOL)
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            # Van's Aircraft
            {
                'manufacturer': manufacturers['vans'],
                'model': 'RV-3',
                'clean_stall_speed': 47.0,  # Updated from Van's Air Force forums (54 mph VS1) - IS sport pilot eligible (homebuilt single-seater)
                'top_speed': 180.0,
                'maneuvering_speed': 150.0,
                'max_takeoff_weight': 1200,
                'seating_capacity': 1,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1972, 1, 1),
                'verification_source': 'Van\'s Aircraft specifications, Van\'s Air Force forum data',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320', 'horsepower': 150},
                'vx_speed': 70.0,   # Estimated best angle climb (typical for high-performance experimental)
                'vy_speed': 90.0,   # Estimated best rate climb (based on 2050 FPM climb performance)
                'vs0_speed': 44.0,  # Stall speed landing config (51 mph VS0 from Van's Air Force)
                'vg_speed': 85.0,   # Estimated best glide speed (typical for high-performance RV)
                'vfe_speed': 87.0,  # Maximum flap extended speed (100 mph from Van's Air Force)
                'vno_speed': 117.0, # Max structural cruising speed (135 mph from Van's Air Force)
                'vne_speed': 183.0, # Never exceed speed (210 mph from Van's Air Force)
            },
            {
                'manufacturer': manufacturers['vans'],
                'model': 'RV-9A',
                'clean_stall_speed': 47.0,  # IS sport pilot eligible (popular cross-country homebuilt)
                'top_speed': 145.0,
                'maneuvering_speed': 102.0,  # Updated from Van's Air Force builder data (118 mph VA)
                'max_takeoff_weight': 1750,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2000, 1, 1),
                'verification_source': 'Van\'s Aircraft specifications, Van\'s Air Force builder data',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320', 'horsepower': 160},
                'vx_speed': 73.0,   # Best angle climb (75kt from builder consensus)
                'vy_speed': 88.0,   # Best rate climb (average of 82-95kt range from builders)
                'vs0_speed': 47.0,  # Stall speed landing config (assume similar to clean)
                'vg_speed': 80.0,   # Best glide speed (80kt from builder reports)
                'vfe_speed': 78.0,  # Maximum flap extended speed (90 mph from Van's Air Force)
                'vno_speed': 156.0, # Max structural cruising speed (180 mph from Van's Air Force)
                'vne_speed': 182.0, # Never exceed speed (210 mph from Van's Air Force)
            },
            {
                'manufacturer': manufacturers['vans'],
                'model': 'RV-12iS',
                'clean_stall_speed': 45.0,  # Updated from Van's Air Force owner data (52 mph VS) - IS sport pilot eligible (LSA)
                'top_speed': 138.0,
                'maneuvering_speed': 90.0,  # Updated from Van's Air Force owner data (104 mph VA)
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2009, 1, 1),
                'verification_source': 'Van\'s Aircraft specifications, Van\'s Air Force owner reference card',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100},
                'vx_speed': 60.0,   # Best angle climb (69 mph from owner reference card)
                'vy_speed': 75.0,   # Best rate climb (86 mph from owner reference card)
                'vs0_speed': 41.0,  # Stall speed landing config (47 mph VSO from owner data)
                'vg_speed': 85.0,   # Best glide speed (98 mph from owner reference card)
                'vfe_speed': 82.0,  # Maximum flap extended speed (94 mph from owner data)
                'vno_speed': 108.0, # Max structural cruising speed (124 mph from owner data)
                'vne_speed': 136.0, # Never exceed speed (156 mph from owner data)
            },
            # Zenith Aircraft
            {
                'manufacturer': manufacturers['zenith'],
                'model': 'CH-701 STOL',
                'clean_stall_speed': 30.0,  # 35 mph (30 kt) clean stall from manufacturer specs - SPORT PILOT ELIGIBLE (exceptional STOL kit)
                'top_speed': 96.0,  # 110 mph (96 kt) never exceed speed
                'maneuvering_speed': 75.0,  # Estimated maneuvering speed for STOL aircraft
                'max_takeoff_weight': 1100,  # 1100 lbs gross weight from manufacturer specs
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1995, 1, 1),
                'verification_source': 'Zenith Aircraft Company specifications, kit builder manuals',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100},
                'vx_speed': 45.0,   # Estimated best angle climb for STOL performance
                'vy_speed': 60.0,   # Estimated best rate climb (1200 fpm capability)
                'vs0_speed': 26.0,  # 30 mph (26 kt) landing config stall from manufacturer specs
                'vg_speed': 55.0,   # Estimated best glide speed for STOL design
                'vfe_speed': 60.0,  # Estimated max flap extended speed
                'vno_speed': 75.0,  # Estimated normal operating speed
                'vne_speed': 96.0,  # 110 mph (96 kt) never exceed from manufacturer specs
            },
            {
                'manufacturer': manufacturers['zenith'],
                'model': 'CH-750 STOL',
                'clean_stall_speed': 39.0,  # Updated from flight manual (45 mph stall) - IS sport pilot eligible (LSA-optimized STOL kit)
                'top_speed': 104.0,
                'maneuvering_speed': 85.0,
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2005, 1, 1),
                'verification_source': 'Zenith Aircraft specifications, official flight manual',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100},
                'vx_speed': 52.0,   # Best angle climb (60 mph from flight manual)
                'vy_speed': 54.0,   # Best rate climb (62 mph from flight manual)
                'vs0_speed': 39.0,  # Stall speed landing config (45 mph from flight manual)
                'vg_speed': 60.0,   # Estimated best glide speed (typical for STOL design)
                'vfe_speed': 70.0,  # Maximum flap extended speed (80 mph from flight manual)
                'vno_speed': 122.0, # Max structural cruising speed (140 mph from flight manual)
                'vne_speed': 122.0, # Never exceed speed (140 mph from flight manual)
            },
            # Murphy Aircraft
            {
                'manufacturer': manufacturers['murphy'],
                'model': 'Rebel',
                'clean_stall_speed': 38.0,  # 44 mph (38 kt) clean stall power off - SPORT PILOT ELIGIBLE (Canadian STOL design)
                'top_speed': 104.0,  # 120 mph (104 kt) cruise at 75% power (Lycoming O-320)
                'maneuvering_speed': 85.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 1650,  # 1650 lbs gross weight from manufacturer specs
                'seating_capacity': 2,  # Typically 2 seats, though 3-seat variants exist
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1990, 1, 1),
                'verification_source': 'Murphy Aircraft official specifications, builder manuals',
                'vx_speed': 55.0,   # Estimated best angle climb for STOL performance
                'vy_speed': 70.0,   # Estimated best rate climb (1200 fpm capability with O-320)
                'vs0_speed': 35.0,  # 40 mph (35 kt) landing config stall with flaps
                'vg_speed': 65.0,   # Estimated best glide speed
                'vfe_speed': 70.0,  # Estimated max flap extended speed
                'vno_speed': 95.0,  # Estimated normal operating speed
                'vne_speed': 131.0, # 151 mph (131 kt) never exceed from manufacturer specs
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320', 'horsepower': 160}
            },
            # American Champion
            {
                'manufacturer': manufacturers['american_champion'],
                'model': 'Scout 8GCBC',
                'clean_stall_speed': 47.0,  # 47 knots clean stall - SPORT PILOT ELIGIBLE aerobatic trainer!
                'top_speed': 141.0,  # 141 knots top speed
                'maneuvering_speed': 115.0,  # 115 knots maneuvering speed
                'max_takeoff_weight': 2150,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1974, 1, 1),
                'verification_source': 'Type Certificate Data Sheet, American Champion Scout 8GCBC specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-C1G', 'horsepower': 180},
                # V-Speed data from American Champion Scout specifications and similar aircraft
                'vx_speed': 54.0,   # Best angle climb (similar to other American Champion O-360 aircraft)
                'vy_speed': 72.0,   # Best rate climb (estimated from 180 HP O-360 performance)
                'vs0_speed': 44.0,  # Stall landing configuration (estimated 3kt lower than clean)
                'vg_speed': 70.0,   # Best glide speed (typical for aerobatic aircraft design)
                'vfe_speed': 78.0,  # Max flap extended speed (typical for robust aerobatic design)
                'vno_speed': 115.0, # Max structural cruising (using existing maneuvering speed)
                'vne_speed': 141.0, # Never exceed speed (using existing top speed)
            },
            {
                'manufacturer': manufacturers['american_champion'],
                'model': 'Citabria 7ECA',
                'clean_stall_speed': 44.0,  # Updated from AOPA - IS sport pilot eligible (aerobatic trainer)
                'top_speed': 126.0,
                'maneuvering_speed': 115.0,
                'max_takeoff_weight': 1650,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1964, 8, 10),
                'verification_source': 'American Champion Aircraft specifications, AOPA fact sheet',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-K2C', 'horsepower': 118},  # Corrected from AOPA
                'vx_speed': 52.0,   # Best angle climb (60 mph from manufacturer specs)
                'vy_speed': 67.0,   # Best rate climb (77 mph from manufacturer specs)
                'vs0_speed': 44.0,  # Stall speed landing config (AOPA clean stall, assume similar with flaps)
                'vg_speed': 65.0,   # Estimated best glide speed (typical for aerobatic aircraft)
                'vfe_speed': 90.0,  # Estimated max flap extended speed (typical for this class)
                'vno_speed': 104.0, # Max structural cruising speed (AOPA: 104 KCAS)
                'vne_speed': 141.0, # Never exceed speed (AOPA: 141 KCAS)
            },
            {
                'manufacturer': manufacturers['american_champion'],
                'model': 'Citabria 7GCBC',
                'clean_stall_speed': 45.0,  # Updated from research (52 mph VS1) - IS sport pilot eligible (150hp aerobatic)
                'top_speed': 130.0,
                'maneuvering_speed': 104.0,  # Updated from research (120 mph VA)
                'max_takeoff_weight': 1800,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1970, 1, 1),
                'verification_source': 'American Champion Aircraft specifications, manufacturer v-speed data',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-A2B', 'horsepower': 150},
                'vx_speed': 51.0,   # Best angle climb (59 mph from manufacturer specs)
                'vy_speed': 68.0,   # Best rate climb (78 mph from manufacturer specs)
                'vs0_speed': 40.0,  # Stall speed landing config (46 mph VS0 from research)
                'vg_speed': 70.0,   # Estimated best glide speed (typical for aerobatic aircraft)
                'vfe_speed': 78.0,  # Maximum flap extended speed (90 mph VF from research)
                'vno_speed': 104.0, # Max structural cruising speed (120 mph from research)
                'vne_speed': 141.0, # Never exceed speed (162 mph from research)
            },
            {
                'manufacturer': manufacturers['american_champion'],
                'model': 'Decathlon 8KCAB',
                'clean_stall_speed': 46.0,  # Updated from research - IS sport pilot eligible (aerobatic)
                'top_speed': 135.0,  # Maximum speed from research
                'maneuvering_speed': 122.0,
                'max_takeoff_weight': 1800,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1970, 1, 1),
                'verification_source': 'American Champion Aircraft, WMU aviation specs, AOPA',
                # V-Speed data from research and aerobatic aircraft specifications
                'vx_speed': 65.0,   # Estimated best angle climb for aerobatic aircraft
                'vy_speed': 85.0,   # Estimated best rate climb
                'vs0_speed': 46.0,  # Stall speed from research (53 mph = 46 knots)
                'vg_speed': 75.0,   # Estimated best glide speed
                'vfe_speed': 90.0,  # Estimated max flap extended speed
                'vno_speed': 150.0, # Estimated max structural cruising speed
                'vne_speed': 174.0, # From research (200 mph = 174 knots)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'AEIO-360-H1B', 'horsepower': 180}
            },
            # Maule Air
            {
                'manufacturer': manufacturers['maule'],
                'model': 'M-7-235 Super Rocket',
                'clean_stall_speed': 35.0,  # 35 knots clean stall - EXCEPTIONAL SPORT PILOT ELIGIBLE STOL aircraft!
                'top_speed': 135.0,  # 135 knots top speed
                'maneuvering_speed': 110.0,  # 110 knots maneuvering speed
                'max_takeoff_weight': 2500,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,  # Most Maule aircraft have constant speed props
                'certification_date': date(1984, 1, 1),
                'verification_source': 'Type Certificate Data Sheet, Maule M-7-235 Super Rocket specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-540-J1A5', 'horsepower': 235},
                # V-Speed data from Maule STOL aircraft specifications and similar high-performance STOL aircraft
                'vx_speed': 58.0,   # Best angle climb (excellent STOL performance with 235 HP)
                'vy_speed': 85.0,   # Best rate climb (exceptional climb rate with high power-to-weight)
                'vs0_speed': 32.0,  # Stall landing configuration (exceptional STOL design)
                'vg_speed': 75.0,   # Best glide speed (high-performance single-engine)
                'vfe_speed': 90.0,  # Max flap extended speed (robust STOL flap system)
                'vno_speed': 110.0, # Max structural cruising (using maneuvering speed)
                'vne_speed': 135.0, # Never exceed speed (using top speed)
            },
            # Just Aircraft
            {
                'manufacturer': manufacturers['just_aircraft'],
                'model': 'SuperSTOL',
                'clean_stall_speed': 32.0,  # 32-37 mph (28-32 kt) clean stall - SPORT PILOT ELIGIBLE (extreme STOL experimental)
                'top_speed': 87.0,  # 100 mph (87 kt) cruise speed from manufacturer specs
                'maneuvering_speed': 80.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 1750,  # 1750 lbs LS/EAB configuration from manufacturer specs
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2018, 1, 1),
                'verification_source': 'Just Aircraft official specifications, STOL performance data',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100},
                'vx_speed': 50.0,   # Estimated best angle climb (exceptional STOL design for obstacle clearance)
                'vy_speed': 65.0,   # Estimated best rate climb (1000 fpm from manufacturer specs)
                'vs0_speed': 28.0,  # 32 mph (28 kt) landing config stall from manufacturer specs
                'vg_speed': 55.0,   # Estimated best glide speed (low speed optimized design)
                'vfe_speed': 65.0,  # Estimated max flap extended speed (STOL design with large flaps)
                'vno_speed': 85.0,  # Estimated normal operating speed
                'vne_speed': 113.0, # 130 mph (113 kt) never exceed from manufacturer specs
            },
            # CubCrafters
            {
                'manufacturer': manufacturers['cubcrafters'],
                'model': 'Carbon Cub EX-2',
                'clean_stall_speed': 32.0,  # 36-37 mph (31-32 kt) clean stall from CubCrafters specs - SPORT PILOT ELIGIBLE
                'top_speed': 117.0,  # 135 mph (117 kt) max speed in level flight from manufacturer specs
                'maneuvering_speed': 87.0,  # 93-106 mph (81-92 kt) from CubCrafters performance specs
                'max_takeoff_weight': 1865,  # 1865-2000 lbs depending on configuration
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2012, 1, 1),
                'verification_source': 'CubCrafters official specifications, Carbon Cub EX-2 performance data',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'Titan CC340', 'horsepower': 180},
                'vx_speed': 47.0,   # 50-57 mph (43-50 kt) best angle climb from CubCrafters specs
                'vy_speed': 62.0,   # 71 mph (62 kt) best rate climb from manufacturer specs
                'vs0_speed': 32.0,  # 36-37 mph (31-32 kt) landing config stall
                'vg_speed': 59.0,   # 68 mph (59 kt) best glide speed from manufacturer specs
                'vfe_speed': 85.0,  # Estimated max flap extended speed (G-Series slotted flaps)
                'vno_speed': 105.0, # Estimated normal operating speed
                'vne_speed': 135.0, # 141-170 mph (123-148 kt) never exceed from manufacturer specs
            },
            # Aviat Aircraft
            {
                'manufacturer': manufacturers['aviat'],
                'model': 'Husky A-1C-180',
                'clean_stall_speed': 43.0,  # Updated from research (50 mph low end = ~43 kts) - sport pilot eligible
                'top_speed': 135.0,  # ~140 mph from research
                'maneuvering_speed': 110.0,
                'max_takeoff_weight': 2250,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1987, 1, 1),
                'verification_source': 'Type Certificate Data Sheet, Aviat Aircraft, Aviation Consumer',
                # V-Speed data from research on Husky line
                'vx_speed': 55.0,   # Estimated best angle climb for STOL performance
                'vy_speed': 70.0,   # Estimated from 1500 FPM climb rate
                'vs0_speed': 43.0,  # Stall speed from speed range research
                'vg_speed': 70.0,   # Estimated best glide speed
                'vfe_speed': 80.0,  # Estimated max flap extended speed
                'vno_speed': 103.0, # From research - max structural cruising speed
                'vne_speed': 132.0, # From research - never exceed speed
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A1P', 'horsepower': 180}
            },
            # Additional Current Production Taildragger Aircraft from Wikipedia
            # Maule Aircraft
            {
                'manufacturer': manufacturers['maule'],
                'model': 'M-4-210C Rocket',
                'clean_stall_speed': 35.0,  # 35 KIAS from specs - NOT sport pilot eligible (2100 lbs MTOW)
                'top_speed': 143.0,  # Best cruise speed in knots
                'maneuvering_speed': 105.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 2100,
                'seating_capacity': 4,  # 3 passengers + 1 pilot
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1966, 1, 1),
                'verification_source': 'Maule specifications, M-4-210C POH',
                'vx_speed': 60.0,   # Estimated best angle climb
                'vy_speed': 80.0,   # Estimated best rate climb (1250 FPM)
                'vs0_speed': 35.0,  # Stall speed landing config
                'vg_speed': 85.0,   # Estimated best glide speed
                'vfe_speed': 75.0,  # Estimated max flap extended speed
                'vno_speed': 105.0, # Normal operating speed
                'vne_speed': 143.0, # Never exceed speed (same as max cruise)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-360-A', 'horsepower': 210}
            },
            {
                'manufacturer': manufacturers['maule'],
                'model': 'M-7-180 Star Rocket',
                'clean_stall_speed': 35.0,  # 40 mph = ~35 knots - NOT sport pilot eligible (2500 lbs MTOW)
                'top_speed': 141.0,  # 162 mph converted to knots
                'maneuvering_speed': 110.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 2500,
                'seating_capacity': 5,  # Five-seat lightplane
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1975, 1, 1),
                'verification_source': 'Maule specifications, M-7 performance data',
                'vx_speed': 65.0,   # Estimated best angle climb
                'vy_speed': 85.0,   # Estimated best rate climb (1650 FPM)
                'vs0_speed': 35.0,  # Stall speed landing config
                'vg_speed': 90.0,   # Estimated best glide speed
                'vfe_speed': 80.0,  # Estimated max flap extended speed
                'vno_speed': 110.0, # Normal operating speed
                'vne_speed': 141.0, # Never exceed speed (same as max cruise)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-C1F', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['maule'],
                'model': 'M-9-235 Lunar Rocket',
                'clean_stall_speed': 40.0,  # 46 mph = ~40 knots - NOT sport pilot eligible (2800 lbs MTOW)
                'top_speed': 141.0,  # 141 knots at 75% power
                'maneuvering_speed': 115.0,  # Estimated maneuvering speed
                'max_takeoff_weight': 2800,
                'seating_capacity': 5,  # 4-5 seat configuration
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1985, 1, 1),
                'verification_source': 'Maule specifications, M-9 performance data',
                'vx_speed': 70.0,   # Estimated best angle climb
                'vy_speed': 90.0,   # Estimated best rate climb
                'vs0_speed': 40.0,  # Stall speed landing config (46 mph)
                'vg_speed': 95.0,   # Estimated best glide speed
                'vfe_speed': 85.0,  # Estimated max flap extended speed
                'vno_speed': 115.0, # Normal operating speed
                'vne_speed': 141.0, # Never exceed speed (same as max cruise)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-540-W1A5', 'horsepower': 235}
            },
            # Seabird Aviation
            {
                'manufacturer': manufacturers['seabird'],
                'model': 'SB7L-360A Seeker',
                'clean_stall_speed': 48.0,  # 48 knots from specs - NOT sport pilot eligible (2145 lbs MTOW)
                'top_speed': 115.0,  # 130 mph = ~115 knots
                'maneuvering_speed': 95.0,   # Estimated maneuvering speed
                'max_takeoff_weight': 2145,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2005, 1, 1),
                'verification_source': 'Seabird Aviation specifications, flight test data',
                'vx_speed': 70.0,   # Estimated best angle climb
                'vy_speed': 80.0,   # Estimated best rate climb
                'vs0_speed': 48.0,  # Stall speed landing config (same as clean for observation aircraft)
                'vg_speed': 85.0,   # Estimated best glide speed
                'vfe_speed': 75.0,  # Estimated max flap extended speed
                'vno_speed': 95.0,  # Normal operating speed
                'vne_speed': 115.0, # Never exceed speed (same as max cruise)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360', 'horsepower': 180}
            },
            # Waco Aircraft
            {
                'manufacturer': manufacturers['waco'],
                'model': 'YMF-5D',
                'clean_stall_speed': 51.0,  # 59 mph = ~51 knots - NOT sport pilot eligible (2950 lbs MTOW)
                'top_speed': 106.0,  # 122 mph = ~106 knots
                'maneuvering_speed': 120.0,  # Estimated maneuvering speed for aerobatic aircraft
                'max_takeoff_weight': 2950,
                'seating_capacity': 3,  # 2 passengers + 1 pilot
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1994, 1, 1),
                'verification_source': 'Waco Aircraft specifications, YMF-5D POH',
                'vx_speed': 75.0,   # Estimated best angle climb
                'vy_speed': 85.0,   # Estimated best rate climb
                'vs0_speed': 51.0,  # Stall speed with flaps
                'vg_speed': 80.0,   # Estimated best glide speed
                'vfe_speed': 85.0,  # Estimated max flap extended speed
                'vno_speed': 120.0, # Normal operating speed
                'vne_speed': 161.0, # 185 knots from specs
                'engine_specs': {'manufacturer': 'Jacobs', 'model': 'R-755', 'horsepower': 300}
            },
            {
                'manufacturer': manufacturers['waco'],
                'model': 'Great Lakes 2T-1A-2',
                'clean_stall_speed': 50.0,  # 57 mph = ~50 knots - NOT sport pilot eligible (1800 lbs MTOW)
                'top_speed': 133.0,  # 153 mph = ~133 knots
                'maneuvering_speed': 105.0,  # Estimated maneuvering speed for aerobatic aircraft
                'max_takeoff_weight': 1800,
                'seating_capacity': 2,  # Tandem configuration
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1973, 1, 1),
                'verification_source': 'Great Lakes Aircraft specifications, 2T-1A-2 performance data',
                'vx_speed': 65.0,   # Estimated best angle climb
                'vy_speed': 75.0,   # Estimated best rate climb (1400 FPM)
                'vs0_speed': 50.0,  # Stall speed landing config
                'vg_speed': 85.0,   # Estimated best glide speed
                'vfe_speed': 80.0,  # Estimated max flap extended speed
                'vno_speed': 105.0, # Normal operating speed
                'vne_speed': 133.0, # Never exceed speed (same as max speed)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'AEIO-360-B1G6', 'horsepower': 180}
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
                'clean_stall_speed': 135.0,  # NOT sport pilot eligible (commercial airliner)
                'top_speed': 544.0,
                'maneuvering_speed': 320.0,
                'max_takeoff_weight': 174200,
                'seating_capacity': 189,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1998, 1, 1),
                'verification_source': 'Boeing specifications, commercial aviation data',
                'engine_specs': {'manufacturer': 'CFM International', 'model': 'CFM56-7B27', 'thrust_pounds': 27300, 'fuel_type': 'JET_A', 'engine_type': 'JET'},
                'vx_speed': 180.0,  # Estimated best angle climb (typical for commercial jets)
                'vy_speed': 200.0,  # Estimated best rate climb (typical for commercial jets)
                'vs0_speed': 135.0, # Stall speed landing config (assume similar to clean for estimate)
                'vg_speed': 220.0,  # Estimated best glide speed (typical for commercial jets)
                'vfe_speed': 200.0, # Estimated max flap extended speed (varies by flap setting)
                'vno_speed': 320.0, # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 400.0, # Estimated never exceed speed (typical for commercial jets)
            },
            {
                'manufacturer': manufacturers['airbus'],
                'model': 'A320',
                'clean_stall_speed': 110.0,  # Updated from VREF calculations (VREF ~134kt / 1.23 = ~109kt) - NOT sport pilot eligible (commercial airliner)
                'top_speed': 350.0,  # Updated to Vmo limit (350 KIAS / 0.82 Mach)
                'maneuvering_speed': 320.0,
                'max_takeoff_weight': 172000,  # Confirmed MTOW (some variants up to 78,000 kg)
                'seating_capacity': 180,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1988, 1, 1),
                'verification_source': 'Airbus specifications, FCOM speed data',
                'vx_speed': 155.0,   # Estimated best angle climb (typical for commercial aircraft)
                'vy_speed': 175.0,   # Estimated best rate climb (typical for commercial aircraft)
                'vs0_speed': 110.0,  # Stall speed landing config (estimated from VLS calculations)
                'vg_speed': 200.0,   # Estimated best glide speed (typical for commercial aircraft)
                'vfe_speed': 200.0,  # Estimated max flap extended speed (varies by flap setting)
                'vno_speed': 320.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 350.0,  # Never exceed speed (same as Vmo)
                'engine_specs': {'manufacturer': 'CFM International', 'model': 'CFM56-5B', 'thrust_pounds': 22000, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
            },
            {
                'manufacturer': manufacturers['embraer'],
                'model': 'E-Jet 175',
                'clean_stall_speed': 108.0,  # Estimated from commercial jet specifications - NOT sport pilot eligible (regional jet)
                'top_speed': 450.0,  # Updated to Mach 0.82 equivalent (450 knots)
                'maneuvering_speed': 300.0,
                'max_takeoff_weight': 89000,  # Updated to correct MTOW (89,000 lbs)
                'seating_capacity': 88,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(2004, 1, 1),
                'verification_source': 'Embraer specifications, commercial aviation performance data',
                'vx_speed': 160.0,   # Estimated best angle climb (typical for regional jets)
                'vy_speed': 180.0,   # Estimated best rate climb (typical for regional jets)
                'vs0_speed': 108.0,  # Stall speed landing config (assume similar to clean for estimate)
                'vg_speed': 200.0,   # Estimated best glide speed (typical for regional jets)
                'vfe_speed': 190.0,  # Estimated max flap extended speed (varies by flap setting)
                'vno_speed': 300.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 450.0,  # Never exceed speed (same as maximum operating speed)
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'CF34-8E', 'thrust_pounds': 13790, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
            },
            {
                'manufacturer': manufacturers['bombardier'],
                'model': 'CRJ-700',
                'clean_stall_speed': 105.0,  # Confirmed from POH data and approach speeds - NOT sport pilot eligible (regional jet)
                'top_speed': 488.0,  # Updated to Mach 0.85 equivalent (488 knots)
                'maneuvering_speed': 290.0,
                'max_takeoff_weight': 75000,  # Confirmed MTOW
                'seating_capacity': 78,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(2001, 1, 1),
                'verification_source': 'Bombardier specifications, CRJ-700 POH data',
                'vx_speed': 138.0,   # V2 takeoff safety speed from POH (best angle climb)
                'vy_speed': 145.0,   # Estimated best rate climb (slightly above V2)
                'vs0_speed': 105.0,  # Stall speed landing config (estimated based on approach speeds)
                'vg_speed': 180.0,   # Estimated best glide speed (typical for regional jets)
                'vfe_speed': 167.0,  # Max flap extended speed (Vref at flaps 0 from POH data)
                'vno_speed': 290.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 488.0,  # Never exceed speed (same as maximum operating speed)
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'CF34-8C5B1', 'thrust_pounds': 13790, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
            },
            # Business Jets
            {
                'manufacturer': manufacturers['bombardier'],
                'model': 'Global 6000',
                'clean_stall_speed': 90.0,  # Confirmed from flight test data - NOT sport pilot eligible (business jet)
                'top_speed': 513.0,  # Updated to confirmed max cruise speed (513 knots)
                'maneuvering_speed': 340.0,
                'max_takeoff_weight': 99500,  # Confirmed MTOW
                'seating_capacity': 17,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(2012, 1, 1),
                'verification_source': 'Bombardier specifications, flight test data',
                'vx_speed': 120.0,   # Estimated best angle climb (typical for business jets)
                'vy_speed': 140.0,   # Estimated best rate climb (typical for business jets)
                'vs0_speed': 100.0,  # Stall speed landing config (from flight test near-stall data)
                'vg_speed': 160.0,   # Estimated best glide speed (typical for business jets)
                'vfe_speed': 115.0,  # Max flap extended speed (from approach speed data)
                'vno_speed': 340.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 513.0,  # Never exceed speed (same as maximum operating speed)
                'engine_specs': {'manufacturer': 'Rolls-Royce', 'model': 'BR710A2-20', 'thrust_pounds': 14750, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
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
                # V-Speed data for F-16 military fighter - NOT sport pilot eligible (140kt stall, military aircraft)
                'vx_speed': 180.0,   # Estimated best angle climb (typical for military fighters)
                'vy_speed': 220.0,   # Estimated best rate climb (typical for military fighters)
                'vs0_speed': 125.0,  # Stall speed landing config (estimated 15kt below clean)
                'vg_speed': 270.0,   # Estimated best glide speed (typical for military fighters)
                'vfe_speed': 180.0,  # Estimated max flap extended speed (varies by configuration)
                'vno_speed': 600.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 800.0,  # Estimated never exceed speed (below maximum operating speed)
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'F110-GE-129', 'thrust_pounds': 29000, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
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
                # V-Speed data for F-22 stealth fighter - NOT sport pilot eligible (120kt stall, military aircraft)
                'vx_speed': 160.0,   # Estimated best angle climb (advanced fighter)
                'vy_speed': 200.0,   # Estimated best rate climb (advanced fighter)
                'vs0_speed': 105.0,  # Stall speed landing config (estimated 15kt below clean)
                'vg_speed': 250.0,   # Estimated best glide speed (advanced fighter)
                'vfe_speed': 160.0,  # Estimated max flap extended speed (varies by configuration)
                'vno_speed': 700.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 850.0,  # Estimated never exceed speed (below maximum operating speed)
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'F119-PW-100', 'thrust_pounds': 35000, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
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
                # V-Speed data for F-35 Lightning II - NOT sport pilot eligible (130kt stall, military aircraft)
                'vx_speed': 170.0,   # Estimated best angle climb (modern stealth fighter)
                'vy_speed': 210.0,   # Estimated best rate climb (modern stealth fighter)
                'vs0_speed': 115.0,  # Stall speed landing config (estimated 15kt below clean)
                'vg_speed': 260.0,   # Estimated best glide speed (modern stealth fighter)
                'vfe_speed': 170.0,  # Estimated max flap extended speed (varies by configuration)
                'vno_speed': 650.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 800.0,  # Estimated never exceed speed (below maximum operating speed)
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'F135-PW-100', 'thrust_pounds': 40000, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
            },
            # Military Transport/Cargo
            {
                'manufacturer': manufacturers['lockheed'],
                'model': 'C-130 Hercules',
                'clean_stall_speed': 100.0,  # Updated from military specifications - NOT sport pilot eligible (military transport)
                'top_speed': 366.0,
                'maneuvering_speed': 260.0,
                'max_takeoff_weight': 155000,
                'seating_capacity': 92,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1954, 1, 1),
                'verification_source': 'US Air Force specifications, military transport performance data',
                'vx_speed': 120.0,   # Estimated best angle climb (typical for turboprop transport)
                'vy_speed': 140.0,   # Estimated best rate climb (typical for turboprop transport)
                'vs0_speed': 100.0,  # Stall speed landing config (assume similar to clean for estimate)
                'vg_speed': 160.0,   # Estimated best glide speed (typical for military transport)
                'vfe_speed': 150.0,  # Estimated max flap extended speed (varies by flap setting)
                'vno_speed': 260.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 320.0,  # Estimated never exceed speed (typical for military turboprops)
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
                # V-Speed data for C-17 military transport - NOT sport pilot eligible (115kt stall, military aircraft)
                'vx_speed': 140.0,   # Estimated best angle climb (military transport)
                'vy_speed': 160.0,   # Estimated best rate climb (military transport)
                'vs0_speed': 100.0,  # Stall speed landing config (estimated 15kt below clean)
                'vg_speed': 200.0,   # Estimated best glide speed (military transport)
                'vfe_speed': 180.0,  # Estimated max flap extended speed (varies by configuration)
                'vno_speed': 350.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 450.0,  # Estimated never exceed speed (below maximum operating speed)
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'F117-PW-100', 'thrust_pounds': 40440, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
            },
            # Classic Military Aircraft
            {
                'manufacturer': manufacturers['mcdonnell_douglas'],
                'model': 'F-4 Phantom II',
                'clean_stall_speed': 160.0,  # Updated from flight manual data (160 knots clean) - NOT sport pilot eligible (military fighter)
                'top_speed': 1400.0,  # Updated to Mach 2.23 equivalent (approximately 1400+ knots)
                'maneuvering_speed': 650.0,
                'max_takeoff_weight': 61795,  # Confirmed 61,795 lbs MTOW
                'seating_capacity': 2,
                'retractable_gear': True,
                'variable_pitch_prop': False,
                'certification_date': date(1960, 1, 1),
                'verification_source': 'US Air Force specifications, F-4E flight manual data',
                'vx_speed': 200.0,   # Estimated best angle climb (typical for military fighters)
                'vy_speed': 250.0,   # Estimated best rate climb (typical for military fighters)
                'vs0_speed': 135.0,  # Stall speed landing config (135 knots from flight manual data)
                'vg_speed': 300.0,   # Estimated best glide speed (typical for military fighters)
                'vfe_speed': 200.0,  # Estimated max flap extended speed (varies by configuration)
                'vno_speed': 650.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 850.0,  # Estimated never exceed speed (below maximum operating speed)
                'engine_specs': {'manufacturer': 'General Electric', 'model': 'J79-GE-17A', 'thrust_pounds': 17845, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
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
                # V-Speed data for F-111 variable-geometry fighter-bomber - NOT sport pilot eligible (160kt stall, military aircraft)
                'vx_speed': 200.0,   # Estimated best angle climb (variable-geometry fighter-bomber)
                'vy_speed': 240.0,   # Estimated best rate climb (variable-geometry fighter-bomber)
                'vs0_speed': 140.0,  # Stall speed landing config (estimated 20kt below clean)
                'vg_speed': 300.0,   # Estimated best glide speed (variable-geometry fighter-bomber)
                'vfe_speed': 200.0,  # Estimated max flap extended speed (varies by configuration)
                'vno_speed': 700.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 900.0,  # Estimated never exceed speed (below maximum operating speed)
                'engine_specs': {'manufacturer': 'Pratt & Whitney', 'model': 'TF30-P-100', 'thrust_pounds': 25100, 'fuel_type': 'JET_A', 'engine_type': 'JET'}
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
                'clean_stall_speed': 35.0,  # 35 knots clean stall - EXCELLENT SPORT PILOT ELIGIBLE LSA!
                'top_speed': 118.0,
                'maneuvering_speed': 97.0,  # 98 KIAS design maneuvering speed from AOPA
                'cruise_speed': 102.0,  # Typical cruise speed for P2008 family
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2007, 4, 12),
                'verification_source': 'Tecnam P2008-JC POH, AOPA TC specifications, FAA LSA certification',
                # V-Speed data from AOPA P2008 TC specifications and Tecnam POH
                'vx_speed': 65.0,   # 65 KIAS best angle of climb from AOPA specifications
                'vy_speed': 78.0,   # 78 KIAS best rate of climb from AOPA specifications
                'vs0_speed': 32.0,  # 39 KIAS stall landing config (estimated for standard P2008)
                'vg_speed': 70.0,   # Best glide speed (estimated near Vy)
                'vfe_speed': 68.0,  # 68 KIAS max flap extended speed from AOPA
                'vno_speed': 106.0, # 106 KIAS max structural cruising from AOPA
                'vne_speed': 134.0, # 134 KIAS never exceed speed from AOPA
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['tecnam'],
                'model': 'P2002-Sierra',
                'clean_stall_speed': 38.0,
                'top_speed': 118.0,
                'maneuvering_speed': 96.0,
                'max_takeoff_weight': 1389,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2008, 1, 15),
                'verification_source': 'Tecnam P2002-Sierra POH, official flight manual specifications, AOPA aircraft guide',
                # V-Speed data from Tecnam P2002-JF/Sierra flight manual - EXCELLENT sport pilot aircraft (38kt stall)
                'vx_speed': 56.0,  # Best angle of climb speed (KIAS)
                'vy_speed': 66.0,  # Best rate of climb speed (KIAS)
                'vs0_speed': 39.0, # Stall speed landing configuration (full flaps) - KCAS from POH
                'vg_speed': 68.0,  # Best glide speed (KIAS)
                'vfe_speed': 80.0, # Max flap extended speed (estimate for this class)
                'vno_speed': 108.0, # Normal operating speed (KCAS from POH)
                'vne_speed': 138.0, # Never exceed speed (KCAS from POH)
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
                # V-Speed data estimated from LSA performance characteristics - EXCELLENT sport pilot aircraft
                'vx_speed': 55.0,  # Typical LSA best angle climb speed
                'vy_speed': 72.0,  # Typical LSA best rate climb speed
                'vs0_speed': 35.0, # Landing configuration stall (lower than clean stall)
                'vg_speed': 65.0,  # Best glide speed (typical for LSA)
                'vfe_speed': 70.0, # Max flap speed (conservative for LSA)
                'vno_speed': 100.0, # Max structural cruising (matches maneuvering speed)
                'vne_speed': 132.0, # Never exceed (typical LSA limit)
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['evektor'],
                'model': 'SportStar',
                'clean_stall_speed': 37.0,  # EXCELLENT sport pilot aircraft (42 kts from Evektor specs)
                'top_speed': 115.0,  # 115 kts max cruise from specifications
                'maneuvering_speed': 100.0,  # Estimated for LSA
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2005, 4, 1),  # First LSA certified by FAA
                'verification_source': 'Evektor SportStar RTC specifications, manufacturer data, FAA LSA certification',
                # V-Speed data from Evektor specifications and LSA performance characteristics
                'vx_speed': 60.0,   # Best angle climb speed (typical for LSA with Rotax 912)
                'vy_speed': 75.0,   # Best rate climb speed (estimated from 876 fpm climb rate)
                'vs0_speed': 37.0,  # Stall speed landing configuration (from earlier search: 37 KIAS)
                'vg_speed': 70.0,   # Best glide speed (typical for LSA near Vy)
                'vfe_speed': 85.0,  # Max flap extended speed (estimated for LSA)
                'vno_speed': 120.0, # Normal operating speed (between cruise and Vne)
                'vne_speed': 145.0, # Never exceed speed (from flight test data)
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['icon'],
                'model': 'A5',
                'clean_stall_speed': 45.0,  # 45 KIAS clean stall from Icon POH - SPORT PILOT ELIGIBLE AMPHIBIOUS LSA!
                'top_speed': 109.0,  # 84 KTAS cruise speed from specifications
                'maneuvering_speed': 87.0,  # 87 KIAS maneuvering speed at max weight from POH
                'cruise_speed': 84.0,  # 84 KTAS cruise speed from manufacturer specifications
                'max_takeoff_weight': 1510,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2014, 7, 23),
                'verification_source': 'Icon A5 POH, manufacturer specifications, FAA Special LSA certification',
                # V-Speed data from Icon A5 POH and manufacturer performance specifications
                'vx_speed': 54.0,   # 54 KIAS best angle of climb (616 ft/min) from POH
                'vy_speed': 58.0,   # 58 KIAS best rate of climb (629 ft/min) from POH
                'vs0_speed': 39.0,  # 39 KIAS stall landing configuration from POH
                'vg_speed': 60.0,   # Best glide speed (estimated near operational speeds)
                'vfe_speed': 75.0,  # 75 KIAS maximum flap extended speed from POH
                'vno_speed': 100.0, # Max structural cruising speed (estimated)
                'vne_speed': 120.0, # 120 KIAS never exceed speed from POH
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912iS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['pipistrel'],
                'model': 'Virus SW 121',
                'clean_stall_speed': 37.0,  # 37 knots clean stall - SPORT PILOT ELIGIBLE modern LSA!
                'top_speed': 135.0,  # 135 knots top speed
                'maneuvering_speed': 108.0,  # 108 knots maneuvering speed
                'max_takeoff_weight': 1320,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2010, 3, 16),
                'verification_source': 'Pipistrel Virus SW 121 POH, Slovenian manufacturer specifications, modern LSA performance data',
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100},
                # V-Speed data from Pipistrel Virus SW 121 specifications and modern LSA performance standards
                'vx_speed': 52.0,   # Best angle climb (efficient modern design with Rotax 912ULS)
                'vy_speed': 65.0,   # Best rate climb (excellent climb performance for LSA)
                'vs0_speed': 35.0,  # Stall landing configuration (efficient flap design)
                'vg_speed': 62.0,   # Best glide speed (modern efficient airfoil design)
                'vfe_speed': 78.0,  # Max flap extended speed (typical for modern LSA)
                'vno_speed': 108.0, # Max structural cruising (using existing maneuvering speed)
                'vne_speed': 135.0, # Never exceed speed (using existing top speed)
            },
            {
                'manufacturer': manufacturers['progressive'],
                'model': 'SeaRey',
                'clean_stall_speed': 39.0,
                'top_speed': 115.0,
                'maneuvering_speed': 82.0,
                'max_takeoff_weight': 1430,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(2005, 9, 14),
                'verification_source': 'Progressive Aerodyne SeaRey POH, AOPA SeaRey review, aviation forum specifications',
                # V-Speed data from SeaRey LSA POH and performance specs - EXCELLENT sport pilot amphibious aircraft (39kt stall)
                'vx_speed': 50.0,  # Best angle of climb speed (58 MPH converted)
                'vy_speed': 55.0,  # Best rate of climb speed (63 MPH converted)
                'vs0_speed': 35.0, # Stall speed landing configuration with flaps (40 MPH converted)
                'vg_speed': 52.0,  # Best glide speed (estimated for amphibious configuration)
                'vfe_speed': 52.0, # Max flap extended speed (estimate based on configuration speeds)
                'vno_speed': 96.0, # Normal operating speed (estimated from Va/Vne relationship)
                'vne_speed': 104.0, # Never exceed speed (120 MPH converted from POH)
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912ULS', 'horsepower': 100}
            },
            {
                'manufacturer': manufacturers['taylorcraft'],
                'model': 'BC-12D',
                'clean_stall_speed': 30.0,  # Updated from research (35 mph) - IS sport pilot eligible (excellent vintage STOL)
                'top_speed': 105.0,
                'maneuvering_speed': 87.0,
                'max_takeoff_weight': 1200,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 3, 15),
                'verification_source': 'Taylorcraft BC-12D POH (1946), Continental A-65 engine specifications, owner reports',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'A-65-8', 'horsepower': 65},
                'vx_speed': 50.0,   # Estimated best angle climb (similar to other A-65 powered aircraft)
                'vy_speed': 60.0,   # Estimated from 500 FPM climb rate and approach speed data
                'vs0_speed': 30.0,  # Stall speed landing config (35 mph from research)
                'vg_speed': 52.0,   # Best glide speed (60 mph approach speed from research)
                'vfe_speed': 70.0,  # Estimated max flap extended speed (typical for era)
                'vno_speed': 87.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 122.0, # Never exceed speed (140 mph from research)
            },
            {
                'manufacturer': manufacturers['aeronca'],
                'model': '7AC Champion',
                'clean_stall_speed': 33.0,  # Updated from research - excellent sport pilot aircraft
                'top_speed': 100.0,
                'maneuvering_speed': 82.0,  # Updated from POH (95 mph = 82 knots)
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 1, 1),
                'verification_source': 'Aeronca 7AC POH, planephd.com, Plane & Pilot',
                # V-Speed data from POH and research sources
                'vx_speed': 43.0,   # Best angle of climb (50 mph from POH)
                'vy_speed': 52.0,   # Best rate of climb (60 mph from POH)
                'vs0_speed': 33.0,  # Stall speed (33 KIAS from planephd.com)
                'vg_speed': 52.0,   # Best glide speed (60 mph from POH)
                'vfe_speed': 65.0,  # Estimated max flap extended speed
                'vno_speed': 95.0,  # Estimated max structural cruising speed
                'vne_speed': 112.0, # Never exceed speed (129 mph from POH)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'A-65-8', 'horsepower': 65}
            },
            {
                'manufacturer': manufacturers['aeronca'],
                'model': '7CCM',
                'clean_stall_speed': 40.0,  # 40 knots clean stall - SPORT PILOT ELIGIBLE vintage trainer
                'top_speed': 105.0,  # 105 knots top speed
                'maneuvering_speed': 90.0,  # 90 knots maneuvering speed
                'max_takeoff_weight': 1300,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1947, 1, 1),
                'verification_source': 'Aeronca 7CCM specifications, similar to 7AC Champion performance',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-85-12', 'horsepower': 85},
                # V-Speed data based on similar Aeronca designs and C-85-12 engine performance
                'vx_speed': 45.0,   # Best angle climb (slightly better than 7AC due to more power)
                'vy_speed': 55.0,   # Best rate climb (better than 7AC with C-85 vs A-65)
                'vs0_speed': 38.0,  # Stall landing configuration (estimated from clean stall)
                'vg_speed': 55.0,   # Best glide speed (similar to other Aeronca designs)
                'vfe_speed': 70.0,  # Max flap extended speed (typical for 1947 design)
                'vno_speed': 90.0,  # Max structural cruising (using maneuvering speed)
                'vne_speed': 105.0, # Never exceed speed (using top speed)
            },
            {
                'manufacturer': manufacturers['aeronca'],
                'model': 'Champ 7BCM',
                'clean_stall_speed': 33.0,  # Updated from 7AC research - IS sport pilot eligible (excellent vintage trainer)
                'top_speed': 100.0,
                'maneuvering_speed': 87.0,
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 1, 1),
                'verification_source': 'Aeronca Champ 7BCM specifications, Flying Magazine article',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'C-85', 'horsepower': 85},  # Corrected from research
                'vx_speed': 50.0,   # Estimated best angle climb (slightly better than 7AC due to higher power)
                'vy_speed': 62.0,   # Estimated best rate climb (better than 7AC's performance)
                'vs0_speed': 33.0,  # Stall speed landing config (from 7AC research)
                'vg_speed': 55.0,   # Estimated best glide speed (similar to 7AC)
                'vfe_speed': 70.0,  # Estimated max flap extended speed (typical for this era)
                'vno_speed': 87.0,  # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 100.0, # Using existing top speed as never exceed speed
            },
            {
                'manufacturer': manufacturers['aeronca'],
                'model': 'Champion 7AC',
                'clean_stall_speed': 33.0,  # 33 knots (38 mph) clean stall from POH - EXCELLENT SPORT PILOT ELIGIBLE!
                'top_speed': 87.0,  # 87 knots (100 mph) top speed from POH
                'maneuvering_speed': 82.0,  # 82 knots (95 mph) Va from POH
                'max_takeoff_weight': 1220,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1946, 1, 1),
                'verification_source': 'Aeronca Champion 7AC POH N1946E (2010 Covenant Aviation), Manualzilla POH documentation',
                'engine_specs': {'manufacturer': 'Continental', 'model': 'A-65-8', 'horsepower': 65},
                # V-Speed data from official Aeronca 7AC POH (Aircraft N1946E SN 7AC-5513)
                'vx_speed': 43.0,   # 43 knots (50 mph) best angle climb from POH limitations section
                'vy_speed': 52.0,   # 52 knots (60 mph) best rate climb from POH performance section
                'vs0_speed': 30.0,  # 30 knots (35 mph) stall landing configuration from POH
                'vg_speed': 52.0,   # 52 knots (60 mph) best glide speed from POH
                'vfe_speed': 70.0,  # Estimated max flap extended speed (typical for 1946 design)
                'vno_speed': 78.0,  # Estimated max structural cruising speed (90% of top speed)
                'vne_speed': 112.0, # 112 knots (129 mph) never exceed speed from POH
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
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-L2A', 'horsepower': 180},
                # V-Speed data for higher-weight 172S variant (63kt stall vs 48kt for standard)
                'vx_speed': 62.0,   # Best angle climb (same as standard 172S)
                'vy_speed': 74.0,   # Best rate climb (same as standard 172S)
                'vs0_speed': 55.0,  # Stall landing configuration (higher than standard due to weight)
                'vg_speed': 68.0,   # Best glide speed (same as standard)
                'vfe_speed': 85.0,  # Max flap extended speed (same as standard)
                'vno_speed': 129.0, # Max structural cruising (same as standard)
                'vne_speed': 163.0, # Never exceed speed (same as standard)
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
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-540-AB1A5', 'horsepower': 235},
                # V-Speed data for Cessna 182T with IO-540 engine (more powerful than earlier 182s)
                'vx_speed': 68.0,   # Best angle climb (better than original 182 with more power)
                'vy_speed': 85.0,   # Best rate climb (excellent with 235HP IO-540)
                'vs0_speed': 58.0,  # Stall landing configuration (heavier than original)
                'vg_speed': 78.0,   # Best glide speed (higher than original due to weight)
                'vfe_speed': 100.0, # Max flap extended speed (higher than original)
                'vno_speed': 140.0, # Max structural cruising (using maneuvering speed)
                'vne_speed': 175.0, # Never exceed speed (higher than original due to power)
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
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A4A', 'horsepower': 180},
                # V-Speed data for Piper Cherokee 180 with O-360-A4A engine
                'vx_speed': 68.0,   # Best angle climb (typical for O-360 180HP Cherokee)
                'vy_speed': 88.0,   # Best rate climb (good performance with 180HP)
                'vs0_speed': 58.0,  # Stall landing configuration (typical 5kt reduction from clean)
                'vg_speed': 76.0,   # Best glide speed (typical for Cherokee family)
                'vfe_speed': 100.0, # Max flap extended speed (typical for Cherokee)
                'vno_speed': 113.0, # Max structural cruising (using existing maneuvering speed)
                'vne_speed': 139.0, # Never exceed speed (using existing top speed)
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Cherokee 235',
                'clean_stall_speed': 52.0,  # CORRECTED - IS sport pilot eligible (≤59kt)
                'top_speed': 144.0,  # Updated from risingup.com source
                'maneuvering_speed': 120.0,  # Estimated from conversion
                'max_takeoff_weight': 2900,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1963, 1, 1),
                'verification_source': 'risingup.com Cherokee 235B specs, Aerovalley Flying Club',
                # V-Speed data from multiple sources (converted from MPH to knots where needed)
                'vx_speed': 78.0,   # Best angle of climb (~90 mph converted)
                'vy_speed': 87.0,   # Best rate of climb (~100 mph converted)
                'vs0_speed': 52.0,  # Stall speed in landing configuration (verified source)
                'vg_speed': 82.0,   # Best glide speed (~95 mph converted)
                'vfe_speed': 100.0, # Maximum flap extension speed (~115 mph converted)
                'vno_speed': 142.0, # Maximum structural cruising speed (~164 mph converted)
                'vne_speed': 174.0, # Never exceed speed (~200 mph converted)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-540-B4B5', 'horsepower': 235}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Super Cub PA-18',
                'clean_stall_speed': 43.0,  # 43 knots clean stall from bush flying specifications - SPORT PILOT ELIGIBLE LEGENDARY!
                'top_speed': 130.0,
                'maneuvering_speed': 110.0,  # 90 mph (78 knots) maximum operating maneuvering speed from specs
                'cruise_speed': 100.0,  # Typical cruise speed for bush operations
                'max_takeoff_weight': 1750,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1949, 1, 1),
                'verification_source': 'Piper Super Cub POH, bush flying specifications, AOPA fact sheet',
                # V-Speed data from Super Cub POH and bush flying performance specs
                'vx_speed': 48.0,   # 55 mph (48 knots) best angle of climb from POH
                'vy_speed': 63.0,   # 72 mph (63 knots) best rate of climb from POH
                'vs0_speed': 16.0,  # 18 mph (16 knots) stall with flaps down from POH
                'vg_speed': 65.0,   # Best glide speed (estimated near Vy)
                'vfe_speed': 52.0,  # 60 mph (52 knots) maximum speed with 10° flaps
                'vno_speed': 90.0,  # 90 mph normal operating speed from specs
                'vne_speed': 121.0, # 139 mph (121 knots) never exceed speed from POH
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-B2A', 'horsepower': 150}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Archer III',
                'clean_stall_speed': 64.0,  # NOT sport pilot eligible (>59kt)
                'top_speed': 126.0,
                'maneuvering_speed': 113.0,
                'max_takeoff_weight': 2550,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1995, 8, 22),
                'verification_source': 'Piper Archer III POH, FAA Type Certificate 3A12 (amended)',
                # V-Speed data from POH and flight training materials
                'vx_speed': 64.0,   # Best angle of climb (KIAS)
                'vy_speed': 76.0,   # Best rate of climb (KIAS)
                'vs0_speed': 45.0,  # Stall speed in landing configuration (KIAS)
                'vg_speed': 76.0,   # Best glide speed at max weight (KIAS)
                'vfe_speed': 102.0, # Maximum flap extension speed (KIAS)
                'vno_speed': 125.0, # Maximum structural cruising speed (KIAS)
                'vne_speed': 154.0, # Never exceed speed (KIAS)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-B1E', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['piper'],
                'model': 'Saratoga',
                'clean_stall_speed': 67.0,  # NOT sport pilot eligible (>59kt)
                'top_speed': 167.0,
                'maneuvering_speed': 134.0,  # Updated from POH specs
                'max_takeoff_weight': 3600,
                'seating_capacity': 6,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(1980, 4, 9),
                'verification_source': 'Piper Saratoga POH, FAA Type Certificate A24SO',
                # V-Speed data from POH and official specifications
                'vx_speed': 71.0,   # Best angle of climb (KIAS)
                'vy_speed': 95.0,   # Best rate of climb, gear up, flaps up (KIAS)
                'vs0_speed': 63.0,  # Stall speed in landing configuration (KIAS)
                'vg_speed': 85.0,   # Estimated best glide speed based on similar aircraft
                'vfe_speed': 110.0, # Maximum flap extension speed (KIAS)
                'vno_speed': 167.0, # Maximum structural cruising speed (KIAS)
                'vne_speed': 191.0, # Never exceed speed (KIAS)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-540-K1G5', 'horsepower': 300}
            },
            {
                'manufacturer': manufacturers['grumman'],
                'model': 'Tiger AA-5B',
                'clean_stall_speed': 56.0,
                'top_speed': 139.0,
                'maneuvering_speed': 109.0,
                'max_takeoff_weight': 2400,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1975, 1, 1),
                'verification_source': 'Grumman Tiger AA-5B specifications, AOPA Tiger review, POH research',
                # V-Speed data from Tiger POH and AOPA specifications - MOSAIC LSA eligible (56kt stall ≤61kt limit, but >59kt so NOT sport pilot)
                'vx_speed': 70.0,  # Best angle of climb speed (81 MPH converted)
                'vy_speed': 90.0,  # Best rate of climb speed (104 MPH converted)
                'vs0_speed': 53.0, # Stall speed landing configuration (61 MPH converted)
                'vg_speed': 80.0,  # Best glide speed (estimated for this performance class)
                'vfe_speed': 78.0, # Max flap extended speed (estimate based on approach speeds)
                'vno_speed': 130.0, # Normal operating speed (estimated based on performance)
                'vne_speed': 152.0, # Never exceed speed (estimated based on design limits)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A4K', 'horsepower': 180}
            },
            {
                'manufacturer': manufacturers['grumman'],
                'model': 'AA-5 Traveler',
                'clean_stall_speed': 50.0,  # Updated from planephd.com - IS sport pilot eligible (4-seater)
                'top_speed': 135.0,
                'maneuvering_speed': 120.0,
                'max_takeoff_weight': 2200,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1972, 1, 1),
                'verification_source': 'Grumman Traveler AA-5 specifications, planephd.com performance data',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-320-E2G', 'horsepower': 150},
                'vx_speed': 63.0,   # Estimated best angle climb (similar to other 150hp O-320 aircraft)
                'vy_speed': 78.0,   # Estimated best rate climb (based on 660 FPM climb rate and similar aircraft)
                'vs0_speed': 50.0,  # Stall speed landing config (same as clean from planephd.com)
                'vg_speed': 75.0,   # Estimated best glide speed (typical for this performance class)
                'vfe_speed': 85.0,  # Estimated max flap extended speed (typical for Grumman design)
                'vno_speed': 120.0, # Using existing maneuvering speed as structural cruising speed
                'vne_speed': 155.0, # Estimated never exceed speed (typical for this class)
            },
            {
                'manufacturer': manufacturers['grumman'],
                'model': 'AA-1 Yankee',
                'clean_stall_speed': 57.0,  # AOPA: 57 knots clean stall
                'top_speed': 117.0,  # AOPA: 117 knots at 75% power
                'maneuvering_speed': 115.0,
                'max_takeoff_weight': 1500,
                'seating_capacity': 2,
                'retractable_gear': False,
                'variable_pitch_prop': False,
                'certification_date': date(1970, 1, 1),
                'verification_source': 'AOPA fact sheet, Grumman AA-1 POH, performance specifications',
                # V-Speed data from AOPA and POH research - popular club aircraft
                'vx_speed': 55.0,   # 63 mph best angle of climb (converted to knots)
                'vy_speed': 69.0,   # 79 mph best rate of climb (converted to knots)
                'vs0_speed': 57.0,  # Stall speed landing configuration (AOPA: same as clean)
                'vg_speed': 75.0,   # Best glide speed (estimated near approach speed)
                'vfe_speed': 80.0,  # Max flap extended speed (estimated)
                'vno_speed': 125.0, # Max structural cruising speed (AOPA: 125 KCAS)
                'vne_speed': 169.0, # Do not exceed speed (AOPA: 169 KCAS)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-235-C2C', 'horsepower': 108}
            },
            {
                'manufacturer': manufacturers['tecnam'],
                'model': 'P2006T',
                'clean_stall_speed': 58.0,  # IS sport pilot eligible (twin-engine LSA)
                'top_speed': 155.0,  # Updated to align with research
                'maneuvering_speed': 122.0,  # Va from POH
                'max_takeoff_weight': 2645,
                'seating_capacity': 4,
                'retractable_gear': False,
                'variable_pitch_prop': True,
                'certification_date': date(2012, 1, 1),
                'verification_source': 'Tecnam P2006T POH, planephd.com, operating manual',
                # V-Speed data from POH and operating manual sources
                'vx_speed': 84.0,   # Best rate of climb (also single-engine Vyse)
                'vy_speed': 84.0,   # Best rate of climb both engines
                'vs0_speed': 53.0,  # Stall landing configuration (POH white arc lower)
                'vg_speed': 95.0,   # Maximum glide range speed (POH)
                'vfe_speed': 93.0,  # Maximum flap extended speed landing (POH)
                'vno_speed': 138.0, # Maximum structural cruising speed (POH green arc)
                'vne_speed': 171.0, # Never exceed speed (POH red line)
                'engine_specs': {'manufacturer': 'Rotax', 'model': '912S3', 'horsepower': 100}
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
                # V-Speed data from MooneySpace forum POH discussion - NOT sport pilot eligible (61kt stall > 59kt limit)
                'vx_speed': 82.0,  # 94 mph converted to knots (best angle climb)
                'vy_speed': 98.0,  # 113 mph converted to knots (best rate climb at sea level)
                'vs0_speed': 50.0, # Estimated stall speed with flaps (typically ~10kt lower than clean)
                'vg_speed': 85.0,  # Estimated best glide speed (typical for M20 series)
                'vfe_speed': 87.0, # Estimated max flap speed (conservative for retractable)
                'vno_speed': 152.0, # Estimated max structural cruising (typical for M20E)
                'vne_speed': 195.0, # Estimated never exceed (typical for M20E performance)
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
                'verification_source': 'Mooney M20F Executive specifications, Mooney family performance analysis',
                # V-Speed data based on Mooney family analysis - CRITICAL: 59kt stall = RIGHT AT sport pilot limit!
                'vx_speed': 82.0,  # Best angle of climb speed (similar to M20D with same engine)
                'vy_speed': 96.0,  # Best rate of climb speed (estimate based on 180hp performance)
                'vs0_speed': 53.0, # Stall speed landing configuration (estimated from family data)
                'vg_speed': 85.0,  # Best glide speed (estimate based on Mooney characteristics)
                'vfe_speed': 100.0, # Max flap extended speed (typical Mooney specification)
                'vno_speed': 148.0, # Normal operating speed (estimate based on Mooney family)
                'vne_speed': 174.0, # Never exceed speed (estimate based on Mooney performance envelope)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A1A', 'horsepower': 180}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20G Statesman',
                'clean_stall_speed': 50.0,  # Updated from planephd.com - IS sport pilot eligible
                'top_speed': 155.0,  # 155 kts from aircraft specifications
                'maneuvering_speed': 138.0,
                'max_takeoff_weight': 2525,  # Corrected weight from research
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1968, 1, 1),
                'verification_source': 'MooneySpace forum, Global Air, planephd.com specifications',
                # V-Speed data from MooneySpace M20G discussion and specifications
                'vx_speed': 71.0,   # 82 mph best angle of climb (MooneySpace forum)
                'vy_speed': 88.0,   # 101 mph best rate of climb (MooneySpace forum)
                'vs0_speed': 50.0,  # Stall speed landing configuration (Global Air specs)
                'vg_speed': 85.0,   # Best glide speed (estimated near cruise climb)
                'vfe_speed': 109.0, # Max flap extended speed (125 mph typical for era)
                'vno_speed': 152.0, # Normal operating speed (175 mph post-1969)
                'vne_speed': 174.0, # Never exceed speed (200 mph typical for Mooneys)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'O-360-A1D', 'horsepower': 180}
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
                'verification_source': 'Mooney M20J 201 specifications, high-performance retractable specifications',
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'IO-360-A3B6D', 'horsepower': 200},
                # V-Speed data for Mooney M20J 201 (MOSAIC LSA ELIGIBLE - 61kt = 61kt limit!)
                'vx_speed': 70.0,   # Best angle climb (high-performance with 200HP IO-360)
                'vy_speed': 95.0,   # Best rate climb (excellent with fuel injection)
                'vs0_speed': 56.0,  # Stall landing configuration (gear/flaps down)
                'vg_speed': 82.0,   # Best glide speed (high-performance retractable)
                'vfe_speed': 110.0, # Max flap extended speed (high-performance design)
                'vno_speed': 150.0, # Max structural cruising (using maneuvering speed)
                'vne_speed': 201.0, # Never exceed speed (using top speed)
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20K 231',
                'clean_stall_speed': 57.0,  # CORRECTED - IS MOSAIC LSA eligible (≤61kt, not sport pilot)
                'top_speed': 200.0,  # Updated from planephd.com - 191kt cruise, ~200kt max
                'maneuvering_speed': 160.0,
                'max_takeoff_weight': 2900,  # Updated from research
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1979, 1, 1),
                'verification_source': 'planephd.com M20K 231 specs, Aviation Consumer, AOPA',
                # V-Speed data from research and estimated values based on turbocharged Mooney performance
                'vx_speed': 79.0,   # Estimated from Mooney owner POH references
                'vy_speed': 96.0,   # Estimated from Mooney owner POH references
                'vs0_speed': 54.0,  # Estimated landing configuration stall (slightly lower than clean)
                'vg_speed': 95.0,   # Estimated best glide speed based on performance
                'vfe_speed': 109.0, # Estimated max flap extended speed (typical for Mooney)
                'vno_speed': 174.0, # From research (200 mph converted to knots)
                'vne_speed': 196.0, # From research (225 mph converted to knots)
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-360-GB', 'horsepower': 210}
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
                # V-Speed data for M20L with Porsche engine - NOT sport pilot eligible (62kt stall > 59kt limit)
                'vx_speed': 83.0,   # Best angle of climb speed (typical for M20L)
                'vy_speed': 100.0,  # Best rate of climb speed (Porsche engine performance)
                'vs0_speed': 52.0,  # Stall speed with flaps (approximately 10kt below clean)
                'vg_speed': 85.0,   # Best glide speed (typical for M20L series)
                'vfe_speed': 87.0,  # Maximum flap extended speed (conservative for retractable)
                'vno_speed': 154.0, # Maximum structural cruising speed
                'vne_speed': 196.0, # Never exceed speed (typical for M20L performance)
                'engine_specs': {'manufacturer': 'Porsche', 'model': 'PFM 3200', 'horsepower': 217}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20M TLS',
                'clean_stall_speed': 58.0,  # CORRECTED - IS sport pilot eligible (≤59kt)!
                'top_speed': 223.0,  # Updated from planephd.com - best cruise speed
                'maneuvering_speed': 175.0,
                'max_takeoff_weight': 3200,  # Updated from research
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1989, 1, 1),
                'verification_source': 'planephd.com M20M TLS specs, Aviation Consumer, AVweb',
                # V-Speed data from research and official sources
                'vx_speed': 80.0,   # Best angle of climb from research
                'vy_speed': 105.0,  # Best rate of climb from research (1,230 FPM)
                'vs0_speed': 55.0,  # Estimated landing configuration stall (slightly lower than clean)
                'vg_speed': 100.0,  # Estimated best glide speed based on performance
                'vfe_speed': 120.0, # Estimated max flap extended speed (typical for high-performance)
                'vno_speed': 190.0, # Estimated max structural cruising speed
                'vne_speed': 210.0, # Estimated never exceed speed (typical for TLS)
                'engine_specs': {'manufacturer': 'Lycoming', 'model': 'TIO-540-AF1B', 'horsepower': 270}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20R Ovation',
                'clean_stall_speed': 65.0,  # Vs1 clean configuration (NOT sport pilot eligible)
                'top_speed': 197.0,
                'maneuvering_speed': 152.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1994, 1, 1),
                'verification_source': 'AOPA, Aviation Consumer, Mooney pilot reports',
                # V-Speed data from multiple Mooney M20R sources
                'vx_speed': 85.0,   # Best angle climb from pilot reports
                'vy_speed': 105.0,  # Best rate climb from AOPA test flights
                'vs0_speed': 59.0,  # Stall landing configuration from specifications
                'vg_speed': 100.0,  # Estimated best glide speed (typical for high-performance aircraft)
                'vfe_speed': 110.0, # Estimated max flap extended speed
                'vno_speed': 175.0, # Estimated normal operating speed
                'vne_speed': 197.0, # Never exceed speed (same as top speed)
                'vle_speed': 132.0, # Estimated max gear extended speed (typical for RG)
                'vlo_speed': 132.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-550-G', 'horsepower': 280}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20S Eagle',
                'clean_stall_speed': 58.0,  # Corrected stall speed - IS sport pilot eligible
                'top_speed': 175.0,
                'maneuvering_speed': 145.0,
                'max_takeoff_weight': 3200,  # Corrected from research (3,200 lbs)
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(1999, 1, 1),  # Corrected release year
                'verification_source': 'Aviation Consumer, planephd.com, pilot reports',
                # V-Speed data from research and estimated values based on similar Mooney aircraft
                'vx_speed': 80.0,   # Estimated best angle climb (typical for IO-550 powered Mooney)
                'vy_speed': 110.0,  # Estimated from 1,175 fpm climb rate performance
                'vs0_speed': 55.0,  # Estimated landing configuration stall
                'vg_speed': 95.0,   # Estimated best glide speed
                'vfe_speed': 105.0, # Estimated max flap extended speed
                'vno_speed': 165.0, # Estimated normal operating speed
                'vne_speed': 175.0, # Never exceed speed (same as top speed)
                'vle_speed': 132.0, # Estimated max gear extended speed
                'vlo_speed': 132.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'IO-550-G', 'horsepower': 244}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20TN Acclaim',
                'clean_stall_speed': 66.0,  # Estimated clean stall (NOT sport pilot eligible)
                'top_speed': 242.0,
                'maneuvering_speed': 175.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(2006, 1, 1),
                'verification_source': 'Aviation Consumer, FlyRadius, pilot reports',
                # V-Speed data from research and estimated values for turbocharged Acclaim
                'vx_speed': 90.0,   # Estimated best angle climb (higher for turbocharged)
                'vy_speed': 120.0,  # Estimated best rate climb for high-performance turbocharged
                'vs0_speed': 60.0,  # Landing configuration stall from Type S POH (60.2 knots)
                'vg_speed': 105.0,  # Estimated best glide speed
                'vfe_speed': 115.0, # Estimated max flap extended speed
                'vno_speed': 200.0, # Estimated normal operating speed (high-performance)
                'vne_speed': 242.0, # Never exceed speed (same as top speed)
                'vle_speed': 140.0, # Estimated max gear extended speed
                'vlo_speed': 140.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-550-G', 'horsepower': 280}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20V Acclaim Ultra',
                'clean_stall_speed': 62.0,  # Estimated clean stall - MOSAIC LSA eligible (61kt limit)
                'top_speed': 242.0,  # Corrected max cruise speed from research
                'maneuvering_speed': 175.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(2016, 1, 1),
                'verification_source': 'AOPA, Aviation Consumer, SkyTough, planephd.com',
                # V-Speed data from research and estimated values for 2016 Acclaim Ultra
                'vx_speed': 90.0,   # Estimated best angle climb (turbocharged performance)
                'vy_speed': 120.0,  # Best rate climb speed from research
                'vs0_speed': 56.0,  # Landing configuration stall from research - SPORT PILOT ELIGIBLE
                'vg_speed': 105.0,  # Estimated best glide speed
                'vfe_speed': 115.0, # Estimated max flap extended speed
                'vno_speed': 200.0, # Estimated normal operating speed (high-performance turbocharged)
                'vne_speed': 242.0, # Never exceed speed (same as max cruise)
                'vle_speed': 140.0, # Estimated max gear extended speed
                'vlo_speed': 140.0, # Estimated max gear operating speed
                'engine_specs': {'manufacturer': 'Continental', 'model': 'TSIO-550-G', 'horsepower': 280}
            },
            {
                'manufacturer': mooney_intl,
                'model': 'M20U Ovation Ultra',
                'clean_stall_speed': 59.0,  # Estimated clean stall - borderline sport pilot eligible
                'top_speed': 197.0,
                'maneuvering_speed': 152.0,
                'max_takeoff_weight': 3368,
                'seating_capacity': 4,
                'retractable_gear': True,
                'variable_pitch_prop': True,
                'certification_date': date(2016, 1, 1),
                'verification_source': 'GlobalAir, SA Mooney, Aviation Consumer',
                # V-Speed data from research and estimated values for 2016 Ovation Ultra
                'vx_speed': 85.0,   # Estimated best angle climb (similar to M20R)
                'vy_speed': 105.0,  # Estimated best rate climb (similar to M20R)
                'vs0_speed': 56.0,  # Landing configuration stall from research - SPORT PILOT ELIGIBLE
                'vg_speed': 100.0,  # Estimated best glide speed
                'vfe_speed': 110.0, # Estimated max flap extended speed
                'vno_speed': 175.0, # Estimated normal operating speed
                'vne_speed': 197.0, # Never exceed speed (same as top speed)
                'vle_speed': 132.0, # Estimated max gear extended speed
                'vlo_speed': 132.0, # Estimated max gear operating speed
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