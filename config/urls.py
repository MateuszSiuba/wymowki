from django.contrib import admin
from django.urls import path, include  # Dodaj 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Podłączamy wszystkie adresy z 'wymowki.urls' pod główny adres strony
    path('', include('wymowki.urls')), 
]