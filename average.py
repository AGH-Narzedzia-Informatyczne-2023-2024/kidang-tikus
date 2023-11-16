def oblicz_srednia(ilosc_liczb):
    # Inicjalizacja pustej tablicy na liczby
    liczby = []

    # Pętla for do wczytywania liczb
    for i in range(ilosc_liczb):
    liczba = float(input(f"Podaj liczbę {i + 1}: "))
    liczby.append(liczba)

    # Obliczanie średniej
    if ilosc_liczb > 0:
        srednia = round(sum(liczby) / ilosc_liczb, 3)
        return srednia
    else:
        print("Nie podano żadnych liczb, nie można obliczyć średniej.")
        return None
    
# Pobranie ilości liczb od użytkownika
ilosc_liczb = int(input("Podaj ilość liczb: "))

# Wywołanie funkcji i wyświetlenie wyniku
wynik = oblicz_srednia(ilosc_liczb)
if wynik is not None:
    print(f"Średnia z podanych liczb wynosi: {wynik}")
