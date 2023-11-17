def sqrt(a): #sqrt of positive integer
    eps = 0.001 #accuracy of approximation
    first = 1
    last = a

    res = 1

    while last - first > eps:
        res = (first + last) / 2

        if res**2 <= a:
            first = res + eps
        else:
            last = res

    return res
