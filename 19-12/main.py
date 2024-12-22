import util

lines = list(util.get_lines("data.txt"))
towels = set(lines[0].split(", "))
designs = lines[2:]

cache = {}

print("Part 1:", util.solution_one(designs, towels, cache))
print("Part 2:", util.solution_two(designs, towels, cache))