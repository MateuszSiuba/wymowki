from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Wymowka, Kategoria
from .models import Komentarz

class WymowkaForm(forms.ModelForm):
    class Meta:
        model = Wymowka
        fields = ['tresc', 'kategoria', 'tags']
        labels = {
            'tresc': 'Wpisz treść swojej wymówki',
            'kategoria': 'Kategoria',
            'tags': 'Tagi (oddzielone przecinkami)'
        }
        widgets = {
            'tresc': forms.Textarea(attrs={'placeholder': 'Np. "Pies zjadł mi notatki..."', 'rows': 4}),
            'tags': forms.TextInput(attrs={'placeholder': 'np. autobus, korek, spóźnienie'}),
        }

class RejestracjaForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nazwa użytkownika',
            'password1': 'Hasło',
            'password2': 'Potwierdź hasło'
        }

class LogowanieForm(AuthenticationForm):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class KomentarzForm(forms.ModelForm):
    class Meta:
        model = Komentarz
        fields = ['tresc']
        labels = {
            'tresc': 'Twój komentarz (max 500 znaków)',
        }
        widgets = {
            'tresc': forms.Textarea(attrs={
                'placeholder': 'Wpisz swoje spostrzeżenia tutaj...', 
                'rows': 3, 
                'maxlength': 500
            }),
        }