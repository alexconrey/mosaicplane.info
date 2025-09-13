from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date, datetime
from unittest.mock import patch
from .models import Manufacturer, Engine, Aircraft, AircraftCorrection
from .serializers import ManufacturerSerializer, AircraftSerializer, AircraftDetailSerializer
import json


class ManufacturerModelTest(TestCase):
    """Test cases for Manufacturer model"""
    
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Cessna",
            is_currently_manufacturing=True
        )
    
    def test_manufacturer_creation(self):
        """Test that a manufacturer can be created with required fields"""
        self.assertEqual(self.manufacturer.name, "Cessna")
        self.assertTrue(self.manufacturer.is_currently_manufacturing)
        self.assertIsNotNone(self.manufacturer.created_at)
        self.assertIsNotNone(self.manufacturer.updated_at)
    
    def test_manufacturer_str_representation(self):
        """Test string representation of manufacturer"""
        self.assertEqual(str(self.manufacturer), "Cessna")
    
    def test_manufacturer_unique_name(self):
        """Test that manufacturer names must be unique"""
        with self.assertRaises(Exception):
            Manufacturer.objects.create(
                name="Cessna",  # Duplicate name
                is_currently_manufacturing=False
            )
    
    def test_manufacturer_ordering(self):
        """Test that manufacturers are ordered by name"""
        boeing = Manufacturer.objects.create(name="Boeing")
        airbus = Manufacturer.objects.create(name="Airbus")
        
        manufacturers = list(Manufacturer.objects.all())
        self.assertEqual(manufacturers[0].name, "Airbus")
        self.assertEqual(manufacturers[1].name, "Boeing")
        self.assertEqual(manufacturers[2].name, "Cessna")


class EngineModelTest(TestCase):
    """Test cases for Engine model"""
    
    def setUp(self):
        self.engine = Engine.objects.create(
            manufacturer="Lycoming",
            model="O-320-E2A",
            horsepower=150,
            displacement_liters=Decimal('5.24'),
            fuel_type='AVGAS',
            engine_type='PISTON',
            is_fuel_injected=False
        )
    
    def test_engine_creation(self):
        """Test that an engine can be created with all fields"""
        self.assertEqual(self.engine.manufacturer, "Lycoming")
        self.assertEqual(self.engine.model, "O-320-E2A")
        self.assertEqual(self.engine.horsepower, 150)
        self.assertEqual(self.engine.displacement_liters, Decimal('5.24'))
        self.assertEqual(self.engine.fuel_type, 'AVGAS')
        self.assertEqual(self.engine.engine_type, 'PISTON')
        self.assertFalse(self.engine.is_fuel_injected)
    
    def test_engine_str_representation(self):
        """Test string representation of engine"""
        expected = "Lycoming O-320-E2A (150hp)"
        self.assertEqual(str(self.engine), expected)
    
    def test_engine_horsepower_validation(self):
        """Test that engine horsepower is validated within range"""
        # Test minimum validation
        with self.assertRaises(ValidationError):
            engine = Engine(
                manufacturer="Test",
                model="LOW-HP",
                horsepower=25,  # Below minimum of 50
                fuel_type='AVGAS',
                engine_type='PISTON'
            )
            engine.full_clean()
        
        # Test maximum validation
        with self.assertRaises(ValidationError):
            engine = Engine(
                manufacturer="Test",
                model="HIGH-HP",
                horsepower=500,  # Above maximum of 400
                fuel_type='AVGAS',
                engine_type='PISTON'
            )
            engine.full_clean()
    
    def test_engine_unique_together(self):
        """Test that manufacturer and model combination must be unique"""
        with self.assertRaises(Exception):
            Engine.objects.create(
                manufacturer="Lycoming",
                model="O-320-E2A",  # Duplicate manufacturer+model
                horsepower=160,
                fuel_type='AVGAS',
                engine_type='PISTON'
            )


class AircraftModelTest(TestCase):
    """Test cases for Aircraft model"""
    
    def setUp(self):
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
            retractable_gear=False,
            variable_pitch_prop=False,
            certification_date=date(1956, 1, 1)
        )
        self.aircraft.engines.add(self.engine)
    
    def test_aircraft_creation(self):
        """Test that an aircraft can be created with all fields"""
        self.assertEqual(self.aircraft.manufacturer, self.manufacturer)
        self.assertEqual(self.aircraft.model, "172")
        self.assertEqual(self.aircraft.clean_stall_speed, Decimal('47.0'))
        self.assertEqual(self.aircraft.top_speed, Decimal('126.0'))
        self.assertEqual(self.aircraft.maneuvering_speed, Decimal('99.0'))
        self.assertEqual(self.aircraft.max_takeoff_weight, 2550)
        self.assertEqual(self.aircraft.seating_capacity, 4)
        self.assertFalse(self.aircraft.retractable_gear)
        self.assertFalse(self.aircraft.variable_pitch_prop)
        self.assertTrue(self.aircraft.is_mosaic_compliant)
        self.assertTrue(self.aircraft.sport_pilot_eligible)
    
    def test_aircraft_str_representation(self):
        """Test string representation of aircraft"""
        expected = "Cessna 172"
        self.assertEqual(str(self.aircraft), expected)
    
    def test_sport_pilot_eligibility_auto_calculation(self):
        """Test that sport pilot eligibility is automatically calculated"""
        # Test sport pilot eligible (≤59 knots)
        aircraft1 = Aircraft(
            manufacturer=self.manufacturer,
            model="Test1",
            clean_stall_speed=Decimal('59.0'),
            top_speed=Decimal('120.0'),
            maneuvering_speed=Decimal('95.0')
        )
        aircraft1.save()
        self.assertTrue(aircraft1.sport_pilot_eligible)
        
        # Test not sport pilot eligible (>59 knots)
        aircraft2 = Aircraft(
            manufacturer=self.manufacturer,
            model="Test2",
            clean_stall_speed=Decimal('60.0'),
            top_speed=Decimal('130.0'),
            maneuvering_speed=Decimal('100.0')
        )
        aircraft2.save()
        self.assertFalse(aircraft2.sport_pilot_eligible)
    
    def test_mosaic_compliance_calculation(self):
        """Test that MOSAIC compliance is automatically calculated"""
        # Test MOSAIC compliant (≤61 knots)
        aircraft1 = Aircraft(
            manufacturer=self.manufacturer,
            model="MOSAIC1",
            clean_stall_speed=Decimal('61.0'),
            top_speed=Decimal('130.0'),
            maneuvering_speed=Decimal('105.0')
        )
        aircraft1.save()
        self.assertTrue(aircraft1.is_mosaic_compliant)
        
        # Test not MOSAIC compliant (>61 knots)
        aircraft2 = Aircraft(
            manufacturer=self.manufacturer,
            model="MOSAIC2",
            clean_stall_speed=Decimal('62.0'),
            top_speed=Decimal('140.0'),
            maneuvering_speed=Decimal('110.0')
        )
        aircraft2.save()
        self.assertFalse(aircraft2.is_mosaic_compliant)
    
    def test_certification_date_impact(self):
        """Test that certification date affects MOSAIC compliance"""
        # Test legacy aircraft (certified before July 24, 2026)
        legacy_aircraft = Aircraft(
            manufacturer=self.manufacturer,
            model="Legacy",
            clean_stall_speed=Decimal('60.0'),
            top_speed=Decimal('130.0'),
            maneuvering_speed=Decimal('100.0'),
            certification_date=date(2020, 1, 1)  # Before MOSAIC cert date
        )
        legacy_aircraft.save()
        self.assertTrue(legacy_aircraft.is_mosaic_compliant)  # Meets stall speed requirement
        
        # Test new aircraft (certified after July 24, 2026)
        new_aircraft = Aircraft(
            manufacturer=self.manufacturer,
            model="NewMOSAIC",
            clean_stall_speed=Decimal('60.0'),
            top_speed=Decimal('130.0'),
            maneuvering_speed=Decimal('100.0'),
            certification_date=date(2027, 1, 1)  # After MOSAIC cert date
        )
        new_aircraft.save()
        self.assertTrue(new_aircraft.is_mosaic_compliant)  # Meets stall speed requirement
    
    def test_stall_speed_validation(self):
        """Test that stall speed is validated within MOSAIC limits"""
        with self.assertRaises(ValidationError):
            aircraft = Aircraft(
                manufacturer=self.manufacturer,
                model="FastStall",
                clean_stall_speed=Decimal('62.0'),  # Above MOSAIC LSA limit
                top_speed=Decimal('130.0'),
                maneuvering_speed=Decimal('100.0')
            )
            aircraft.full_clean()
    
    def test_seating_capacity_validation(self):
        """Test that seating capacity is validated within MOSAIC limits"""
        # Test maximum seating capacity
        with self.assertRaises(ValidationError):
            aircraft = Aircraft(
                manufacturer=self.manufacturer,
                model="BigPlane",
                clean_stall_speed=Decimal('50.0'),
                top_speed=Decimal('120.0'),
                maneuvering_speed=Decimal('95.0'),
                seating_capacity=5  # Above MOSAIC limit of 4
            )
            aircraft.full_clean()
        
        # Test minimum seating capacity
        with self.assertRaises(ValidationError):
            aircraft = Aircraft(
                manufacturer=self.manufacturer,
                model="NoSeats",
                clean_stall_speed=Decimal('50.0'),
                top_speed=Decimal('120.0'),
                maneuvering_speed=Decimal('95.0'),
                seating_capacity=0  # Below minimum of 1
            )
            aircraft.full_clean()


class AircraftCorrectionModelTest(TestCase):
    """Test cases for AircraftCorrection model"""
    
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Piper")
        self.aircraft = Aircraft.objects.create(
            manufacturer=self.manufacturer,
            model="Cherokee",
            clean_stall_speed=Decimal('55.0'),
            top_speed=Decimal('140.0'),
            maneuvering_speed=Decimal('112.0')
        )
        self.correction = AircraftCorrection.objects.create(
            aircraft=self.aircraft,
            field_name='clean_stall_speed',
            current_value='55.0',
            suggested_value='54.0',
            reason='POH shows clean stall speed as 54 knots, not 55',
            source_documentation='Cherokee POH Section 5, page 5-2',
            submitter_email='pilot@example.com',
            submitter_name='Test Pilot'
        )
    
    def test_correction_creation(self):
        """Test that a correction can be created with all fields"""
        self.assertEqual(self.correction.aircraft, self.aircraft)
        self.assertEqual(self.correction.field_name, 'clean_stall_speed')
        self.assertEqual(self.correction.current_value, '55.0')
        self.assertEqual(self.correction.suggested_value, '54.0')
        self.assertEqual(self.correction.status, 'PENDING')
        self.assertIsNotNone(self.correction.created_at)
    
    def test_correction_str_representation(self):
        """Test string representation of correction"""
        expected = "Correction for Piper Cherokee - Clean stall speed (PENDING)"
        self.assertEqual(str(self.correction), expected)
    
    def test_correction_status_choices(self):
        """Test that correction status can be updated"""
        self.correction.status = 'APPROVED'
        self.correction.save()
        self.assertEqual(self.correction.status, 'APPROVED')
        
        self.correction.status = 'IMPLEMENTED'
        self.correction.admin_notes = 'Updated clean stall speed in database'
        self.correction.save()
        self.assertEqual(self.correction.status, 'IMPLEMENTED')
        self.assertIsNotNone(self.correction.admin_notes)
