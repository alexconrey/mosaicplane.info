"""
Smoke tests for the MOSAIC Aircraft API
Tests basic functionality and integration between components
"""
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from datetime import date
import json
from .models import Manufacturer, Engine, Aircraft, AircraftCorrection


class APISmokTest(APITestCase):
    """Smoke tests for API basic functionality"""
    
    def setUp(self):
        """Set up basic test data"""
        self.manufacturer = Manufacturer.objects.create(
            name="Cessna",
            is_currently_manufacturing=True
        )
        self.engine = Engine.objects.create(
            manufacturer="Lycoming",
            model="O-320-E2A", 
            horsepower=150,
            fuel_type='AVGAS',
            engine_type='PISTON'
        )
        self.aircraft = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model="172",
            clean_stall_speed=Decimal('47.0'),
            top_speed=Decimal('126.0'),
            maneuvering_speed=Decimal('99.0'),
            max_takeoff_weight=2550,
            seating_capacity=4,
            certification_date=date(1956, 1, 1),
            verification_source="Cessna 172 POH"
        )
        self.aircraft.engines.add(self.engine)
    
    def test_api_endpoints_respond(self):
        """Test that all main API endpoints respond correctly"""
        endpoints = [
            ('manufacturer-list', None),
            ('manufacturer-detail', {'pk': self.manufacturer.id}), 
            ('aircraft-list', None),
            ('aircraft-detail', {'pk': self.aircraft.id}),
            ('aircraft-compare', None),  # Special endpoint
        ]
        
        for endpoint_name, kwargs in endpoints:
            with self.subTest(endpoint=endpoint_name):
                if endpoint_name == 'aircraft-compare':
                    # Special handling for compare endpoint
                    url = reverse('aircraft-compare')
                    url += f'?ids={self.aircraft.id}'
                else:
                    url = reverse(endpoint_name, kwargs=kwargs) if kwargs else reverse(endpoint_name)
                
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_200_OK, 
                               f"Endpoint {endpoint_name} failed with {response.status_code}")
                
                # Ensure response is valid JSON
                try:
                    data = response.json()
                    self.assertIsInstance(data, (dict, list), 
                                        f"Endpoint {endpoint_name} returned invalid JSON")
                except (ValueError, TypeError) as e:
                    self.fail(f"Endpoint {endpoint_name} returned invalid JSON: {e}")
    
    def test_aircraft_crud_operations(self):
        """Test basic CRUD operations work end-to-end"""
        aircraft_data = {
            'manufacturer': self.manufacturer.id,
            'model': '150',
            'clean_stall_speed': '48.0',
            'top_speed': '109.0', 
            'maneuvering_speed': '89.0',
            'max_takeoff_weight': 1600,
            'seating_capacity': 2,
            'retractable_gear': False,
            'variable_pitch_prop': False,
            'verification_source': 'Cessna 150 POH'
        }
        
        # CREATE
        create_url = reverse('aircraft-list')
        response = self.client.post(create_url, aircraft_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_data = response.json()
        aircraft_id = created_data['id']
        
        # READ
        detail_url = reverse('aircraft-detail', kwargs={'pk': aircraft_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['model'], '150')
        
        # UPDATE
        aircraft_data['model'] = '150M'
        response = self.client.put(detail_url, aircraft_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['model'], '150M')
        
        # DELETE
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify deletion
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_filtering_and_search_functionality(self):
        """Test that filtering and search work correctly"""
        url = reverse('aircraft-list')
        
        # Test MOSAIC compliance filtering
        response = self.client.get(url, {'is_mosaic_compliant': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(all(a['is_mosaic_compliant'] for a in data))
        
        # Test sport pilot eligibility filtering
        response = self.client.get(url, {'sport_pilot_eligible': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(all(a['sport_pilot_eligible'] for a in data))
        
        # Test search by model
        response = self.client.get(url, {'search': '172'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(any('172' in a['model'] for a in data))
        
        # Test sorting by stall speed
        response = self.client.get(url, {'ordering': 'clean_stall_speed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        if len(data) > 1:
            stall_speeds = [float(a['clean_stall_speed']) for a in data]
            self.assertEqual(stall_speeds, sorted(stall_speeds))
    
    def test_computed_fields_accuracy(self):
        """Test that computed fields are calculated correctly"""
        url = reverse('aircraft-detail', kwargs={'pk': self.aircraft.id})
        response = self.client.get(url)
        data = response.json()
        
        # Test eligibility badges
        self.assertIn('eligibility_badges', data)
        badges = data['eligibility_badges']
        self.assertIsInstance(badges, list)
        self.assertIn('Sport Pilot', badges)  # 47 knots ≤ 59
        self.assertIn('MOSAIC Eligible', badges)  # 47 knots ≤ 61
        
        # Test performance category
        self.assertIn('performance_category', data)
        self.assertIsInstance(data['performance_category'], str)
        
        # Test MOSAIC analysis
        self.assertIn('mosaic_analysis', data)
        analysis = data['mosaic_analysis']
        self.assertIn('lsa_eligible', analysis)
        self.assertIn('sport_pilot_eligible', analysis)
        self.assertTrue(analysis['lsa_eligible'])
        self.assertTrue(analysis['sport_pilot_eligible'])
    
    def test_data_relationships(self):
        """Test that relationships between models work correctly"""
        # Test aircraft-manufacturer relationship
        detail_url = reverse('aircraft-detail', kwargs={'pk': self.aircraft.id})
        response = self.client.get(detail_url)
        data = response.json()
        
        self.assertIn('manufacturer', data)
        manufacturer_data = data['manufacturer']
        self.assertEqual(manufacturer_data['name'], 'Cessna')
        
        # Test aircraft-engines relationship
        self.assertIn('engines', data)
        engines = data['engines']
        self.assertIsInstance(engines, list)
        self.assertEqual(len(engines), 1)
        self.assertEqual(engines[0]['model'], 'O-320-E2A')
        
        # Test manufacturer aircraft endpoint
        mfg_aircraft_url = reverse('manufacturer-aircraft', kwargs={'pk': self.manufacturer.id})
        response = self.client.get(mfg_aircraft_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        aircraft_list = response.json()
        self.assertTrue(any(a['model'] == '172' for a in aircraft_list))


class IntegrationSmokeTest(TransactionTestCase):
    """Integration smoke tests that verify system components work together"""
    
    def setUp(self):
        """Set up test data for integration tests"""
        self.manufacturer = Manufacturer.objects.create(name="Piper")
        self.aircraft = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model="Cherokee",
            clean_stall_speed=Decimal('55.0'),
            top_speed=Decimal('140.0'),
            maneuvering_speed=Decimal('112.0')
        )
    
    def test_aircraft_creation_triggers_calculations(self):
        """Test that creating aircraft triggers proper field calculations"""
        # Create aircraft with stall speed that should make it sport pilot eligible
        aircraft = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model="J-3 Cub",
            clean_stall_speed=Decimal('38.0'),
            top_speed=Decimal('87.0'),
            maneuvering_speed=Decimal('70.0')
        )
        
        # Check that sport pilot eligibility was calculated
        self.assertTrue(aircraft.sport_pilot_eligible)
        self.assertTrue(aircraft.is_mosaic_compliant)
        
        # Create aircraft that exceeds MOSAIC limits
        non_mosaic = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model="Saratoga",
            clean_stall_speed=Decimal('65.0'),
            top_speed=Decimal('177.0'),
            maneuvering_speed=Decimal('142.0')
        )
        
        self.assertFalse(non_mosaic.sport_pilot_eligible)
        self.assertFalse(non_mosaic.is_mosaic_compliant)
    
    def test_correction_system_workflow(self):
        """Test the aircraft correction system workflow"""
        # Create a correction
        correction = AircraftCorrection.objects.create(
            aircraft=self.aircraft,
            field_name='clean_stall_speed',
            current_value='55.0',
            suggested_value='54.0',
            reason='POH shows 54 knots clean stall speed',
            source_documentation='Cherokee POH Section 5'
        )
        
        # Verify correction was created with proper status
        self.assertEqual(correction.status, 'PENDING')
        self.assertEqual(correction.aircraft, self.aircraft)
        
        # Simulate approval workflow
        correction.status = 'APPROVED'
        correction.admin_notes = 'Verified against POH'
        correction.save()
        
        self.assertEqual(correction.status, 'APPROVED')
        self.assertIsNotNone(correction.admin_notes)
    
    def test_database_constraints_work(self):
        """Test that database constraints prevent invalid data"""
        # Test unique manufacturer names
        with self.assertRaises(Exception):
            Manufacturer.objects.create(name="Piper")  # Duplicate name
        
        # Test engine unique together constraint
        engine = Engine.objects.create(
            manufacturer="Lycoming",
            model="O-320-E2A",
            horsepower=150,
            fuel_type='AVGAS',
            engine_type='PISTON'
        )
        
        # Should fail with duplicate manufacturer+model
        with self.assertRaises(Exception):
            Engine.objects.create(
                manufacturer="Lycoming",
                model="O-320-E2A",
                horsepower=160,
                fuel_type='AVGAS',
                engine_type='PISTON'
            )
    
    def test_api_documentation_accessible(self):
        """Test that API documentation is accessible"""
        from django.test import Client
        client = Client()
        
        # Test OpenAPI schema endpoint
        response = client.get('/api/schema/')
        self.assertEqual(response.status_code, 200)
        
        # Test Swagger UI
        response = client.get('/api/docs/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'swagger')


class PerformanceSmokeTest(APITestCase):
    """Smoke tests for API performance and scalability"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data that can be reused across test methods"""
        # Create multiple manufacturers
        cls.manufacturers = []
        for i in range(5):
            mfg = Manufacturer.objects.create(name=f"Manufacturer-{i}")
            cls.manufacturers.append(mfg)
        
        # Create multiple engines
        cls.engines = []
        for i in range(10):
            engine = Engine.objects.create(
                manufacturer=f"EngineManufacturer-{i}",
                model=f"ENGINE-{i}",
                horsepower=100 + (i * 10),
                fuel_type='AVGAS',
                engine_type='PISTON'
            )
            cls.engines.append(engine)
        
        # Create many aircraft
        cls.aircraft = []
        for i in range(50):
            stall_speed = 40 + (i * 0.5)  # Vary from 40 to 65 knots
            aircraft = Aircraft.objects.create(
                manufacturer=cls.manufacturers[i % 5],
                model=f"Model-{i}",
                clean_stall_speed=Decimal(str(stall_speed)),
                top_speed=Decimal(str(100 + i)),
                maneuvering_speed=Decimal(str(80 + i)),
                seating_capacity=2 + (i % 3),
                retractable_gear=(i % 4 == 0),
                variable_pitch_prop=(i % 3 == 0)
            )
            # Add random engines
            aircraft.engines.add(cls.engines[i % 10])
            cls.aircraft.append(aircraft)
    
    def test_list_performance_with_many_aircraft(self):
        """Test that aircraft list endpoint performs well with many records"""
        url = reverse('aircraft-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(len(data), 50)  # All aircraft should be returned
        
        # Verify computed fields are present for all aircraft
        for aircraft in data:
            self.assertIn('eligibility_badges', aircraft)
            self.assertIn('performance_category', aircraft)
            self.assertIn('speed_range', aircraft)
    
    def test_filtering_performance(self):
        """Test that filtering works efficiently with many records"""
        url = reverse('aircraft-list')
        
        # Test sport pilot filter
        response = self.client.get(url, {'sport_pilot_eligible': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(all(a['sport_pilot_eligible'] for a in data))
        
        # Test manufacturer filter
        response = self.client.get(url, {'manufacturer': self.manufacturers[0].id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 10)  # Should have 10 aircraft per manufacturer
        
        # Test complex filtering
        response = self.client.get(url, {
            'is_mosaic_compliant': True,
            'seating_capacity': 4,
            'retractable_gear': False
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return some results based on our test data
    
    def test_search_performance(self):
        """Test that search functionality works with many records"""
        url = reverse('aircraft-list')
        
        # Test model search
        response = self.client.get(url, {'search': 'Model-1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # Should find multiple matches (Model-1, Model-10, Model-11, etc.)
        self.assertGreater(len(data), 0)
        
        # Test manufacturer search
        response = self.client.get(url, {'search': 'Manufacturer-2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 10)  # Should find all aircraft from Manufacturer-2
    
    def test_sorting_performance(self):
        """Test that sorting works efficiently with many records"""
        url = reverse('aircraft-list')
        
        # Test sorting by various fields
        sort_fields = ['clean_stall_speed', 'top_speed', 'seating_capacity', 'manufacturer__name']
        
        for field in sort_fields:
            with self.subTest(sort_field=field):
                response = self.client.get(url, {'ordering': field})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                data = response.json()
                self.assertEqual(len(data), 50)
    
    def test_detail_view_with_relationships(self):
        """Test that detail views efficiently load related data"""
        aircraft = self.aircraft[0]
        url = reverse('aircraft-detail', kwargs={'pk': aircraft.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Should include manufacturer details
        self.assertIn('manufacturer', data)
        self.assertIn('name', data['manufacturer'])
        
        # Should include engines
        self.assertIn('engines', data)
        self.assertIsInstance(data['engines'], list)
        self.assertGreater(len(data['engines']), 0)
        
        # Should include computed analysis
        self.assertIn('mosaic_analysis', data)
        self.assertIn('lsa_eligible', data['mosaic_analysis'])