from itertools import product

def projection_combos_of_each_chunk(chunks, amounts):
    # in which chunks to add these new splits into
    n_missing_split_points = len(amounts) - len(chunks)
    projections = []


    if n_missing_split_points > 0:
        expansion_per_input_chunk_combos = [x for x in product(range(n_missing_split_points + 1), repeat=len(chunks)) if sum(x) == n_missing_split_points]
        # addition_combos = np.ones(((n_missing_split_points + 1)**len(chunks), len(chunks)), dtype=int)
        for combo in expansion_per_input_chunk_combos:
            end_points = 
            index_chunk = 0
            for chunk, expansion in zip(chunks, combo):
                chunk_range = expansion
                projections.append((chunk, (index_chunk, index_chunk + )))
                # print(combo)


    if n_missing_split_points < 0:
        gen = (x for x in product(range(-n_missing_split_points + 3), repeat=len(amounts)) if sum(x) == - n_missing_split_points)
        # addition_combos = np.ones(((n_missing_split_points + 1)**len(chunks), len(chunks)), dtype=int)
        for combo in gen:
            print(combo)


    return projections
            

print(projection_combos_of_each_chunk(((2, 4), (7,12)), (1,3,5)))            
print(projection_combos_of_each_chunk(((2, 4), (7,12), (15,19), (23,27)), (1,3,5)))
