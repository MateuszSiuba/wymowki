from django.contrib import admin
from .models import Wymowka, Kategoria, Ocena, Komentarz

class KategoriaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'opis')
    search_fields = ('nazwa',)

class WymowkaAdmin(admin.ModelAdmin):
    list_display = ('tresc', 'kategoria', 'autor', 'glosy', 'data_dodania')
    search_fields = ('tresc', 'autor__username')
    list_filter = ('data_dodania', 'kategoria')
    readonly_fields = ('data_dodania', 'glosy')

class OcenaAdmin(admin.ModelAdmin):
    list_display = ('wymowka', 'uzytkownik', 'wartosc', 'data')
    list_filter = ('wartosc', 'data')
    search_fields = ('wymowka__tresc', 'uzytkownik__username')
    readonly_fields = ('data',)

class KomentarzAdmin(admin.ModelAdmin):
    list_display = ('wymowka', 'autor', 'data_dodania', 'tresc')
    list_filter = ('data_dodania', 'autor')
    search_fields = ('tresc', 'autor__username', 'wymowka__tresc')
    readonly_fields = ('data_dodania',)

admin.site.register(Kategoria, KategoriaAdmin)
admin.site.register(Wymowka, WymowkaAdmin)
admin.site.register(Ocena, OcenaAdmin)
admin.site.register(Komentarz, KomentarzAdmin)
