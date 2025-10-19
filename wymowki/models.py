from django.db import models
from django.contrib.auth.models import User

class Kategoria(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)
    opis = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.nazwa

class Wymowka(models.Model):
    tresc = models.TextField()
    kategoria = models.ForeignKey(Kategoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='wymowki')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wymowki', null=True, blank=True)
    glosy = models.IntegerField(default=0)
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tresc[:50] + "..."

    class Meta:
        ordering = ['-data_dodania']
        verbose_name_plural = "Wymówki"

class Ocena(models.Model):
    wymowka = models.ForeignKey(Wymowka, on_delete=models.CASCADE, related_name='oceny')
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    wartosc = models.IntegerField(choices=[(1, '👍'), (-1, '👎')])
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wymowka', 'uzytkownik')
        verbose_name_plural = "Oceny"

    def __str__(self):
        return f"{self.uzytkownik.username} - {self.wymowka.tresc[:30]}"
