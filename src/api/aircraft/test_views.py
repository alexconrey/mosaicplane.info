from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date
from .models import Manufacturer, Engine, Aircraft, AircraftCorrection
import json


class ManufacturerViewSetTest(APITestCase):
    """Test cases for ManufacturerViewSet API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.manufacturer1 = Manufacturer.objects.create(
            name="Cessna",
            is_currently_manufacturing=True
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Piper", 
            is_currently_manufacturing=True
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Beechcraft",
            is_currently_manufacturing=False
        )
    
    def test_list_manufacturers(self):
        """Test GET /api/manufacturers/ returns all manufacturers"""
        url = reverse('manufacturer-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Should return all 3 manufacturers
        self.assertEqual(len(data), 3)
        
        # Should be ordered by name (Beechcraft, Cessna, Piper)
        names = [m['name'] for m in data]
        self.assertEqual(names, ['Beechcraft', 'Cessna', 'Piper'])
    
    def test_filter_manufacturers_by_manufacturing_status(self):
        """Test filtering manufacturers by is_currently_manufacturing"""
        url = reverse('manufacturer-list')
        
        # Test active manufacturers
        response = self.client.get(url, {'is_currently_manufacturing': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)  # Cessna and Piper
        
        # Test inactive manufacturers
        response = self.client.get(url, {'is_currently_manufacturing': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)  # Only Beechcraft
        self.assertEqual(data[0]['name'], 'Beechcraft')
    
    def test_search_manufacturers(self):
        """Test searching manufacturers by name"""
        url = reverse('manufacturer-list')
        
        response = self.client.get(url, {'search': 'Cessna'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Cessna')
        
        # Test partial search
        response = self.client.get(url, {'search': 'Pi'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Piper')
    
    def test_get_manufacturer_detail(self):
        """Test GET /api/manufacturers/{id}/ returns manufacturer details"""
        url = reverse('manufacturer-detail', kwargs={'pk': self.manufacturer1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertEqual(data['name'], 'Cessna')
        self.assertTrue(data['is_currently_manufacturing'])
        self.assertIn('id', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_manufacturer_aircraft_endpoint(self):
        """Test GET /api/manufacturers/{id}/aircraft/ returns manufacturer's aircraft"""
        # Create aircraft for manufacturer
        aircraft1 = Aircraft.objects.create(
            manufacturer=self.manufacturer1,
            model='172',
            clean_stall_speed=Decimal('47.0'),
            top_speed=Decimal('126.0'),
            maneuvering_speed=Decimal('99.0')
        )
        aircraft2 = Aircraft.objects.create(
            manufacturer=self.manufacturer1,
            model='182',
            clean_stall_speed=Decimal('56.0'),
            top_speed=Decimal('145.0'),
            maneuvering_speed=Decimal('119.0')
        )
        
        url = reverse('manufacturer-aircraft', kwargs={'pk': self.manufacturer1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertEqual(len(data), 2)
        models = [a['model'] for a in data]
        self.assertIn('172', models)
        self.assertIn('182', models)
    
    def test_create_manufacturer(self):
        """Test POST /api/manufacturers/ creates new manufacturer"""
        url = reverse('manufacturer-list')
        data = {
            'name': 'Boeing',
            'is_currently_manufacturing': True
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify manufacturer was created
        self.assertTrue(Manufacturer.objects.filter(name='Boeing').exists())
        
        # Verify response data
        response_data = response.json()
        self.assertEqual(response_data['name'], 'Boeing')
        self.assertTrue(response_data['is_currently_manufacturing'])
    
    def test_update_manufacturer(self):
        """Test PUT /api/manufacturers/{id}/ updates manufacturer"""
        url = reverse('manufacturer-detail', kwargs={'pk': self.manufacturer1.id})
        data = {
            'name': 'Cessna Aircraft Company',
            'is_currently_manufacturing': False
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify manufacturer was updated
        self.manufacturer1.refresh_from_db()
        self.assertEqual(self.manufacturer1.name, 'Cessna Aircraft Company')
        self.assertFalse(self.manufacturer1.is_currently_manufacturing)
    
    def test_delete_manufacturer(self):
        """Test DELETE /api/manufacturers/{id}/ deletes manufacturer"""
        url = reverse('manufacturer-detail', kwargs={'pk': self.manufacturer3.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify manufacturer was deleted
        self.assertFalse(Manufacturer.objects.filter(id=self.manufacturer3.id).exists())


class AircraftViewSetTest(APITestCase):
    """Test cases for AircraftViewSet API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
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
        
        # Create test aircraft
        self.aircraft1 = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model='172',
            clean_stall_speed=Decimal('47.0'),
            top_speed=Decimal('126.0'),
            maneuvering_speed=Decimal('99.0'),
            max_takeoff_weight=2550,
            seating_capacity=4,
            retractable_gear=False,
            variable_pitch_prop=False,
            certification_date=date(1956, 1, 1)
        )
        self.aircraft1.engines.add(self.engine)
        
        self.aircraft2 = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model='182',
            clean_stall_speed=Decimal('60.0'),  # Above sport pilot limit
            top_speed=Decimal('145.0'),
            maneuvering_speed=Decimal('119.0'),
            max_takeoff_weight=3100,
            seating_capacity=4,
            retractable_gear=False,
            variable_pitch_prop=True
        )
        
        self.aircraft3 = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model='210',
            clean_stall_speed=Decimal('62.0'),  # Not MOSAIC compliant
            top_speed=Decimal('175.0'),
            maneuvering_speed=Decimal('140.0'),
            max_takeoff_weight=4100,
            seating_capacity=6,
            retractable_gear=True,
            variable_pitch_prop=True
        )
    
    def test_list_aircraft(self):
        """Test GET /api/aircraft/ returns all aircraft"""
        url = reverse('aircraft-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Should return all 3 aircraft
        self.assertEqual(len(data), 3)
        
        # Should be ordered by manufacturer name, then model
        models = [a['model'] for a in data]
        self.assertEqual(models, ['172', '182', '210'])
    
    def test_filter_aircraft_by_mosaic_compliance(self):
        """Test filtering aircraft by MOSAIC compliance"""
        url = reverse('aircraft-list')
        
        # Test MOSAIC compliant aircraft
        response = self.client.get(url, {'is_mosaic_compliant': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)  # 172 and 182
        
        # Test non-MOSAIC compliant aircraft
        response = self.client.get(url, {'is_mosaic_compliant': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)  # Only 210
        self.assertEqual(data[0]['model'], '210')
    
    def test_filter_aircraft_by_sport_pilot_eligibility(self):
        """Test filtering aircraft by sport pilot eligibility"""
        url = reverse('aircraft-list')
        
        # Test sport pilot eligible aircraft
        response = self.client.get(url, {'sport_pilot_eligible': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)  # Only 172
        self.assertEqual(data[0]['model'], '172')
        
        # Test non-sport pilot eligible aircraft
        response = self.client.get(url, {'sport_pilot_eligible': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)  # 182 and 210
    
    def test_filter_aircraft_by_seating_capacity(self):
        """Test filtering aircraft by seating capacity"""
        url = reverse('aircraft-list')
        
        response = self.client.get(url, {'seating_capacity': 4})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)  # 172 and 182
        
        response = self.client.get(url, {'seating_capacity': 6})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)  # Only 210
        self.assertEqual(data[0]['model'], '210')
    
    def test_filter_aircraft_by_gear_type(self):
        """Test filtering aircraft by retractable gear"""
        url = reverse('aircraft-list')
        
        # Test fixed gear aircraft
        response = self.client.get(url, {'retractable_gear': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)  # 172 and 182
        
        # Test retractable gear aircraft
        response = self.client.get(url, {'retractable_gear': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)  # Only 210
        self.assertEqual(data[0]['model'], '210')
    
    def test_filter_aircraft_by_propeller_type(self):
        """Test filtering aircraft by variable pitch propeller"""
        url = reverse('aircraft-list')
        
        # Test fixed pitch propeller aircraft
        response = self.client.get(url, {'variable_pitch_prop': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)  # Only 172
        self.assertEqual(data[0]['model'], '172')
        
        # Test variable pitch propeller aircraft
        response = self.client.get(url, {'variable_pitch_prop': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 2)  # 182 and 210
    
    def test_search_aircraft(self):
        """Test searching aircraft by model and manufacturer"""
        url = reverse('aircraft-list')
        
        # Test search by model
        response = self.client.get(url, {'search': '172'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['model'], '172')
        
        # Test search by manufacturer name
        response = self.client.get(url, {'search': 'Cessna'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 3)  # All aircraft are Cessna
    
    def test_sort_aircraft(self):
        """Test sorting aircraft by various fields"""
        url = reverse('aircraft-list')
        
        # Test sort by stall speed ascending
        response = self.client.get(url, {'ordering': 'clean_stall_speed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        stall_speeds = [float(a['clean_stall_speed']) for a in data]
        self.assertEqual(stall_speeds, [47.0, 60.0, 62.0])
        
        # Test sort by stall speed descending
        response = self.client.get(url, {'ordering': '-clean_stall_speed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        stall_speeds = [float(a['clean_stall_speed']) for a in data]
        self.assertEqual(stall_speeds, [62.0, 60.0, 47.0])
        
        # Test sort by top speed
        response = self.client.get(url, {'ordering': 'top_speed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        top_speeds = [float(a['top_speed']) for a in data]
        self.assertEqual(top_speeds, [126.0, 145.0, 175.0])
    
    def test_get_aircraft_detail(self):
        """Test GET /api/aircraft/{id}/ returns detailed aircraft info"""
        url = reverse('aircraft-detail', kwargs={'pk': self.aircraft1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Should include basic info
        self.assertEqual(data['model'], '172')
        self.assertEqual(float(data['clean_stall_speed']), 47.0)
        
        # Should include manufacturer details
        self.assertIn('manufacturer', data)
        self.assertEqual(data['manufacturer']['name'], 'Cessna')
        
        # Should include engines (detail serializer)
        self.assertIn('engines', data)
        self.assertEqual(len(data['engines']), 1)
        engine = data['engines'][0]
        self.assertEqual(engine['manufacturer'], 'Lycoming')
        self.assertEqual(engine['model'], 'O-320-E2A')
        
        # Should include computed fields
        self.assertIn('eligibility_badges', data)
        self.assertIn('performance_category', data)
        self.assertIn('mosaic_analysis', data)
    
    def test_compare_aircraft_endpoint(self):
        """Test GET /api/aircraft/compare/ compares multiple aircraft"""
        url = reverse('aircraft-compare')
        
        # Test comparing two aircraft
        response = self.client.get(url, {'ids': f'{self.aircraft1.id},{self.aircraft2.id}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertEqual(len(data), 2)
        models = [a['model'] for a in data]
        self.assertIn('172', models)
        self.assertIn('182', models)
        
        # Should include engines for all aircraft (detail serializer)
        for aircraft in data:
            self.assertIn('engines', aircraft)
            self.assertIn('mosaic_analysis', aircraft)
    
    def test_compare_aircraft_invalid_ids(self):
        """Test compare endpoint with invalid aircraft IDs"""
        url = reverse('aircraft-compare')
        
        # Test with no IDs
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
        
        # Test with invalid ID format
        response = self.client.get(url, {'ids': 'abc,def'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
        
        # Test with non-existent IDs
        response = self.client.get(url, {'ids': '9999,8888'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 0)  # No aircraft found
    
    def test_create_aircraft(self):
        """Test POST /api/aircraft/ creates new aircraft"""
        url = reverse('aircraft-list')
        data = {
            'manufacturer': self.manufacturer.id,
            'model': '150',
            'clean_stall_speed': '48.0',
            'top_speed': '109.0',
            'maneuvering_speed': '89.0',
            'max_takeoff_weight': 1600,
            'seating_capacity': 2,
            'retractable_gear': False,
            'variable_pitch_prop': False,
            'certification_date': '1957-09-12',
            'verification_source': 'Cessna 150 POH'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify aircraft was created
        aircraft = Aircraft.objects.get(model='150')
        self.assertEqual(aircraft.clean_stall_speed, Decimal('48.0'))
        self.assertTrue(aircraft.sport_pilot_eligible)  # Should be auto-calculated
        self.assertTrue(aircraft.is_mosaic_compliant)
    
    def test_update_aircraft(self):
        """Test PUT /api/aircraft/{id}/ updates aircraft"""
        url = reverse('aircraft-detail', kwargs={'pk': self.aircraft1.id})
        data = {
            'manufacturer': self.manufacturer.id,
            'model': '172N',
            'clean_stall_speed': '49.0',  # Updated stall speed
            'top_speed': '126.0',
            'maneuvering_speed': '99.0',
            'max_takeoff_weight': 2550,
            'seating_capacity': 4,
            'retractable_gear': False,
            'variable_pitch_prop': False,
            'certification_date': '1956-01-01',
            'verification_source': 'Updated Cessna 172N POH'
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify aircraft was updated
        self.aircraft1.refresh_from_db()
        self.assertEqual(self.aircraft1.model, '172N')
        self.assertEqual(self.aircraft1.clean_stall_speed, Decimal('49.0'))
    
    def test_delete_aircraft(self):
        """Test DELETE /api/aircraft/{id}/ deletes aircraft"""
        url = reverse('aircraft-detail', kwargs={'pk': self.aircraft3.id})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify aircraft was deleted
        self.assertFalse(Aircraft.objects.filter(id=self.aircraft3.id).exists())


class AircraftAPIIntegrationTest(APITestCase):
    """Integration tests for aircraft API with complex scenarios"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create manufacturers
        self.cessna = Manufacturer.objects.create(name="Cessna", is_currently_manufacturing=True)
        self.piper = Manufacturer.objects.create(name="Piper", is_currently_manufacturing=True)
        
        # Create engines
        self.engine1 = Engine.objects.create(
            manufacturer="Lycoming", model="O-320-E2A", horsepower=150,
            fuel_type='AVGAS', engine_type='PISTON'
        )
        self.engine2 = Engine.objects.create(
            manufacturer="Continental", model="O-200-A", horsepower=100,
            fuel_type='AVGAS', engine_type='PISTON'
        )
        
        # Create diverse aircraft portfolio
        self.create_test_aircraft()
    
    def create_test_aircraft(self):
        """Create a realistic set of test aircraft"""
        # Sport pilot eligible aircraft
        self.cessna_150 = Aircraft.objects.create(
            manufacturer=self.cessna, model='150',
            clean_stall_speed=Decimal('48.0'), top_speed=Decimal('109.0'),
            maneuvering_speed=Decimal('89.0'), seating_capacity=2,
            certification_date=date(1957, 9, 12)
        )
        self.cessna_150.engines.add(self.engine2)
        
        # MOSAIC eligible but not sport pilot  
        self.cessna_172 = Aircraft.objects.create(
            manufacturer=self.cessna, model='172',
            clean_stall_speed=Decimal('60.0'), top_speed=Decimal('126.0'),
            maneuvering_speed=Decimal('99.0'), seating_capacity=4,
            certification_date=date(1956, 1, 1)
        )
        self.cessna_172.engines.add(self.engine1)
        
        # Not MOSAIC eligible
        self.piper_saratoga = Aircraft.objects.create(
            manufacturer=self.piper, model='Saratoga',
            clean_stall_speed=Decimal('65.0'), top_speed=Decimal('177.0'),
            maneuvering_speed=Decimal('142.0'), seating_capacity=6,
            retractable_gear=True, variable_pitch_prop=True
        )
        
        # Complex aircraft with endorsements (not sport pilot eligible)
        self.cessna_182rg = Aircraft.objects.create(
            manufacturer=self.cessna, model='182RG',
            clean_stall_speed=Decimal('60.0'), top_speed=Decimal('155.0'),
            maneuvering_speed=Decimal('119.0'), seating_capacity=4,
            retractable_gear=True, variable_pitch_prop=True
        )
    
    def test_complex_filtering_scenario(self):
        """Test complex multi-field filtering scenarios"""
        url = reverse('aircraft-list')
        
        # Find MOSAIC eligible 4-seat aircraft without retractable gear
        response = self.client.get(url, {
            'is_mosaic_compliant': True,
            'seating_capacity': 4,
            'retractable_gear': False
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['model'], '172')
    
    def test_realistic_user_search_patterns(self):
        """Test realistic user search patterns"""
        url = reverse('aircraft-list')
        
        # User looking for sport pilot aircraft
        response = self.client.get(url, {'sport_pilot_eligible': True})
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['model'], '150')
        
        # User looking for 4-seat MOSAIC aircraft
        response = self.client.get(url, {
            'is_mosaic_compliant': True,
            'seating_capacity': 4
        })
        data = response.json()
        self.assertEqual(len(data), 2)  # 172 and 182RG
        models = [a['model'] for a in data]
        self.assertIn('172', models)
        self.assertIn('182RG', models)
        
        # User looking for aircraft requiring endorsements
        response = self.client.get(url, {'retractable_gear': True})
        data = response.json()
        endorsement_aircraft = [a['model'] for a in data]
        self.assertIn('Saratoga', endorsement_aircraft)
        self.assertIn('182RG', endorsement_aircraft)
    
    def test_api_data_consistency(self):
        """Test that API data is consistent across endpoints"""
        # Get aircraft from list endpoint
        list_url = reverse('aircraft-list')
        list_response = self.client.get(list_url)
        list_data = list_response.json()
        
        cessna_150_list = next((a for a in list_data if a['model'] == '150'), None)
        self.assertIsNotNone(cessna_150_list)
        
        # Get same aircraft from detail endpoint
        detail_url = reverse('aircraft-detail', kwargs={'pk': self.cessna_150.id})
        detail_response = self.client.get(detail_url)
        detail_data = detail_response.json()
        
        # Compare common fields (excluding manufacturer since list has ID, detail has nested object)
        common_fields = ['model', 'clean_stall_speed', 'top_speed', 'seating_capacity',
                        'sport_pilot_eligible', 'is_mosaic_compliant']
        
        for field in common_fields:
            self.assertEqual(cessna_150_list[field], detail_data[field],
                           f"Field {field} differs between list and detail")
        
        # Check manufacturer consistency (list has ID, detail has nested object)
        self.assertEqual(cessna_150_list['manufacturer'], detail_data['manufacturer']['id'])
    
    def test_eligibility_badges_accuracy(self):
        """Test that eligibility badges are computed accurately"""
        url = reverse('aircraft-list')
        response = self.client.get(url)
        aircraft_data = {a['model']: a for a in response.json()}
        
        # Cessna 150: Sport pilot eligible
        badges_150 = aircraft_data['150']['eligibility_badges']
        self.assertIn('Sport Pilot', badges_150)
        self.assertIn('MOSAIC Eligible', badges_150)
        
        # Cessna 172: MOSAIC eligible but not sport pilot
        badges_172 = aircraft_data['172']['eligibility_badges']
        self.assertIn('Private Pilot', badges_172)
        self.assertIn('MOSAIC Eligible', badges_172)
        self.assertNotIn('Sport Pilot', badges_172)
        
        # Cessna 182RG: Requires endorsements
        badges_182rg = aircraft_data['182RG']['eligibility_badges']
        self.assertIn('RG', badges_182rg)
        self.assertIn('VP', badges_182rg)
        
        # Piper Saratoga: Not MOSAIC eligible
        badges_saratoga = aircraft_data['Saratoga']['eligibility_badges']
        self.assertIn('Not MOSAIC Eligible', badges_saratoga)
        self.assertIn('RG', badges_saratoga)
        self.assertIn('VP', badges_saratoga)
    
    def test_performance_edge_cases(self):
        """Test API performance with edge cases and error conditions"""
        # Test with non-existent manufacturer filter 
        url = reverse('aircraft-list')
        response = self.client.get(url, {'manufacturer': 99999})
        # Django-filters may return 400 for non-existent foreign keys or return empty results
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(len(response.json()), 0)
        
        # Test with invalid sorting field (should return 400 or ignore)
        response = self.client.get(url, {'ordering': 'invalid_field'})
        # API may return 400 for invalid fields or ignore them - both are acceptable
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
        
        # Test with extreme filter values
        response = self.client.get(url, {'seating_capacity': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
    
    def test_api_response_structure(self):
        """Test that API responses have consistent structure"""
        # Test aircraft list response structure
        url = reverse('aircraft-list')
        response = self.client.get(url)
        data = response.json()
        
        required_fields = [
            'id', 'manufacturer', 'model', 'clean_stall_speed', 'top_speed',
            'maneuvering_speed', 'seating_capacity', 'sport_pilot_eligible',
            'is_mosaic_compliant', 'eligibility_badges', 'performance_category'
        ]
        
        for aircraft in data:
            for field in required_fields:
                self.assertIn(field, aircraft, f"Missing field {field} in aircraft {aircraft.get('model', 'unknown')}")
            
            # Test manufacturer field (should be ID in list view)
            manufacturer = aircraft['manufacturer']
            self.assertIsInstance(manufacturer, int, "Manufacturer should be ID in list view")
        
        # Test aircraft detail response structure
        detail_url = reverse('aircraft-detail', kwargs={'pk': self.cessna_150.id})
        detail_response = self.client.get(detail_url)
        detail_data = detail_response.json()
        
        # Should include all list fields plus additional detail fields
        detail_fields = required_fields + ['engines', 'mosaic_analysis', 'verification_source']
        for field in detail_fields:
            self.assertIn(field, detail_data, f"Missing detail field {field}")
        
        # Test manufacturer nested structure in detail view
        detail_manufacturer = detail_data['manufacturer']
        manufacturer_fields = ['id', 'name', 'is_currently_manufacturing']
        for field in manufacturer_fields:
            self.assertIn(field, detail_manufacturer, f"Missing manufacturer field {field}")
        
        # Test engine structure within detail
        self.assertIsInstance(detail_data['engines'], list)
        if detail_data['engines']:
            engine = detail_data['engines'][0]
            engine_fields = ['id', 'manufacturer', 'model', 'horsepower', 'fuel_type', 'engine_type']
            for field in engine_fields:
                self.assertIn(field, engine, f"Missing engine field {field}")