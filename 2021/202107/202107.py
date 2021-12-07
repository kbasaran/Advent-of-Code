# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
import matplotlib.pyplot as plt

start_time = perf_counter()


def parse_input(p_in):
    return [int(val) for val in p_in.split(",")]


def alignment_cost_part1(positions, target):
    return sum([abs(pos - target) for pos in positions])


def alignment_cost_part2(positions, target):
    return sum([sum(range(abs(pos - target) + 1)) for pos in positions])


def find_minimum_cost(positions, points_to_check, cost_function):
    fuel_costs = {}
    for target in points_to_check:
        cost = cost_function(positions, target)
        fuel_costs[target] = cost
    minimum_cost = min(fuel_costs.values())
    plt.plot(fuel_costs.keys(), fuel_costs.values())
    plt.grid()
    plt.show()
    print(f"\nLowest fuel needed: {minimum_cost}")


positions = parse_input(p_in)
find_minimum_cost(positions, range(-1000, 1000), alignment_cost_part1)
find_minimum_cost(positions, range(300, 600), alignment_cost_part2)

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
