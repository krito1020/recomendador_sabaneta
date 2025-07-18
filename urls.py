# Rutas principales
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.recomendador.urls')),  # Ruta principal del recomendador
    path('admin/', admin.site.urls),              # Panel de administración (opcional)
]