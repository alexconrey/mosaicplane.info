from django.urls import path
from . import views

app_name = 'feature_flags'

urlpatterns = [
    # Simple key-value format for frontend consumption
    path('', views.feature_flags_list, name='feature_flags_list'),

    # Detailed format with descriptions
    path('detailed/', views.feature_flags_detailed, name='feature_flags_detailed'),

    # Individual feature flag
    path('<str:feature_key>/', views.feature_flag_detail, name='feature_flag_detail'),
]