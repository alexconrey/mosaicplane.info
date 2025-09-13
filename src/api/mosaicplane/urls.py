"""
URL configuration for mosaicplane project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aircraft.urls')),
    # OpenAPI 3 schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc UI
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve static files and Vue.js SPA
static_dir = os.path.join(settings.BASE_DIR.parent, 'static')

urlpatterns += [
    # Serve static files (CSS, JS, images)
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': os.path.join(static_dir, 'assets')}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    # Serve Vue.js SPA for all other routes (client-side routing)
    re_path(r'^.*$', serve, {'document_root': static_dir, 'path': 'index.html'}),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
