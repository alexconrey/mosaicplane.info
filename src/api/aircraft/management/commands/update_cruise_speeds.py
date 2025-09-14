from django.core.management.base import BaseCommand
from aircraft.models import Aircraft
from decimal import Decimal


class Command(BaseCommand):
    help = 'Update cruise speeds for aircraft based on research data'

    def handle(self, *args, **options):
        """
        Update cruise speeds for aircraft based on comprehensive research
        All speeds are at 75% power at optimal altitude
        """
        
        # Cruise speed data based on research from FAA TCDS, POH, and manufacturer specs
        cruise_speed_data = {
            # CESSNA AIRCRAFT
            ('Cessna', '140'): 90,
            ('Cessna', '140A'): 90,
            ('Cessna', '150'): 96,
            ('Cessna', '150A'): 96,
            ('Cessna', '150B'): 96,
            ('Cessna', '150C'): 96,
            ('Cessna', '150D'): 96,
            ('Cessna', '150E'): 96,
            ('Cessna', '150F'): 96,
            ('Cessna', '150G'): 96,
            ('Cessna', '150H'): 96,
            ('Cessna', '150J'): 96,
            ('Cessna', '150K'): 96,
            ('Cessna', '150L'): 96,
            ('Cessna', '150M'): 96,
            ('Cessna', '152'): 98,
            ('Cessna', '170'): 100,
            ('Cessna', '170A'): 100,
            ('Cessna', '170B'): 100,
            ('Cessna', '172'): 114,
            ('Cessna', '172A'): 114,
            ('Cessna', '172B'): 114,
            ('Cessna', '172C'): 114,
            ('Cessna', '172D'): 114,
            ('Cessna', '172E'): 114,
            ('Cessna', '172F'): 114,
            ('Cessna', '172G'): 114,
            ('Cessna', '172H'): 114,
            ('Cessna', '172I'): 114,
            ('Cessna', '172K'): 114,
            ('Cessna', '172L'): 114,
            ('Cessna', '172M'): 114,
            ('Cessna', '172N'): 122,
            ('Cessna', '172P'): 122,
            ('Cessna', '172Q Cutlass'): 128,
            ('Cessna', '172R'): 124,
            ('Cessna', '172RG Cutlass'): 140,
            ('Cessna', '172S'): 124,
            ('Cessna', '175'): 118,
            ('Cessna', '177'): 120,
            ('Cessna', '180'): 140,
            ('Cessna', '182'): 141,
            ('Cessna', '182 (Original)'): 141,
            ('Cessna', '182A'): 141,
            ('Cessna', '182B'): 141,
            ('Cessna', '182C'): 141,
            ('Cessna', '182D'): 141,
            ('Cessna', '182E'): 141,
            ('Cessna', '182F'): 141,
            ('Cessna', '182G'): 141,
            ('Cessna', '182H'): 141,
            ('Cessna', '182J'): 141,
            ('Cessna', '182K'): 141,
            ('Cessna', '182L'): 141,
            ('Cessna', '182M'): 141,
            ('Cessna', '182N'): 141,
            ('Cessna', '182P'): 141,
            ('Cessna', '182Q'): 141,
            ('Cessna', '182R'): 141,
            ('Cessna', '182RG Skylane RG'): 156,
            ('Cessna', '182S'): 141,
            ('Cessna', '182T'): 141,
            ('Cessna', '185'): 145,
            ('Cessna', '206 Stationair'): 131,
            
            # PIPER AIRCRAFT
            ('Piper', 'J-3 Cub'): 75,
            ('Piper', 'Cherokee 140'): 110,
            ('Piper', 'Cherokee 150'): 112,
            ('Piper', 'Cherokee 160'): 117,
            ('Piper', 'Cherokee 180'): 122,
            ('Piper', 'Cherokee 235'): 132,
            ('Piper', 'Archer III'): 120,
            ('Piper', 'Saratoga'): 145,
            ('Piper', 'Super Cub'): 100,
            ('Piper', 'Super Cub PA-18'): 100,
            ('Piper', 'Tomahawk'): 95,
            ('Piper', 'Pacer'): 100,
            ('Piper', 'Clipper'): 110,
            ('Piper', 'Colt'): 102,
            ('Piper', 'Tri-Pacer'): 108,
            
            # BEECHCRAFT AIRCRAFT
            ('Beechcraft', 'Musketeer'): 110,
            ('Beechcraft', 'Sundowner'): 120,
            ('Beechcraft', 'Sierra'): 135,
            ('Beechcraft', 'Skipper 77'): 104,
            ('Beechcraft', 'Sport 150'): 115,
            ('Beechcraft', 'Bonanza A36'): 165,
            
            # MOONEY AIRCRAFT
            ('Mooney International', 'M20 (Original)'): 145,
            ('Mooney International', 'M20A'): 145,
            ('Mooney International', 'M20B'): 145,
            ('Mooney International', 'M20C Ranger'): 150,
            ('Mooney International', 'M20D Master'): 150,
            ('Mooney International', 'M20E Super 21'): 157,
            ('Mooney International', 'M20F Executive 21'): 157,
            ('Mooney International', 'M20G Statesman'): 153,
            ('Mooney International', 'M20J 201'): 175,
            ('Mooney International', 'M20K 231'): 180,
            ('Mooney International', 'M20L PFM'): 170,
            ('Mooney International', 'M20M TLS'): 180,
            ('Mooney International', 'M20R Ovation'): 180,
            ('Mooney International', 'M20S Eagle'): 155,
            ('Mooney International', 'M20T Acclaim'): 220,
            ('Mooney International', 'M20U Ovation Ultra'): 185,
            ('Mooney International', 'M20V Acclaim Ultra'): 220,
            
            # AMERICAN CHAMPION AIRCRAFT
            ('American Champion Aircraft', 'Citabria 7ECA'): 95,
            ('American Champion Aircraft', 'Citabria 7GCBC'): 104,
            ('American Champion Aircraft', 'Decathlon 8KCAB'): 115,
            ('American Champion Aircraft', 'Scout 8GCBC'): 115,
            ('American Champion Aircraft', 'Scout 8KCAB'): 110,
            
            # CHAMPION AIRCRAFT (Legacy)
            ('Champion Aircraft', 'Citabria 7GCAA'): 104,
            ('Champion Aircraft', 'Citabria 7GCBC'): 104,
            
            # GRUMMAN AIRCRAFT
            ('Grumman', 'AA-1A'): 112,
            ('Grumman', 'AA-1B'): 112,
            ('Grumman', 'AA-5'): 121,
            ('Grumman', 'AA-5A Cheetah'): 119,
            ('Grumman', 'AA-5B Tiger'): 139,
            ('Grumman American', 'AA-1 Yankee'): 112,
            ('Grumman American', 'AA-5 Traveler'): 121,
            
            # AERONCA AIRCRAFT
            ('Aeronca', 'Champion 7AC'): 85,
            ('Aeronca', 'Champ 7BCM'): 88,
            
            # AVIAT AIRCRAFT
            ('Aviat Aircraft', 'Husky A-1C'): 120,
            ('Aviat Aircraft', 'Husky A-1C-180'): 115,
            ('Aviat Aircraft', 'Pitts S-2A'): 135,
            
            # CIRRUS AIRCRAFT
            ('Cirrus', 'SR20'): 142,
            ('Cirrus', 'SR22'): 169,
            
            # DIAMOND AIRCRAFT
            ('Diamond Aircraft', 'DA20-A1'): 125,
            ('Diamond Aircraft', 'DA20-C1'): 125,
            
            # MAULE AIR
            ('Maule Air', 'M-4-180C'): 120,
            ('Maule Air', 'M-4-220C'): 125,
            ('Maule Air', 'M-5-180C'): 130,
            ('Maule Air', 'M-5-235C'): 140,
            ('Maule Air', 'M-6-180'): 135,
            ('Maule Air', 'M-6-235'): 150,
            ('Maule Air', 'M-7-180'): 145,
            ('Maule Air', 'M-7-235'): 155,
            ('Maule Air', 'M-7-235 Super Rocket'): 125,
            
            # LAKE AIRCRAFT
            ('Lake Aircraft', 'LA-4-200'): 115,
            
            # LIGHT SPORT AIRCRAFT
            ('Czech Sport Aircraft', 'SportCruiser'): 98,
            ('Flight Design', 'CTLS'): 98,
            ('Icon Aircraft', 'A5'): 85,
            ('Progressive Aerodyne', 'SeaRey'): 90,
            ('Pipistrel', 'Virus SW 121'): 108,
            ('Tecnam', 'P2008-JC'): 95,
            ('Tecnam', 'P2002-Sierra'): 118,
            ('Tecnam', 'P2006T'): 135,
            ('Remos', 'GX'): 108,
            
            # EXPERIMENTAL AIRCRAFT
            ('Van\'s Aircraft', 'RV-3'): 165,
            ('Van\'s Aircraft', 'RV-9A'): 130,
            ('Van\'s Aircraft', 'RV-12iS'): 115,
            ('Kitfox Aircraft', 'Series 7 STi'): 85,
            ('Kitfox Aircraft', 'Series 7 Super Sport'): 85,
            ('Kitfox Aircraft', 'Series 7 Speedster'): 110,
            ('RANS Aircraft', 'S-6ES Coyote II'): 70,
            ('RANS Aircraft', 'S-7LS Courier'): 78,
            ('Zenith Aircraft', 'CH-701 STOL'): 80,
            ('Zenith Aircraft', 'CH-750 STOL'): 85,
            
            # CLASSIC AIRCRAFT
            ('Taylorcraft', 'BC-12D'): 88,
            ('Murphy Aircraft', 'Rebel'): 85,
            ('Just Aircraft', 'SuperSTOL'): 80,
            ('CubCrafters', 'Carbon Cub EX-2'): 110,
            ('Evektor', 'SportStar'): 95,
            ('Quicksilver Aircraft', 'Sport 2S'): 52,
        }
        
        updated_count = 0
        not_found_count = 0
        
        for aircraft in Aircraft.objects.all():
            manufacturer_name = aircraft.manufacturer.name
            model_name = aircraft.model
            
            # Look up cruise speed
            key = (manufacturer_name, model_name)
            if key in cruise_speed_data:
                cruise_speed = cruise_speed_data[key]
                
                # Update only if cruise speed is currently null
                if aircraft.cruise_speed is None:
                    aircraft.cruise_speed = Decimal(str(cruise_speed))
                    aircraft.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated {manufacturer_name} {model_name}: {cruise_speed} knots'
                        )
                    )
                else:
                    self.stdout.write(
                        f'Skipped {manufacturer_name} {model_name}: Already has cruise speed ({aircraft.cruise_speed})'
                    )
            else:
                not_found_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'No cruise speed data found for: {manufacturer_name} {model_name}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nCruise speed update completed!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Aircraft updated: {updated_count}'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                f'Aircraft without data: {not_found_count}'
            )
        )