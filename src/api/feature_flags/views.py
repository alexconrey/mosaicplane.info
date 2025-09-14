from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FeatureFlag
from .serializers import FeatureFlagSerializer, FeatureFlagListSerializer


@api_view(['GET'])
def feature_flags_list(request):
    """
    Get all feature flags in a simple key-value format
    Always returns fresh data from database
    """
    try:
        flags = FeatureFlag.objects.all()
        serializer = FeatureFlagListSerializer(flags)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Failed to fetch feature flags: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def feature_flags_detailed(request):
    """
    Get detailed feature flags information (includes descriptions)
    Always returns fresh data from database
    """
    try:
        flags = FeatureFlag.objects.all()
        serializer = FeatureFlagSerializer(flags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Failed to fetch feature flags: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def feature_flag_detail(request, feature_key):
    """
    Get a specific feature flag by key
    Always returns fresh data from database
    """
    try:
        flag = FeatureFlag.objects.get(feature_key=feature_key)
        serializer = FeatureFlagSerializer(flag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except FeatureFlag.DoesNotExist:
        return Response(
            {'error': f'Feature flag "{feature_key}" not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch feature flag: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
