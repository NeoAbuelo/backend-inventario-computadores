from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('seguridad.urls')),
    path('api/v1/', include('inventario.urls')),
    path('api/v1/', include('salapcs.urls')),
    path('docs/', include('doc.urls')),
    path('api/v1/', include('dashboard.urls')),
]
