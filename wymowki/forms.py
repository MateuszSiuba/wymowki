from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Wymowka, Kategoria

class WymowkaForm(forms.ModelForm):
    class Meta:
        model = Wymowka
        fields = ['tresc', 'kategoria']
        labels = {
            'tresc': 'Wpisz treść swojej wymówki',
            'kategoria': 'Kategoria'
        }
        widgets = {
            'tresc': forms.Textarea(attrs={'placeholder': 'Np. "Pies zjadł mi notatki..."', 'rows': 4}),
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
