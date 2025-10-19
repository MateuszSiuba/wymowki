from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wymowka, Kategoria, Ocena
from .forms import WymowkaForm, RejestracjaForm, LogowanieForm

def strona_glowna(request):
    kategoria_id = request.GET.get('kategoria')
    szukaj = request.GET.get('szukaj', '')

    wymowki = Wymowka.objects.all()

    if kategoria_id:
        wymowki = wymowki.filter(kategoria_id=kategoria_id)

    if szukaj:
        wymowki = wymowki.filter(tresc__icontains=szukaj)

    losowa_wymowka = wymowki.order_by('?').first()
    kategorie = Kategoria.objects.all()

    context = {
        'wymowka': losowa_wymowka,
        'kategorie': kategorie,
        'wybrana_kategoria': kategoria_id,
        'szukaj': szukaj,
    }
    return render(request, 'wymowki/strona_glowna.html', context)

@login_required
def dodaj_wymowke(request):
    if request.method == 'POST':
        form = WymowkaForm(request.POST)
        if form.is_valid():
            wymowka = form.save(commit=False)
            wymowka.autor = request.user
            wymowka.save()
            messages.success(request, 'Wymówka została dodana!')
            return redirect('strona_glowna')
    else:
        form = WymowkaForm()

    context = {
        'form': form
    }
    return render(request, 'wymowki/dodaj_wymowke.html', context)

def ranking(request):
    kategoria_id = request.GET.get('kategoria')

    wymowki = Wymowka.objects.all()

    if kategoria_id:
        wymowki = wymowki.filter(kategoria_id=kategoria_id)

    top_wymowki = wymowki.order_by('-glosy')[:20]
    kategorie = Kategoria.objects.all()

    context = {
        'wymowki': top_wymowki,
        'kategorie': kategorie,
        'wybrana_kategoria': kategoria_id,
    }
    return render(request, 'wymowki/ranking.html', context)

@login_required
def ocen_wymowke(request, wymowka_id, wartosc):
    wymowka = get_object_or_404(Wymowka, id=wymowka_id)

    wartosc = int(wartosc)

    ocena, created = Ocena.objects.get_or_create(
        wymowka=wymowka,
        uzytkownik=request.user,
        defaults={'wartosc': wartosc}
    )

    if not created:
        if ocena.wartosc != wartosc:
            wymowka.glosy -= ocena.wartosc
            ocena.wartosc = wartosc
            ocena.save()
            wymowka.glosy += wartosc
            wymowka.save()
            messages.success(request, 'Zmieniono ocenę!')
        else:
            messages.info(request, 'Już oceniłeś tę wymówkę!')
    else:
        wymowka.glosy += wartosc
        wymowka.save()
        messages.success(request, 'Dziękujemy za ocenę!')

    return redirect(request.META.get('HTTP_REFERER', 'strona_glowna'))

def rejestracja(request):
    if request.user.is_authenticated:
        return redirect('strona_glowna')

    if request.method == 'POST':
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Witaj {user.username}! Twoje konto zostało utworzone.')
            return redirect('strona_glowna')
    else:
        form = RejestracjaForm()

    return render(request, 'wymowki/rejestracja.html', {'form': form})

def logowanie(request):
    if request.user.is_authenticated:
        return redirect('strona_glowna')

    if request.method == 'POST':
        form = LogowanieForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Witaj z powrotem, {username}!')
                return redirect('strona_glowna')
    else:
        form = LogowanieForm()

    return render(request, 'wymowki/logowanie.html', {'form': form})

def wylogowanie(request):
    logout(request)
    messages.info(request, 'Zostałeś wylogowany.')
    return redirect('strona_glowna')
