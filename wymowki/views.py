from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wymowka, Kategoria, Ocena, Komentarz
from .forms import WymowkaForm, RejestracjaForm, LogowanieForm, KomentarzForm
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.contrib.staticfiles import finders
import base64
from reportlab.pdfbase import pdfmetrics      
from reportlab.pdfbase.ttfonts import TTFont

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
    pass


def ranking(request):
    wymowka_id = request.GET.get('wymowka')
    
    if wymowka_id:
        wymowka = get_object_or_404(Wymowka, pk=wymowka_id)
        komentarze = Komentarz.objects.filter(wymowka=wymowka).select_related('autor')
        
        komentarz_form = KomentarzForm()
        
        if request.method == 'POST' and request.user.is_authenticated:
            komentarz_form = KomentarzForm(request.POST)
            if komentarz_form.is_valid():
                nowy_komentarz = komentarz_form.save(commit=False)
                nowy_komentarz.wymowka = wymowka
                nowy_komentarz.autor = request.user
                nowy_komentarz.save()
                messages.success(request, "Twój komentarz został dodany!")
                return redirect(reverse('ranking') + f'?wymowka={wymowka.id}')

        context = {
            'wymowka_szczegoly': wymowka,
            'komentarze': komentarze,
            'komentarz_form': komentarz_form,
        }
        return render(request, 'wymowki/ranking_szczegoly.html', context)

    kategoria_id = request.GET.get('kategoria')
    
    wymowki = Wymowka.objects.all()
    
    if kategoria_id:
        wymowki = wymowki.filter(kategoria_id=kategoria_id)
    
    wymowki = wymowki.order_by('-glosy')[:20]
        
    kategorie = Kategoria.objects.all()

    context = {
        'wymowki': wymowki,
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


def link_callback(uri, rel):

    sciezka_do_fontu = r"C:\Users\patry\wymowki\wymowki\static\wymowki\fonts\polski.ttf"

    if uri.endswith('.ttf'):
        if os.path.isfile(sciezka_do_fontu):
            return sciezka_do_fontu
        else:
            print(f"XHTML2PDF ERROR: Plik fizycznie nie istnieje w: {sciezka_do_fontu}")
            return None

    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        relative_path = uri.replace(settings.STATIC_URL, "")
        path = finders.find(relative_path)
        if not path and hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            path = os.path.join(settings.STATIC_ROOT, relative_path)
    else:
        path = uri

    return path

def export_pdf(request):
    wymowki = Wymowka.objects.all().order_by('-glosy')[:20]

    sciezka_font = r"C:\Users\patry\wymowki\wymowki\static\wymowki\fonts\DejaVuSans.ttf"
    
    try:
        pdfmetrics.registerFont(TTFont('PolskiFont', sciezka_font))
    except Exception as e:
        print(f"BŁĄD REJESTRACJI CZCIONKI: {e}")

    context = {
        'wymowki': wymowki,
    }

    html_string = render_to_string('wymowki/pdf_template.html', context)
    
    result = BytesIO()
    
    pdf = pisa.pisaDocument(
        BytesIO(html_string.encode("UTF-8")), 
        result,
        link_callback=link_callback 
    )
    
    if pdf.err:
        return HttpResponse(f"Wystąpił błąd przy generowaniu PDF: {pdf.err}", status=500)
    
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ranking_wymowek.pdf"'
    
    return response