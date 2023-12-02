# 2022 Day 11

# Receive input
with open('input.txt') as f:
# with open("test.txt") as f:
    p_in = f.read()

from time import perf_counter
from dataclasses import dataclass
from functools import reduce

start_time = perf_counter()

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

@dataclass
class Monkey():
    number: int
    items: list
    worry_operation_text: str
    test_divider: int
    monkey_true: int
    monkey_false: int
    inspect_counter: int=0

    def __post_init__(self):

        # Described worry operation, used only in part 1
        operation = lambda old: eval(self.worry_operation_text)
        self.worry_operation = operation
        self.relief = lambda worry: worry // 3
 
        # Worry operation and division test for part 2
        val1, operator, val2 = self.worry_operation_text.split()

        def operate_plus(item):
            for key, val in item.items():
                _, item[key] = divmod(val + int(val2), key)
            return item, item[self.test_divider] == 0

        def operate_prod(item):
            for key, val in item.items():
                _, item[key] = divmod(val * int(val2), key)
            return item, item[self.test_divider] == 0

        def operate_power(item):
            for key, val in item.items():
                _, item[key] = divmod(val * val, key)
            return item, item[self.test_divider] == 0

        if operator == "+":
            self.worry_operation_part2 = operate_plus
        elif operator == "*" and val1 == "old" and val2 == "old":
            self.worry_operation_part2 = operate_power
        elif operator == "*" and val1 == "old":
            self.worry_operation_part2 = operate_prod
        else:
            raise ValueError(f"Unrecognized worry text: {self.worry_operation_text}")
           
    def receive_item(self, item):
        self.items = self.items + [item]

    def has_item(self):
        return len(self.items) > 0

    def modify_items_for_part2(self, test_divider_primes):
        items_remainders = []
        for item in self.items:
            # dicts. key in dict is prime divisor. value is remainder.
            item_as_remainder_dict = {divider: divmod(item, divider)[1] for divider in test_divider_primes}
            items_remainders.append(item_as_remainder_dict)
        self.items = items_remainders

    def inspect_part1(self):
        item = self.items.pop()
        new_item = self.worry_operation(item)
        new_item = self.relief(new_item)
        self.inspect_counter += 1
        # print(f"\nMonkey {self.number} end of inspection with operation {self.worry_operation_text}"
        #       f"\nItem {item} became {new_item}"
        #       )
        if new_item % self.test_divider == 0:
            # print(f"Send to monkey {self.monkey_true}")
            return self.monkey_true, new_item
        else:
            # print(f"Send to monkey {self.monkey_false}")
            return self.monkey_false, new_item

    def inspect_part2(self):
        item = self.items.pop()
        new_item, pass_test = self.worry_operation_part2(item)
        self.inspect_counter += 1

        if pass_test:
            return self.monkey_true, new_item
        else:
            return self.monkey_false, new_item


def initiate_monkeys(p_in, part2=False):
    monkeys = {}
    for monkey_text in p_in.split("\n\n"):
        lines = monkey_text.splitlines()
        number = int(lines[0].split()[1].replace(":", ""))
        items = [int(val) for val in lines[1].replace(",", "").split()[2:]][::-1]
        worry_operation_text = lines[2].split(" = ")[-1]
        test_divider = int(lines[3].split("by ")[-1])
        monkey_true = int(lines[4].split("monkey ")[-1])
        monkey_false = int(lines[5].split("monkey ")[-1])
        monkeys[number] = Monkey(number,
                                 items,
                                 worry_operation_text,
                                 test_divider,
                                 monkey_true,
                                 monkey_false,
                                 )
    if part2:
        test_divider_primes = set([monkey.test_divider for monkey in monkeys.values()])
        for monkey in monkeys.values():
            monkey.modify_items_for_part2(test_divider_primes)
    return monkeys

def calculate_monkey_business(monkeys):
    inspection_amounts = sorted([monkey.inspect_counter for monkey in monkeys.values()],
                                reverse=True,
                                )
    return inspection_amounts[0] * inspection_amounts[1] 


if __name__ == "__main__":
    monkeys = initiate_monkeys(p_in)
    for i_round in range(1, 21):
        for monkey in monkeys.values():
            while monkey.has_item():
                i_receiver, worry = monkey.inspect_part1()
                monkeys[i_receiver].receive_item(worry)

    print(calculate_monkey_business(monkeys))  # Part 1


    monkeys = initiate_monkeys(p_in, part2=True)
    for i_round in range(1, 10_001):
        for monkey in monkeys.values():
            while monkey.has_item():
                i_receiver, item = monkey.inspect_part2()
                monkeys[i_receiver].receive_item(item)

    # print([monkey.inspect_counter for monkey in monkeys.values()])
    print(calculate_monkey_business(monkeys))  # Part 2


print(f"\nSolved in {(perf_counter() - start_time) * 1000:.3g} ms.")
