from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.URLField(
        blank=True,
        null=True,
        help_text="URL to manufacturer logo image"
    )
    is_currently_manufacturing = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'manufacturers'
        ordering = ['name']

    def __str__(self):
        return self.name


class Engine(models.Model):
    FUEL_TYPE_CHOICES = [
        ('AVGAS', 'Avgas (100LL/91UL)'),
        ('MOGAS', 'Automotive gasoline (91+ octane)'),
        ('DIESEL', 'Jet A / Diesel'),
        ('ELECTRIC', 'Electric'),
    ]
    
    ENGINE_TYPE_CHOICES = [
        ('PISTON', 'Piston engine'),
        ('TURBOPROP', 'Turboprop'),
        ('ELECTRIC', 'Electric motor'),
    ]
    
    manufacturer = models.CharField(max_length=100, help_text="Engine manufacturer (e.g., Lycoming, Continental, Rotax)")
    model = models.CharField(max_length=100, help_text="Engine model designation (e.g., O-320-E2A, 912ULS)")
    horsepower = models.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(400)  # Reasonable range for LSA/GA engines
        ],
        help_text="Rated horsepower"
    )
    displacement_liters = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Engine displacement in liters"
    )
    fuel_type = models.CharField(
        max_length=10,
        choices=FUEL_TYPE_CHOICES,
        default='AVGAS',
        help_text="Primary fuel type"
    )
    engine_type = models.CharField(
        max_length=15,
        choices=ENGINE_TYPE_CHOICES,
        default='PISTON',
        help_text="Engine type"
    )
    is_fuel_injected = models.BooleanField(
        default=False,
        help_text="Fuel injected (vs. carbureted)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'engines'
        ordering = ['manufacturer', 'model']
        unique_together = ['manufacturer', 'model']

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.horsepower}hp)"


class Aircraft(models.Model):
    manufacturer = models.ForeignKey(
        Manufacturer, 
        on_delete=models.CASCADE,
        related_name='aircraft'
    )
    model = models.CharField(max_length=100)
    clean_stall_speed = models.DecimalField(
        max_digits=5, 
        decimal_places=1,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(61.0)  # MOSAIC LSA certification limit
        ],
        help_text="Clean stall speed (Vs1) in knots CAS (max 61 for MOSAIC LSA, max 59 for sport pilot)"
    )
    top_speed = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(999.0)  # Reasonable maximum
        ],
        help_text="Maximum speed in knots"
    )
    maneuvering_speed = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(999.0)  # Reasonable maximum
        ],
        help_text="Maneuvering speed (Va) in knots"
    )
    cruise_speed = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(999.0)  # Reasonable maximum
        ],
        help_text="Cruise speed in knots (typically 75% power at optimal altitude)"
    )
    vx_speed = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(999.0)
        ],
        help_text="Best angle of climb speed (Vx) in knots"
    )
    vy_speed = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(999.0)
        ],
        help_text="Best rate of climb speed (Vy) in knots"
    )
    vs0_speed = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(999.0)
        ],
        help_text="Stall speed in landing configuration (Vs0) in knots"
    )
    vg_speed = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(999.0)
        ],
        help_text="Best glide speed (Vg) in knots"
    )
    vfe_speed = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(999.0)
        ],
        help_text="Maximum flap extended speed (Vfe) in knots"
    )
    vno_speed = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(999.0)
        ],
        help_text="Maximum structural cruising speed (Vno) in knots"
    )
    vne_speed = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(999.0)
        ],
        help_text="Never exceed speed (Vne) in knots"
    )
    max_takeoff_weight = models.IntegerField(
        null=True, 
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(99999)  # No weight limit under MOSAIC for LSA
        ],
        help_text="Maximum takeoff weight in pounds (no limit under MOSAIC)"
    )
    seating_capacity = models.IntegerField(
        default=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4)  # MOSAIC allows up to 4 seats for LSA
        ],
        help_text="Number of seats in aircraft (max 4 under MOSAIC, but sport pilot limited to 1 passenger)"
    )
    retractable_gear = models.BooleanField(
        default=False,
        help_text="Aircraft has retractable landing gear"
    )
    variable_pitch_prop = models.BooleanField(
        default=False,
        help_text="Aircraft has variable pitch propeller"
    )
    is_mosaic_compliant = models.BooleanField(default=True)
    sport_pilot_eligible = models.BooleanField(
        default=True,
        help_text="Eligible for sport pilot operation under MOSAIC (≤59 knots stall speed)"
    )
    certification_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date aircraft was first certificated (affects MOSAIC LSA eligibility - new aircraft require certification after July 24, 2026)"
    )
    verification_source = models.TextField(
        blank=True,
        help_text="Source of data verification (POH, manufacturer specs, FAA documents, etc.)"
    )
    image = models.ImageField(
        upload_to='aircraft_images/',
        blank=True,
        null=True,
        help_text="Representative image of the aircraft model"
    )
    engines = models.ManyToManyField(
        Engine,
        blank=True,
        related_name='aircraft',
        help_text="Available engine configurations for this aircraft model"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'aircraft'
        ordering = ['manufacturer__name', 'model']
        unique_together = ['manufacturer', 'model']

    def clean(self):
        super().clean()
        # Automatically set sport pilot eligibility based on stall speed
        if self.clean_stall_speed is not None:
            self.sport_pilot_eligible = self.clean_stall_speed <= 59.0
        
        # Validate MOSAIC compliance based on stall speed and certification date
        if self.clean_stall_speed is not None:
            # Basic stall speed requirement
            meets_stall_speed = self.clean_stall_speed <= 61.0
            
            # Certification date requirement for new aircraft
            mosaic_cert_date = date(2026, 7, 24)
            if self.certification_date and self.certification_date >= mosaic_cert_date:
                # New aircraft certified after July 24, 2026 - must meet MOSAIC LSA standards
                self.is_mosaic_compliant = meets_stall_speed
            elif self.certification_date and self.certification_date < mosaic_cert_date:
                # Existing aircraft - eligible if meets performance requirements
                self.is_mosaic_compliant = meets_stall_speed
            else:
                # No certification date provided - assume meets requirements if stall speed OK
                self.is_mosaic_compliant = meets_stall_speed

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.manufacturer.name} {self.model}"


class AircraftCorrection(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('IMPLEMENTED', 'Implemented'),
    ]
    
    FIELD_CHOICES = [
        ('clean_stall_speed', 'Clean stall speed'),
        ('top_speed', 'Top speed'),
        ('maneuvering_speed', 'Maneuvering speed'),
        ('cruise_speed', 'Cruise speed'),
        ('vx_speed', 'Best angle of climb speed (Vx)'),
        ('vy_speed', 'Best rate of climb speed (Vy)'),
        ('vs0_speed', 'Stall speed landing configuration (Vs0)'),
        ('vg_speed', 'Best glide speed (Vg)'),
        ('vfe_speed', 'Maximum flap extended speed (Vfe)'),
        ('vno_speed', 'Maximum structural cruising speed (Vno)'),
        ('vne_speed', 'Never exceed speed (Vne)'),
        ('max_takeoff_weight', 'Maximum takeoff weight'),
        ('seating_capacity', 'Seating capacity'),
        ('retractable_gear', 'Retractable gear'),
        ('variable_pitch_prop', 'Variable pitch propeller'),
        ('certification_date', 'Certification date'),
        ('verification_source', 'Verification source'),
        ('engines', 'Engine configurations'),
        ('general', 'General information'),
    ]
    
    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.CASCADE,
        related_name='correction_suggestions'
    )
    field_name = models.CharField(
        max_length=30,
        choices=FIELD_CHOICES,
        help_text="The field that needs correction"
    )
    current_value = models.TextField(
        blank=True,
        help_text="Current value in the database"
    )
    suggested_value = models.TextField(
        help_text="Suggested new value"
    )
    reason = models.TextField(
        help_text="Explanation for the suggested change"
    )
    source_documentation = models.TextField(
        blank=True,
        help_text="Reference documentation supporting the change (POH page, TC document, etc.)"
    )
    submitter_email = models.EmailField(
        blank=True,
        help_text="Email address of person submitting correction (optional)"
    )
    submitter_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Name of person submitting correction (optional)"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes for review process"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the correction was reviewed"
    )
    
    class Meta:
        db_table = 'aircraft_corrections'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Correction for {self.aircraft} - {self.get_field_name_display()} ({self.status})"
