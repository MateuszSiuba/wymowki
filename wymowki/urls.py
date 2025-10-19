from django.urls import path
from . import views

urlpatterns = [
    # Pusty string '' oznacza, że to jest główny adres tej aplikacji
    path('', views.strona_glowna, name='strona_glowna'),
    path('dodaj/', views.dodaj_wymowke, name='dodaj_wymowke'),
]