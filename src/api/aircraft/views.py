from typing import Any
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Manufacturer, Aircraft
from .serializers import ManufacturerSerializer, AircraftSerializer, AircraftDetailSerializer


class ReadOnlyOrAuthenticatedPermission(permissions.BasePermission):
    """
    Custom permission to allow read-only access to unauthenticated users,
    but require authentication for write operations.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions require authentication
        return request.user and request.user.is_authenticated


@extend_schema_view(
    list=extend_schema(
        summary="List all manufacturers",
        description="Get a paginated list of all aircraft manufacturers with filtering and search capabilities."
    ),
    create=extend_schema(
        summary="Create a manufacturer",
        description="Create a new aircraft manufacturer."
    ),
    retrieve=extend_schema(
        summary="Get manufacturer details",
        description="Get detailed information about a specific manufacturer."
    ),
    update=extend_schema(
        summary="Update manufacturer",
        description="Update all fields of a manufacturer."
    ),
    partial_update=extend_schema(
        summary="Partially update manufacturer",
        description="Update specific fields of a manufacturer."
    ),
    destroy=extend_schema(
        summary="Delete manufacturer",
        description="Delete a manufacturer and all associated aircraft."
    )
)
class ManufacturerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing aircraft manufacturers.

    Provides CRUD operations for manufacturers with filtering by manufacturing status
    and search by name. Write operations require authentication.
    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [ReadOnlyOrAuthenticatedPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_currently_manufacturing']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @extend_schema(
        summary="Get aircraft by manufacturer",
        description="Get all aircraft manufactured by this manufacturer.",
        responses=AircraftSerializer(many=True)
    )
    @action(detail=True, methods=['get'])
    def aircraft(self, request, pk=None):
        manufacturer = self.get_object()
        aircraft = manufacturer.aircraft.all()
        serializer = AircraftSerializer(aircraft, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="List all aircraft",
        description="Get a paginated list of all MOSAIC-compliant aircraft with comprehensive filtering and search capabilities."
    ),
    create=extend_schema(
        summary="Create an aircraft",
        description="Add a new aircraft to the database."
    ),
    retrieve=extend_schema(
        summary="Get aircraft details",
        description="Get detailed information about a specific aircraft including manufacturer details."
    ),
    update=extend_schema(
        summary="Update aircraft",
        description="Update all fields of an aircraft."
    ),
    partial_update=extend_schema(
        summary="Partially update aircraft",
        description="Update specific fields of an aircraft."
    ),
    destroy=extend_schema(
        summary="Delete aircraft",
        description="Remove an aircraft from the database."
    )
)
class AircraftViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing aircraft specifications.

    Provides CRUD operations for aircraft with filtering by manufacturer, MOSAIC compliance,
    and manufacturing status. Supports search by aircraft model and manufacturer name.
    Also includes speed-based ordering for performance comparisons.
    Write operations require authentication.
    """
    queryset = Aircraft.objects.select_related('manufacturer').all()
    serializer_class = AircraftSerializer
    permission_classes = [ReadOnlyOrAuthenticatedPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'manufacturer', 
        'is_mosaic_compliant',
        'sport_pilot_eligible',
        'seating_capacity',
        'retractable_gear',
        'variable_pitch_prop',
        'certification_date',
        'manufacturer__is_currently_manufacturing'
    ]
    search_fields = ['model', 'manufacturer__name']
    ordering_fields = [
        'model', 
        'clean_stall_speed', 
        'top_speed', 
        'maneuvering_speed',
        'max_takeoff_weight',
        'seating_capacity',
        'certification_date',
        'manufacturer__name'
    ]
    ordering = ['manufacturer__name', 'model']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AircraftDetailSerializer
        return AircraftSerializer

    @extend_schema(
        summary="Compare multiple aircraft",
        description="Compare specifications of multiple aircraft side by side.",
        parameters=[
            OpenApiParameter(
                name='ids',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Comma-separated list of aircraft IDs to compare',
                examples=[
                    OpenApiExample(
                        'Compare two aircraft',
                        value='1,2',
                        description='Compare aircraft with IDs 1 and 2'
                    ),
                    OpenApiExample(
                        'Compare multiple aircraft',
                        value='1,3,5,7',
                        description='Compare aircraft with IDs 1, 3, 5, and 7'
                    ),
                ]
            ),
        ],
        responses=AircraftDetailSerializer(many=True)
    )
    @action(detail=False, methods=['get'])
    def compare(self, request):
        aircraft_ids = request.query_params.get('ids', '').split(',')
        if not aircraft_ids or aircraft_ids == ['']:
            return Response({'error': 'Please provide aircraft IDs to compare'}, status=400)
        
        try:
            aircraft_ids = [int(id.strip()) for id in aircraft_ids]
            aircraft = Aircraft.objects.select_related('manufacturer').filter(id__in=aircraft_ids)
            serializer = AircraftDetailSerializer(aircraft, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'Invalid aircraft ID format'}, status=400)
