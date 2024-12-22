from util import Solution

if __name__ == "__main__":
    s = Solution(filename='data.txt')
    s.solution_one(bytes_fallen=1024, map_bound=71, start=(0,0), end=(70,70))
    s.solution_two(bytes_fallen=1024, map_bound=71, start=(0,0), end=(70,70))