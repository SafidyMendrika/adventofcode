def ways_to_make_design(design, towels, cache):
    if not design:
        return 1  
    
    if design not in cache:
        cache[design] = sum(
            ways_to_make_design(design[len(option):], towels, cache)
            for option in towels
            if design.startswith(option)
        )
    
    return cache[design]

def solution_one(designs, towels, cache):

    return len([1 for design in designs if ways_to_make_design(design, towels, cache) > 0])

def solution_two(designs, towels, cache):

    return sum(ways_to_make_design(design, towels, cache) for design in designs)

def get_lines(path):

    with open(path) as file:
        for ln in file:
            yield ln.strip()