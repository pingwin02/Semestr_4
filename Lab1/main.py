# wariacja z powtórzeniami n^m
def variations1(variation, n, depth=0):
    if len(variation) > n:
        raise ValueError("m > n")
    if depth == len(variation):
        print(*variation)
    else:
        for i in range(n):
            variation[depth] = i
            variations1(variation, n, depth + 1)


# wariacja bez powtórzeń n*(n-1)*...*(n-m+1)
# jeśli n = m to jest to permutacja n!
def variations2(variation, used, depth=0):
    if len(variation) > len(used):
        raise ValueError("m > n")
    if depth == len(variation):
        print(*variation)
    else:
        for i in range(len(used)):
            if not used[i]:
                used[i] = True
                variation[depth] = i
                variations2(variation, used, depth + 1)
                used[i] = False


# kombinacja dwumian Newtona C(n, m) = n!/(m!*(n-m)!)
def combinations(combination, n, start=0, depth=0):
    if len(combination) > n:
        raise ValueError("m > n")
    if depth == len(combination):
        print(*combination)
    else:
        for i in range(start, n):
            combination[depth] = i
            combinations(combination, n, i + 1, depth + 1)


if __name__ == "__main__":
    N = 3
    M = 2
    print("Wariacje z powtórzeniami:")
    variations1([0] * M, N)
    print("Wariacje bez powtórzeń:")
    variations2([0] * M, [False] * N)
    print("Kombinacje:")
    combinations([0] * M, N)
