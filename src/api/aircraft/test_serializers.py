from django.test import TestCase
from decimal import Decimal
from datetime import date
from .models import Manufacturer, Engine, Aircraft, AircraftCorrection
from .serializers import ManufacturerSerializer, AircraftSerializer, AircraftDetailSerializer


class ManufacturerSerializerTest(TestCase):
    """Test cases for ManufacturerSerializer"""
    
    def setUp(self):
        self.manufacturer_data = {
            'name': 'Boeing',
            'is_currently_manufacturing': True
        }
        self.manufacturer = Manufacturer.objects.create(**self.manufacturer_data)
    
    def test_manufacturer_serialization(self):
        """Test that manufacturer serializes correctly"""
        serializer = ManufacturerSerializer(instance=self.manufacturer)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Boeing')
        self.assertTrue(data['is_currently_manufacturing'])
        self.assertIn('id', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_manufacturer_deserialization(self):
        """Test that manufacturer deserializes correctly"""
        data = {
            'name': 'Airbus',
            'is_currently_manufacturing': False
        }
        serializer = ManufacturerSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())
        manufacturer = serializer.save()
        self.assertEqual(manufacturer.name, 'Airbus')
        self.assertFalse(manufacturer.is_currently_manufacturing)
    
    def test_manufacturer_validation_required_fields(self):
        """Test that required fields are validated"""
        data = {'is_currently_manufacturing': True}  # Missing name
        serializer = ManufacturerSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class AircraftSerializerTest(TestCase):
    """Test cases for AircraftSerializer"""
    
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name='Cessna',
            is_currently_manufacturing=True
        )
        self.engine = Engine.objects.create(
            manufacturer='Lycoming',
            model='O-320-E2A',
            horsepower=150,
            fuel_type='AVGAS',
            engine_type='PISTON'
        )
        self.aircraft = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model='172',
            clean_stall_speed=Decimal('47.0'),
            top_speed=Decimal('126.0'),
            maneuvering_speed=Decimal('99.0'),
            max_takeoff_weight=2550,
            seating_capacity=4,
            retractable_gear=False,
            variable_pitch_prop=False,
            certification_date=date(1956, 1, 1),
            verification_source='Cessna 172 POH'
        )
        self.aircraft.engines.add(self.engine)
    
    def test_aircraft_list_serialization(self):
        """Test that aircraft serializes correctly for list view"""
        serializer = AircraftSerializer(instance=self.aircraft)
        data = serializer.data
        
        # Check basic fields
        self.assertEqual(data['model'], '172')
        self.assertEqual(float(data['clean_stall_speed']), 47.0)
        self.assertEqual(float(data['top_speed']), 126.0)
        self.assertEqual(float(data['maneuvering_speed']), 99.0)
        self.assertEqual(data['max_takeoff_weight'], 2550)
        self.assertEqual(data['seating_capacity'], 4)
        self.assertFalse(data['retractable_gear'])
        self.assertFalse(data['variable_pitch_prop'])
        self.assertTrue(data['is_mosaic_compliant'])
        self.assertTrue(data['sport_pilot_eligible'])
        
        # Check manufacturer field (should be ID in list serializer)
        self.assertIn('manufacturer', data)
        self.assertEqual(data['manufacturer'], self.manufacturer.id)
        
        # Check manufacturer_name field
        self.assertIn('manufacturer_name', data)
        self.assertEqual(data['manufacturer_name'], 'Cessna')
        
        # Check computed properties
        self.assertIn('eligibility_badges', data)
        self.assertIn('performance_category', data)
        self.assertIn('speed_range', data)
    
    def test_aircraft_detail_serialization(self):
        """Test that aircraft detail serialization includes engines"""
        serializer = AircraftDetailSerializer(instance=self.aircraft)
        data = serializer.data
        
        # Should include all basic fields
        self.assertEqual(data['model'], '172')
        self.assertEqual(data['verification_source'], 'Cessna 172 POH')
        
        # Should include engines
        self.assertIn('engines', data)
        self.assertEqual(len(data['engines']), 1)
        engine_data = data['engines'][0]
        self.assertEqual(engine_data['manufacturer'], 'Lycoming')
        self.assertEqual(engine_data['model'], 'O-320-E2A')
        self.assertEqual(engine_data['horsepower'], 150)
    
    def test_aircraft_eligibility_badges(self):
        """Test that eligibility badges are computed correctly"""
        # Test sport pilot eligible aircraft
        sport_aircraft = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model='150',
            clean_stall_speed=Decimal('48.0'),
            top_speed=Decimal('109.0'),
            maneuvering_speed=Decimal('89.0'),
            seating_capacity=2
        )
        
        serializer = AircraftSerializer(instance=sport_aircraft)
        badges = serializer.data['eligibility_badges']
        
        self.assertIn('Sport Pilot', badges)
        self.assertIn('MOSAIC Eligible', badges)
        
        # Test retractable gear aircraft (not sport pilot eligible due to >59 knots stall speed)
        rg_aircraft = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model='182RG',
            clean_stall_speed=Decimal('60.0'),  # Above sport pilot limit of 59
            top_speed=Decimal('155.0'),
            maneuvering_speed=Decimal('119.0'),
            seating_capacity=4,
            retractable_gear=True
        )
        
        serializer = AircraftSerializer(instance=rg_aircraft)
        badges = serializer.data['eligibility_badges']
        
        self.assertIn('RG', badges)
        self.assertIn('Private Pilot', badges)  # Should be private pilot only
        self.assertNotIn('Sport Pilot', badges)  # Not sport pilot eligible due to >59 knots
    
    def test_aircraft_performance_category(self):
        """Test that performance category is computed correctly"""
        # Test high performance aircraft
        high_perf = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model='TTx',
            clean_stall_speed=Decimal('60.0'),
            top_speed=Decimal('235.0'),
            maneuvering_speed=Decimal('158.0'),
            seating_capacity=4
        )
        
        serializer = AircraftSerializer(instance=high_perf)
        self.assertEqual(serializer.data['performance_category'], 'High Performance')
        
        # Test cross country aircraft  
        cross_country = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model='182',
            clean_stall_speed=Decimal('56.0'),
            top_speed=Decimal('145.0'),
            maneuvering_speed=Decimal('119.0'),
            seating_capacity=4
        )
        
        serializer = AircraftSerializer(instance=cross_country)
        self.assertEqual(serializer.data['performance_category'], 'Cross Country')
        
        # Test standard performance aircraft
        standard_perf = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model='152',
            clean_stall_speed=Decimal('48.0'),
            top_speed=Decimal('109.0'),
            maneuvering_speed=Decimal('89.0'),
            seating_capacity=2
        )
        
        serializer = AircraftSerializer(instance=standard_perf)
        self.assertEqual(serializer.data['performance_category'], 'Standard Performance')
    
    def test_aircraft_deserialization(self):
        """Test that aircraft can be created from serialized data"""
        data = {
            'manufacturer': self.manufacturer.id,
            'model': '170',
            'clean_stall_speed': '45.0',
            'top_speed': '115.0',
            'maneuvering_speed': '92.0',
            'max_takeoff_weight': 2200,
            'seating_capacity': 4,
            'retractable_gear': False,
            'variable_pitch_prop': False,
            'certification_date': '1948-06-01',
            'verification_source': 'Cessna 170 specifications'
        }
        
        serializer = AircraftSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        aircraft = serializer.save()
        self.assertEqual(aircraft.model, '170')
        self.assertEqual(aircraft.clean_stall_speed, Decimal('45.0'))
        self.assertTrue(aircraft.sport_pilot_eligible)
        self.assertTrue(aircraft.is_mosaic_compliant)
    
    def test_aircraft_validation_stall_speed_limit(self):
        """Test that stall speed is validated within MOSAIC limits"""
        data = {
            'manufacturer': self.manufacturer.id,
            'model': 'FastStall',
            'clean_stall_speed': '65.0',  # Above MOSAIC limit
            'top_speed': '150.0',
            'maneuvering_speed': '120.0',
            'seating_capacity': 2
        }
        
        serializer = AircraftSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('clean_stall_speed', serializer.errors)
    
    def test_aircraft_validation_required_fields(self):
        """Test that required fields are validated"""
        data = {
            'model': 'Incomplete'
            # Missing manufacturer, speeds, etc.
        }
        
        serializer = AircraftSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        
        required_fields = ['manufacturer', 'clean_stall_speed', 'top_speed', 'maneuvering_speed']
        for field in required_fields:
            self.assertIn(field, serializer.errors)


class AircraftDetailSerializerTest(TestCase):
    """Test cases specific to AircraftDetailSerializer"""
    
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name='Piper')
        self.engine1 = Engine.objects.create(
            manufacturer='Lycoming',
            model='O-320-D2A',
            horsepower=160,
            displacement_liters=Decimal('5.24'),
            fuel_type='AVGAS',
            engine_type='PISTON',
            is_fuel_injected=True
        )
        self.engine2 = Engine.objects.create(
            manufacturer='Continental',
            model='O-320-A2B',
            horsepower=150,
            displacement_liters=Decimal('5.20'),
            fuel_type='AVGAS',
            engine_type='PISTON',
            is_fuel_injected=False
        )
        self.aircraft = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model='Cherokee 180',
            clean_stall_speed=Decimal('55.0'),
            top_speed=Decimal('139.0'),
            maneuvering_speed=Decimal('112.0'),
            max_takeoff_weight=2450,
            seating_capacity=4,
            certification_date=date(1962, 10, 15),
            verification_source='Piper Cherokee POH, Section 6'
        )
        self.aircraft.engines.add(self.engine1, self.engine2)
    
    def test_detail_includes_all_engines(self):
        """Test that detail serializer includes all related engines"""
        serializer = AircraftDetailSerializer(instance=self.aircraft)
        data = serializer.data
        
        self.assertIn('engines', data)
        self.assertEqual(len(data['engines']), 2)
        
        # Check that both engines are included with full details
        engine_manufacturers = [e['manufacturer'] for e in data['engines']]
        self.assertIn('Lycoming', engine_manufacturers)
        self.assertIn('Continental', engine_manufacturers)
        
        # Check engine details
        lycoming_engine = next(e for e in data['engines'] if e['manufacturer'] == 'Lycoming')
        self.assertEqual(lycoming_engine['model'], 'O-320-D2A')
        self.assertEqual(lycoming_engine['horsepower'], 160)
        self.assertTrue(lycoming_engine['is_fuel_injected'])
        self.assertEqual(lycoming_engine['fuel_type'], 'AVGAS')
        self.assertEqual(lycoming_engine['engine_type'], 'PISTON')
    
    def test_detail_includes_certification_info(self):
        """Test that detail serializer includes certification date and source"""
        serializer = AircraftDetailSerializer(instance=self.aircraft)
        data = serializer.data
        
        self.assertEqual(data['certification_date'], '1962-10-15')
        self.assertEqual(data['verification_source'], 'Piper Cherokee POH, Section 6')
    
    def test_detail_includes_computed_properties(self):
        """Test that detail serializer includes all computed properties"""
        serializer = AircraftDetailSerializer(instance=self.aircraft)
        data = serializer.data
        
        # Should include all the same computed properties as basic serializer
        self.assertIn('eligibility_badges', data)
        self.assertIn('performance_category', data)
        self.assertIn('speed_range', data)
        
        # Plus any detail-specific computed properties
        self.assertIn('mosaic_analysis', data)
        
        # Check MOSAIC analysis content
        analysis = data['mosaic_analysis']
        self.assertIn('lsa_eligible', analysis)
        self.assertIn('sport_pilot_eligible', analysis)
        self.assertIn('certification_era', analysis)