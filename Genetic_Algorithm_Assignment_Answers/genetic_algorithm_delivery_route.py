import random

# Distance between each pair of locations (in kilometres)
distance = {
    "A": {"A": 0, "B": 4, "C": 8, "D": 6, "E": 7, "F": 9, "G": 5},
    "B": {"A": 4, "B": 0, "C": 5, "D": 7, "E": 3, "F": 8, "G": 6},
    "C": {"A": 8, "B": 5, "C": 0, "D": 4, "E": 6, "F": 3, "G": 7},
    "D": {"A": 6, "B": 7, "C": 4, "D": 0, "E": 5, "F": 6, "G": 8},
    "E": {"A": 7, "B": 3, "C": 6, "D": 5, "E": 0, "F": 4, "G": 6},
    "F": {"A": 9, "B": 8, "C": 3, "D": 6, "E": 4, "F": 0, "G": 5},
    "G": {"A": 5, "B": 6, "C": 7, "D": 8, "E": 6, "F": 5, "G": 0}
}

# A fixed seed makes the experiment repeatable.
random.seed(42)

locations = ["B", "C", "D", "E", "F", "G"]
POPULATION_SIZE = 80
GENERATIONS = 100
MUTATION_RATE = 0.15
ELITE_COUNT = 2


def calculate_distance(route):
    """Calculate the full route distance, including the depot at both ends."""
    full_route = ["A"] + route + ["A"]
    total = 0
    for i in range(len(full_route) - 1):
        total += distance[full_route[i]][full_route[i + 1]]
    return total


def create_population():
    """Create random routes; each delivery location appears exactly once."""
    population = []
    for _ in range(POPULATION_SIZE):
        route = locations[:]
        random.shuffle(route)
        population.append(route)
    return population


def select_parent(population):
    """Tournament selection: choose the shortest route from three candidates."""
    candidates = random.sample(population, 3)
    return min(candidates, key=calculate_distance)


def crossover(parent1, parent2):
    """Order crossover (OX), which keeps every location once in the child."""
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)

    # Copy a section from the first parent.
    child[start:end + 1] = parent1[start:end + 1]

    # Fill the remaining spaces in the order found in the second parent.
    remaining = [location for location in parent2 if location not in child]
    position = (end + 1) % len(child)

    for location in remaining:
        while child[position] is not None:
            position = (position + 1) % len(child)
        child[position] = location
        position = (position + 1) % len(child)

    return child


def mutate(route):
    """Swap two locations to create another valid route."""
    new_route = route[:]
    if random.random() < MUTATION_RATE:
        first, second = random.sample(range(len(new_route)), 2)
        new_route[first], new_route[second] = new_route[second], new_route[first]
    return new_route


def genetic_algorithm():
    population = create_population()

    for generation in range(GENERATIONS):
        population.sort(key=calculate_distance)

        # Keep the two best routes unchanged (elitism).
        next_population = [route[:] for route in population[:ELITE_COUNT]]

        while len(next_population) < POPULATION_SIZE:
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_population.append(child)

        population = next_population

    population.sort(key=calculate_distance)
    return population[0], calculate_distance(population[0])


if __name__ == "__main__":
    best_route, best_distance = genetic_algorithm()
    full_route = ["A"] + best_route + ["A"]

    print("Genetic Algorithm - Delivery Route Optimisation")
    print("Random seed: 42")
    print("Population size:", POPULATION_SIZE)
    print("Number of generations:", GENERATIONS)
    print("Best route:", " -> ".join(full_route))
    print("Total distance:", best_distance, "km")
