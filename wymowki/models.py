# wymowki/models.py
from django.db import models

class Wymowka(models.Model):
    tresc = models.TextField()
    glosy = models.IntegerField(default=0)
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tresc[:50] + "..."