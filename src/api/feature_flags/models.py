from django.db import models
from django.core.exceptions import ValidationError


class FeatureFlag(models.Model):
    """
    Feature flags to control UI features without code deployments.
    Allows enabling/disabling features via Django admin.
    """

    FEATURE_CHOICES = [
        ('ads_enabled', 'Google AdSense Ads'),
        ('amp_ads_enabled', 'AMP Ads'),
        ('analytics_enabled', 'Google Analytics'),
        ('beta_features', 'Beta Features'),
        ('maintenance_mode', 'Maintenance Mode'),
    ]

    feature_key = models.CharField(
        max_length=50,
        unique=True,
        choices=FEATURE_CHOICES,
        help_text="Unique identifier for the feature"
    )

    enabled = models.BooleanField(
        default=False,
        help_text="Whether this feature is currently enabled"
    )

    description = models.TextField(
        blank=True,
        help_text="Description of what this feature flag controls"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metadata for tracking changes
    last_modified_by = models.CharField(
        max_length=100,
        blank=True,
        help_text="User who last modified this flag"
    )

    class Meta:
        db_table = 'feature_flags'
        ordering = ['feature_key']
        verbose_name = 'Feature Flag'
        verbose_name_plural = 'Feature Flags'

    def __str__(self):
        status = "enabled" if self.enabled else "disabled"
        return f"{self.get_feature_key_display()} ({status})"

    def clean(self):
        """Validate feature flag data"""
        super().clean()

        # Ensure feature_key is in allowed choices
        valid_keys = [choice[0] for choice in self.FEATURE_CHOICES]
        if self.feature_key not in valid_keys:
            raise ValidationError(f"Invalid feature key: {self.feature_key}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class FeatureFlagHistory(models.Model):
    """
    Track changes to feature flags for audit purposes
    """
    feature_flag = models.ForeignKey(
        FeatureFlag,
        on_delete=models.CASCADE,
        related_name='history'
    )

    previous_state = models.BooleanField()
    new_state = models.BooleanField()
    changed_by = models.CharField(max_length=100, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, help_text="Reason for the change")

    class Meta:
        db_table = 'feature_flag_history'
        ordering = ['-changed_at']
        verbose_name = 'Feature Flag History'
        verbose_name_plural = 'Feature Flag History'

    def __str__(self):
        return f"{self.feature_flag.feature_key}: {self.previous_state} → {self.new_state}"
