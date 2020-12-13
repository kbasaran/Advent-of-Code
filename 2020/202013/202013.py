import numpy as np

input_l1 = 1000052
input_l2 = "23,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,863,x,x,x,x,x,x,x,x,x,x,x,19,13,x,x,x,17,x,x,x,x,x,x,x,x,x,x,x,29,x,571,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,41".split(",")
# input_l1 = 939
# input_l2 = "7,13,x,x,59,x,31,19".split(",")

bus_ids = [int(s) for s in input_l2 if s.isdigit()]

# Part 1

def calc_divisors(n) :
    divisors = set()
    # Note that this loop runs till square root 
    i = 1
    while i <= np.sqrt(n): 
        if (n % i == 0):
            divisors.update([i, int(n/i)])
        i = i + 1
    return sorted(divisors)


def calc_divisors_fast(n):
    # Note that this loop runs till square root
    val_range = np.arange(1, np.ceil(np.sqrt(n)) + 1)
    remains = np.floor_divide(n, val_range)
    divisors = val_range[val_range * remains == n].astype(np.int32)
    answers = set(divisors)
    answers.update((n / divisors).astype(np.int32))
    return answers


val = input_l1 + 1
while 1:
    divisors = calc_divisors_fast(val)
    for bus_id in bus_ids:
        if bus_id in divisors:
            print(f"Answer: {bus_id * (val - input_l1)}")
            val = 0
            break
    if val > 0:
        val += 1
    else:
        break


# %% Part 2

busses = []
for i, val in enumerate(input_l2):
    if val.isdigit():
        busses.append((int(val), i))
busses = np.array(busses).astype(np.int64)  # first column is bus id, second column is its minute offset

timestamp = 0
dividors_of_step = set([busses[0, 0]])

while 1:
    remainders = np.mod((timestamp + busses[:, 1]), busses[:, 0])
    if np.all(remainders == 0):
        print(f"Answer: {timestamp}")
        break
    else:
        dividors_of_step.update(busses[:, 0][remainders == 0])
        step = np.product(list(dividors_of_step))
        timestamp += step
