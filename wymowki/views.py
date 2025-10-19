from django.shortcuts import render, redirect
from .models import Wymowka
from .forms import WymowkaForm

def strona_glowna(request):
    # Losujemy jedną wymówkę. order_by('?') losuje.
    losowa_wymowka = Wymowka.objects.order_by('?').first()

    context = {
        'wymowka': losowa_wymowka
    }
    return render(request, 'wymowki/strona_glowna.html', context)

def dodaj_wymowke(request):
    # Sprawdzamy, czy formularz został wysłany (metoda POST)
    if request.method == 'POST':
        # Tworzymy instancję formularza z danymi od użytkownika
        form = WymowkaForm(request.POST)
        if form.is_valid():
            # Jeśli dane są poprawne, zapisujemy wymówkę w bazie
            form.save()
            # Przekierowujemy użytkownika z powrotem na stronę główną
            return redirect('strona_glowna')
    else:
        # Jeśli to zwykłe wejście (metoda GET), tworzymy pusty formularz
        form = WymowkaForm()

    # Renderujemy szablon, przekazując do niego formularz
    context = {
        'form': form
    }
    return render(request, 'wymowki/dodaj_wymowke.html', context)