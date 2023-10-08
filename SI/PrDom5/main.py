X = [ -3.5, 4.4, -2.2 ]
Y = [ 0.1, -2.5, 3.9 ]

def manhattan_distance(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))

def euclidean_distance(x, y):
    return round(sum((a - b) ** 2 for a, b in zip(x, y)) ** .5, 2)

def chebyshev_distance(x, y):
    return max(abs(a - b) for a, b in zip(x, y))

print("Manhattan distance: ", manhattan_distance(X, Y))
print("Euclidean distance: ", euclidean_distance(X, Y))
print("Chebyshev distance: ", chebyshev_distance(X, Y))