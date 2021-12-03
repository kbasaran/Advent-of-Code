# %% Take input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()


# %% Part 1
def binary_list_to_int(binary_list: list) -> int:
    return int("".join([str(int(val)) for val in binary_list]), 2)


rows = [[int(letter) for letter in row] for row in p_in.splitlines()]
gamma_rate = binary_list_to_int([sum([row[pos] for row in rows]) > len(rows) / 2
                                 for pos in range(len(rows[0]))
                                 ]
                                )
epsilon_rate = 2**len(rows[0]) - 1 - gamma_rate

print("\n--Part 1--")
print(f"Gamma/Epsilon: {gamma_rate}/{epsilon_rate}" + f"\nProduct: {gamma_rate * epsilon_rate}")


# %% Part 2
import numpy as np
oxy_ratings = co2_ratings = np.array(rows)
for col in range(oxy_ratings.shape[1]):
    most_common_oxy = np.average(oxy_ratings[:, col]) >= 0.5
    if oxy_ratings.shape[0] > 1:
        oxy_ratings = oxy_ratings[oxy_ratings[:, col] == most_common_oxy]

    most_common_co2 = np.average(co2_ratings[:, col]) >= 0.5
    if co2_ratings.shape[0] > 1:
        co2_ratings = co2_ratings[co2_ratings[:, col] != most_common_co2]

oxy_rating = binary_list_to_int(oxy_ratings[0])
co2_rating = binary_list_to_int(co2_ratings[0])

print("\n--Part 2--")
print(f"Oxygen/CO2: {oxy_rating}/{co2_rating}" + f"\nLife support rating: {oxy_rating * co2_rating}")
