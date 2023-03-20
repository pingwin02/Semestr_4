from itertools import compress
import random
import time
import matplotlib.pyplot as plt

from data import *


def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]


def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))


def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness


items, knapsack_max_capacity = get_big()
print(items)

population_size = 100
generations = 200
n_selection = 20
n_elite = 1

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), population_size)
for _ in range(generations):
    population_history.append(population)

    # 2a. Obliczenie prawdopodobieństwa wyboru osobnika
    sum_fitness = 0
    for j in range(len(population)):
        sum_fitness += fitness(items, knapsack_max_capacity, population[j])

    probability = []
    for i in range(len(population)):
        probability.append(fitness(items, knapsack_max_capacity, population[i]) / sum_fitness)

    # 2b. Wybór rodziców
    parents = []
    for _ in range(n_selection):
        parents.append(random.choices(population, probability)[0])

    # 3. Tworzenie kolejnego pokolenia
    children = []
    for i in range(0, len(parents), 2):
        cross_point = random.randint(0, len(items))
        children.append(parents[i][:cross_point] + parents[i + 1][cross_point:])
        children.append(parents[i + 1][:cross_point] + parents[i][cross_point:])

    # 4. Mutacja
    for i in range(len(children)):
        random__ = random.randint(0, len(items) - 1)
        children[i][random__] = not children[i][random__]

    # 5. Wybór najlepszych
    population = children + [population_best(items, knapsack_max_capacity, population)[0] for _ in range(n_elite)]

    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)

end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
