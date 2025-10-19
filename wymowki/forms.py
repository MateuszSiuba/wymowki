from django import forms
from .models import Wymowka

class WymowkaForm(forms.ModelForm):
    class Meta:
        model = Wymowka
        
        # Określamy, które pola z modelu mają być w formularzu
        # Chcemy tylko 'tresc'. 'glosy' i 'data_dodania' ustawią się automatycznie
        fields = ['tresc']
        
        # Opcjonalnie: Polskie etykiety dla pól
        labels = {
            'tresc': 'Wpisz treść swojej wymówki'
        }
        
        # Opcjonalnie: Dodanie atrybutów HTML, np. placeholder
        widgets = {
            'tresc': forms.Textarea(attrs={'placeholder': 'Np. "Pies zjadł mi notatki..."', 'rows': 4}),
        }