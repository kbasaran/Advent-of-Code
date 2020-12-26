from pathlib import Path
import time
from dataclasses import dataclass

start1 = time.time()

@dataclass
class Food:
    ingredients: list
    allergens: list

@dataclass
class Allergen:
    food_ings: list
    possibly_in: set = None
    definitely_in: str = None


def read_input(file_name="input.txt"):
    """Make a food dictionary from input data."""
    P_IN = Path.cwd().joinpath(file_name).read_text()
    global foods
    foods = {}
    for i, food_line in enumerate(P_IN.splitlines()):
        ingredients, allergens = food_line.split(" (contains ")
        ingredients = ingredients.split(" ")
        allergens = allergens.strip(")").split(", ")
        foods[i] = Food(ingredients, allergens)


read_input()

allergens = {}
for food in foods.values():
    for allergen in food.allergens:
        if allergen not in allergens.keys():
            allergens[allergen] = Allergen([food.ingredients])
        else:
            allergens[allergen].food_ings.append(food.ingredients)


# Find the ingredients which were always in the ingredient list when
# a certain allergen was mentioned
for allergen in allergens.values():
    allergen.possibly_in = set.intersection(*[set(food_ing) for food_ing in allergen.food_ings])
    # print(allergen)


def remove_from_possibles(ingredient):
    """
    Remove an ingredient from being a possible container for an allergen.

    Use this when you figure out exactly which allergen is in an ingredient.
    """
    global allergens
    for allergen in allergens.values():
        if ingredient in allergen.possibly_in:
            allergen.possibly_in.remove(ingredient)


# Iterate through the allergens and if they can possibly be found in only one ingredient,
# set the "definitely_in attribute, and remove that ingredient from
# being a possible container for all the other allergens
for _ in range(99):
    for allergen in allergens.values():
        if len(allergen.possibly_in) == 1:
            ingredient_it_is_in = list(allergen.possibly_in)[0]
            allergen.definitely_in = ingredient_it_is_in
            remove_from_possibles(ingredient_it_is_in)

appearance_count = 0
ingredients_with_known_allergens = [allergen.definitely_in for allergen in allergens.values()]
for food in foods.values():
    for ingredient in food.ingredients:
        appearance_count += (ingredient not in ingredients_with_known_allergens)

print(appearance_count)

print(f"Elapsed time: {time.time() - start1:.4g}s")

# %% Part 2
allergen_names = sorted(allergens.keys())
canonical_list = [allergens[allergen_name].definitely_in for allergen_name in allergen_names]
canonical_list_str = ",".join(canonical_list)

print(canonical_list_str)
