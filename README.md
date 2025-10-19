# Generator Wymówek Studenckich 🎓

## Nowe Funkcje

### 1. **System Rejestracji i Logowania**
- Użytkownicy mogą tworzyć konta i logować się do systemu
- Tylko zalogowani użytkownicy mogą dodawać wymówki i je oceniać
- Niezalogowani mogą przeglądać i wyszukiwać wymówki

### 2. **Kategorie Wymówek**
- Wymówki są organizowane w kategorie (Spóźnienie, Brak pracy domowej, Nieobecność, itp.)
- Filtrowanie wymówek po kategorii na stronie głównej i w rankingu
- 8 predefiniowanych kategorii

### 3. **System Oceniania**
- Zalogowani użytkownicy mogą oceniać wymówki: 👍 (lubię) lub 👎 (nie lubię)
- Każdy użytkownik może ocenić wymówkę tylko raz
- Można zmienić swoją ocenę

### 4. **Ranking Najlepszych Wymówek**
- Top 20 wymówek z najwyższymi ocenami
- Filtrowanie rankingu po kategorii
- Podświetlenie TOP 3 wymówek

### 5. **Wyszukiwarka**
- Możliwość wyszukiwania wymówek po treści
- Filtrowanie po kategorii jednocześnie z wyszukiwaniem

## Jak Zacząć

### Pierwsze Uruchomienie

1. **Utwórz superużytkownika** (do panelu admina):
```bash
python manage.py createsuperuser
```

2. **Uruchom serwer**:
```bash
python manage.py runserver
```

3. **Otwórz przeglądarkę**: http://127.0.0.1:8000

### Struktura URL

- `/` - Strona główna (generator losowych wymówek)
- `/dodaj/` - Dodawanie nowej wymówki (wymaga logowania)
- `/ranking/` - Ranking najlepszych wymówek
- `/rejestracja/` - Rejestracja nowego użytkownika
- `/logowanie/` - Logowanie
- `/wylogowanie/` - Wylogowanie
- `/admin/` - Panel administracyjny Django

### Funkcjonalności dla Niezalogowanych

- ✅ Przeglądanie losowych wymówek
- ✅ Wyszukiwanie wymówek
- ✅ Filtrowanie po kategorii
- ✅ Przeglądanie rankingu
- ❌ Dodawanie wymówek
- ❌ Ocenianie wymówek

### Funkcjonalności dla Zalogowanych

- ✅ Wszystkie powyższe
- ✅ Dodawanie własnych wymówek
- ✅ Ocenianie wymówek (👍 👎)
- ✅ Zmiana oceny

## Panel Administracyjny

W panelu admina można:
- Zarządzać użytkownikami
- Dodawać/edytować/usuwać kategorie
- Zarządzać wymówkami
- Przeglądać wszystkie oceny

## Baza Danych

### Modele:

1. **Kategoria**
   - nazwa
   - opis

2. **Wymowka**
   - treść
   - kategoria (opcjonalna)
   - autor (opcjonalny dla starych wymówek)
   - głosy (suma ocen)
   - data_dodania

3. **Ocena**
   - wymówka
   - użytkownik
   - wartość (+1 lub -1)
   - data

## Kategorie Domyślne

1. Spóźnienie
2. Brak pracy domowej
3. Nieobecność
4. Egzamin
5. Projekt
6. Techniczne
7. Rodzinne
8. Zdrowotne

## Wskazówki

- Aby dodać więcej kategorii, użyj panelu admina lub skryptu `dodaj_kategorie.py`
- Stare wymówki bez autora są oznaczone jako "Anonim"
- Ranking pokazuje TOP 20 wymówek
- Głosy są obliczane jako suma wszystkich ocen (+1 za lubię, -1 za nie lubię)

## Bezpieczeństwo

- Hasła użytkowników są szyfrowane
- CSRF protection jest włączona
- Tylko zalogowani użytkownicy mogą modyfikować dane
- Każdy użytkownik może ocenić wymówkę tylko raz

## Dalszy Rozwój

Możliwe rozszerzenia:
- Komentarze do wymówek
- System tagów
- Profil użytkownika z historią wymówek
- API REST
- Eksport wymówek do PDF
- Statystyki i wykresy

