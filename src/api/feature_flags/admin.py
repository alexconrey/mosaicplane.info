from django.contrib import admin
from django.utils.html import format_html
from .models import FeatureFlag, FeatureFlagHistory


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = [
        'feature_key',
        'get_display_name',
        'enabled_status',
        'last_modified_by',
        'updated_at'
    ]
    list_filter = ['enabled', 'created_at', 'updated_at']
    search_fields = ['feature_key', 'description']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Feature Configuration', {
            'fields': ['feature_key', 'enabled', 'description']
        }),
        ('Metadata', {
            'fields': ['last_modified_by', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    def get_display_name(self, obj):
        """Get human-readable name for the feature"""
        return obj.get_feature_key_display()
    get_display_name.short_description = 'Feature Name'

    def enabled_status(self, obj):
        """Show enabled status with color coding"""
        if obj.enabled:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✓ Enabled</span>'
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">✗ Disabled</span>'
            )
    enabled_status.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        """Track who modified the feature flag"""
        if change:
            # Get previous state for history tracking
            try:
                old_obj = FeatureFlag.objects.get(pk=obj.pk)
                if old_obj.enabled != obj.enabled:
                    # Create history record
                    FeatureFlagHistory.objects.create(
                        feature_flag=obj,
                        previous_state=old_obj.enabled,
                        new_state=obj.enabled,
                        changed_by=request.user.username,
                        reason=f"Changed via Django Admin by {request.user.username}"
                    )
            except FeatureFlag.DoesNotExist:
                pass

        obj.last_modified_by = request.user.username
        super().save_model(request, obj, form, change)

    actions = ['enable_features', 'disable_features']

    def enable_features(self, request, queryset):
        """Bulk enable selected features"""
        count = 0
        for obj in queryset:
            if not obj.enabled:
                # Create history record
                FeatureFlagHistory.objects.create(
                    feature_flag=obj,
                    previous_state=obj.enabled,
                    new_state=True,
                    changed_by=request.user.username,
                    reason=f"Bulk enabled via Django Admin by {request.user.username}"
                )
                obj.enabled = True
                obj.last_modified_by = request.user.username
                obj.save()
                count += 1

        self.message_user(request, f"Enabled {count} feature flag(s).")
    enable_features.short_description = "Enable selected feature flags"

    def disable_features(self, request, queryset):
        """Bulk disable selected features"""
        count = 0
        for obj in queryset:
            if obj.enabled:
                # Create history record
                FeatureFlagHistory.objects.create(
                    feature_flag=obj,
                    previous_state=obj.enabled,
                    new_state=False,
                    changed_by=request.user.username,
                    reason=f"Bulk disabled via Django Admin by {request.user.username}"
                )
                obj.enabled = False
                obj.last_modified_by = request.user.username
                obj.save()
                count += 1

        self.message_user(request, f"Disabled {count} feature flag(s).")
    disable_features.short_description = "Disable selected feature flags"


@admin.register(FeatureFlagHistory)
class FeatureFlagHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'feature_flag',
        'state_change',
        'changed_by',
        'changed_at',
        'reason'
    ]
    list_filter = ['changed_at', 'previous_state', 'new_state', 'changed_by']
    search_fields = ['feature_flag__feature_key', 'changed_by', 'reason']
    readonly_fields = ['feature_flag', 'previous_state', 'new_state', 'changed_by', 'changed_at', 'reason']

    def has_add_permission(self, request):
        """Prevent manual creation of history records"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of history records"""
        return False

    def state_change(self, obj):
        """Show state change with icons"""
        if obj.previous_state and not obj.new_state:
            return format_html(
                '<span style="color: #dc3545;">✓ → ✗ (Disabled)</span>'
            )
        elif not obj.previous_state and obj.new_state:
            return format_html(
                '<span style="color: #28a745;">✗ → ✓ (Enabled)</span>'
            )
        else:
            return f"{obj.previous_state} → {obj.new_state}"
    state_change.short_description = 'State Change'
