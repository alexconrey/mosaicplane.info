from rest_framework import serializers
from .models import FeatureFlag


class FeatureFlagSerializer(serializers.ModelSerializer):
    """
    Serializer for feature flags - only exposes public information
    """
    display_name = serializers.CharField(source='get_feature_key_display', read_only=True)

    class Meta:
        model = FeatureFlag
        fields = ['feature_key', 'display_name', 'enabled', 'description']
        read_only_fields = ['feature_key', 'display_name', 'enabled', 'description']


class FeatureFlagListSerializer(serializers.Serializer):
    """
    Simplified serializer that returns just a dictionary of feature_key -> enabled
    for easier frontend consumption
    """
    def to_representation(self, instance):
        # Return a simple dictionary of feature flags
        flags = {}
        for flag in instance:
            flags[flag.feature_key] = flag.enabled
        return flags