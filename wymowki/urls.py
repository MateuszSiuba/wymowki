from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.strona_glowna, name='strona_glowna'),
    path('dodaj/', views.dodaj_wymowke, name='dodaj_wymowke'),
    path('ranking/', views.ranking, name='ranking'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    re_path(r'^ocen/(?P<wymowka_id>\d+)/(?P<wartosc>-?\d+)/$', views.ocen_wymowke, name='ocen_wymowke'),
    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('logowanie/', views.logowanie, name='logowanie'),
    path('wylogowanie/', views.wylogowanie, name='wylogowanie'),
]