from django.contrib import admin
from .models import Wymowka

# Tworzymy klasę konfiguracyjną dla panelu admina
class WymowkaAdmin(admin.ModelAdmin):
    # Pola, które mają być wyświetlane na liście wymówek
    list_display = ('tresc', 'glosy', 'data_dodania')
    
    # Dodaje pole wyszukiwania (będzie szukać w polu 'tresc')
    search_fields = ('tresc',)
    
    # Dodaje panel filtrów po prawej stronie (będzie filtrować po dacie)
    list_filter = ('data_dodania',)
    
    # Pola, które mają być tylko do odczytu podczas edycji
    readonly_fields = ('data_dodania',)

# Rejestrujemy model Wymowka, ale używając naszej nowej klasy konfiguracyjnej
admin.site.register(Wymowka, WymowkaAdmin)