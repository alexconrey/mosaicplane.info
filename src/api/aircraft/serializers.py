from rest_framework import serializers
from .models import Manufacturer, Aircraft, Engine, AircraftCorrection


class ManufacturerSerializer(serializers.ModelSerializer):
    aircraft_count = serializers.SerializerMethodField()

    class Meta:
        model = Manufacturer
        fields = [
            'id',
            'name',
            'logo',
            'is_currently_manufacturing',
            'aircraft_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_aircraft_count(self, obj):
        return obj.aircraft.count()


class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engine
        fields = [
            'id',
            'manufacturer',
            'model',
            'horsepower',
            'displacement_liters',
            'fuel_type',
            'engine_type',
            'is_fuel_injected',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AircraftSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.CharField(source='manufacturer.name', read_only=True)
    engines = EngineSerializer(many=True, read_only=True)
    eligibility_badges = serializers.SerializerMethodField()
    performance_category = serializers.SerializerMethodField()
    speed_range = serializers.SerializerMethodField()

    class Meta:
        model = Aircraft
        fields = [
            'id',
            'manufacturer',
            'manufacturer_name',
            'model',
            'clean_stall_speed',
            'top_speed',
            'maneuvering_speed',
            'cruise_speed',
            'vx_speed',
            'vy_speed',
            'vs0_speed',
            'vg_speed',
            'vfe_speed',
            'vno_speed',
            'vne_speed',
            'max_takeoff_weight',
            'seating_capacity',
            'retractable_gear',
            'variable_pitch_prop',
            'certification_date',
            'verification_source',
            'image',
            'engines',
            'is_mosaic_compliant',
            'sport_pilot_eligible',
            'eligibility_badges',
            'performance_category',
            'speed_range',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_mosaic_compliant', 'sport_pilot_eligible']
    
    def get_eligibility_badges(self, obj):
        """Return list of eligibility badges for the aircraft"""
        badges = []
        
        if obj.sport_pilot_eligible:
            badges.append('Sport Pilot')
        elif obj.is_mosaic_compliant:
            badges.append('Private Pilot')
        
        if not obj.is_mosaic_compliant:
            badges.append('Not MOSAIC Eligible')
        elif obj.is_mosaic_compliant:
            badges.append('MOSAIC Eligible')
            
        if obj.retractable_gear:
            badges.append('RG')
            
        if obj.variable_pitch_prop:
            badges.append('VP')
            
        return badges
    
    def get_performance_category(self, obj):
        """Categorize aircraft by performance"""
        if obj.top_speed >= 200:
            return 'High Performance'
        elif obj.top_speed >= 140:
            return 'Cross Country'
        else:
            return 'Standard Performance'
    
    def get_speed_range(self, obj):
        """Return speed range category"""
        stall = float(obj.clean_stall_speed)
        top = float(obj.top_speed)
        
        if stall <= 45 and top <= 120:
            return 'Trainer'
        elif stall <= 55 and top <= 150:
            return 'Sport'
        elif stall <= 65 and top <= 180:
            return 'Touring'
        else:
            return 'High Performance'


class AircraftDetailSerializer(AircraftSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)
    mosaic_analysis = serializers.SerializerMethodField()

    class Meta(AircraftSerializer.Meta):
        fields = AircraftSerializer.Meta.fields + ['mosaic_analysis']
    
    def get_mosaic_analysis(self, obj):
        """Return detailed MOSAIC analysis"""
        from datetime import date
        
        mosaic_cert_date = date(2026, 7, 24)
        is_legacy = obj.certification_date and obj.certification_date < mosaic_cert_date
        
        return {
            'lsa_eligible': obj.is_mosaic_compliant,
            'sport_pilot_eligible': obj.sport_pilot_eligible,
            'certification_era': 'Legacy' if is_legacy else 'New' if obj.certification_date else 'Unknown',
            'stall_speed_status': 'Within LSA limits' if obj.clean_stall_speed <= 61 else 'Exceeds LSA limits',
            'endorsements_required': obj.retractable_gear or obj.variable_pitch_prop,
            'passenger_limitation': 'Sport pilot limited to 1 passenger' if obj.sport_pilot_eligible else None
        }


class AircraftCorrectionSerializer(serializers.ModelSerializer):
    aircraft_name = serializers.CharField(source='aircraft.__str__', read_only=True)
    field_name_display = serializers.CharField(source='get_field_name_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AircraftCorrection
        fields = [
            'id',
            'aircraft',
            'aircraft_name',
            'field_name',
            'field_name_display',
            'current_value',
            'suggested_value',
            'reason',
            'source_documentation',
            'submitter_email',
            'submitter_name',
            'status',
            'status_display',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'status']

    def create(self, validated_data):
        # Auto-populate current_value from the aircraft
        aircraft = validated_data['aircraft']
        field_name = validated_data['field_name']
        
        if field_name == 'engines':
            current_value = ', '.join([str(engine) for engine in aircraft.engines.all()])
        elif hasattr(aircraft, field_name):
            current_value = str(getattr(aircraft, field_name, ''))
        else:
            current_value = ''
            
        validated_data['current_value'] = current_value
        return super().create(validated_data)