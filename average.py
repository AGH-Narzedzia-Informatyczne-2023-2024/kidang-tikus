def oblicz_srednia(ilosc_liczb):
    # Inicjalizacja pustej tablicy na liczby
    elementy = []                #zmiana nazwy tablicy

    # Pętla for do wczytywania liczb
    for i in range(ilosc_liczb):
        liczba = float(input(f"Podaj liczbę {i + 1}: "))
        elementy.append(liczba)

    # Obliczanie średniej
    if ilosc_liczb > 0:
        srednia = round(sum(elementy) / ilosc_liczb, 3)
        return srednia
    else:
        print("Nie podano żadnych liczb, nie można obliczyć średniej.")
        return None
    
# Pobranie ilości liczb od użytkownika
ilosc_liczb = int(input("Podaj ilość liczb: "))

# Wywołanie funkcji i wyświetlenie wyniku
wynik1 = oblicz_srednia(ilosc_liczb) 
if wynik1 is not None:
    print(f"Średnia z podanych liczb wynosi: {wynik1}") #komentarz
