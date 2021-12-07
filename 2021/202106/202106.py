# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter

start_time = perf_counter()


def parse_input(p_in):
    return [int(val) for val in p_in.split(",")]


def make_population_ledger(lifetimes):
    ledger = {i: 0 for i in range(-1, max(lifetimes) + 10)}
    for lifetime in lifetimes:
        ledger[lifetime] += 1
    return ledger


def calc_age(int_counter, day):
    return (8 - int_counter) + day


def calc_lifetime(int_counter, total_days):
    return calc_age(int_counter, total_days)


def all_children(lifetime):
    n_children, extra_days = divmod(lifetime - 2, 7)
    return [i * 7 + extra_days for i in range(n_children)]


def part_1(p_in, total_days):
    lifetimes = [calc_lifetime(int_counter, total_days) for int_counter in parse_input(p_in)]
    ledger = make_population_ledger(lifetimes)

    # if any fish in the ledger can still have children
    while any([value > 0 for value in [ledger[lifetime] for lifetime in range(9, total_days + 10)]]):
        for lifetime in range(9, total_days + 10):
            if ledger[lifetime] > 0:
                children_lifetimes = all_children(lifetime)
                for children_lifetime in children_lifetimes:
                    ledger[children_lifetime] += ledger[lifetime]
                # processed fish, can retire, no more children
                ledger[-1] += ledger[lifetime]
                ledger[lifetime] = 0

    print(f"Answer: {sum([val for val in ledger.values()])}")


part_1(p_in, 256)

print(f"\nSolved in {(perf_counter() - start_time) * 1000:.1f} ms.")
