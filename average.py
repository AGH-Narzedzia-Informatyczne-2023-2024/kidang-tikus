ilosc_liczb = int(input("Podaj ilość liczb: "))

# Inicjalizacja pustej tablicy na liczby
liczby = []

# Pętla for do wczytywania liczb
for i in range(ilosc_liczb):
    liczba = float(input(f"Podaj liczbę {i + 1}: "))
    liczby.append(liczba)

# Obliczanie średniej
if ilosc_liczb > 0:
    srednia = round(sum(liczby) / ilosc_liczb, 3)
    print(f"Średnia z podanych liczb wynosi: {srednia}")
else:
    print("Nie podano żadnych liczb, nie można obliczyć średniej.")
