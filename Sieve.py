def sieve(n):
    if n < 2:
        return []
    sieve = [1 for i in range(0,n + 1)]
    sieve[0] = 0
    sieve[1] = 0
    for i in range(0,len(sieve)):
        if sieve[i]:
            for j in range(i * i, len(sieve), i):
                sieve[j] = 0
    #print(sieve)
    result = [x for x in range(len(sieve)) if sieve[x]]
    return result

if __name__ == "__main__":
    n = int(input("Podaj n: "))
    print(f"Liczby pierwsze do n: ")
    result = sieve(n)
    print(*result)