from util import PathFinder

finder = PathFinder()
grid, start, end = finder.read_input("data.txt")

print(f"Part 1: {finder.solution_one(grid, start, end)}")
print(f"Part 2: {finder.solution_two(grid, start, end)}")