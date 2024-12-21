from dataclasses import dataclass
from typing import List, Set, Tuple, Optional
from collections import deque

@dataclass
class Point:
    y: int
    x: int

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)

@dataclass
class Route:
    points: List[Point]
    score: int

DIRECTIONS = [
    Point(0, 1),   
    Point(-1, 0),  
    Point(0, -1),  
    Point(1, 0)    
]

class PathFinder:
    def __init__(self):
        self.MAX_ROUTES = 1000
        self.INF = float('inf')

    def read_input(self, filename: str) -> Tuple[List[List[str]], Point, Point]:
        grid = []
        start = Point(0, 0)
        end = Point(0, 0)
        
        with open(filename, 'r') as file:
            for y, line in enumerate(file):
                row = list(line.strip())
                grid.append(row)
                for x, cell in enumerate(row):
                    if cell == 'S':
                        start = Point(y, x)
                    elif cell == 'E':
                        end = Point(y, x)
        
        return grid, start, end

    def find_routes(self, grid: List[List[str]], start: Point, end: Point) -> List[Route]:
        height = len(grid)
        width = len(grid[0])
        routes = []
        visited = {}
        
        queue = deque([(start, [start], 0, 0)])
        
        while queue:
            pos, history, curr_score, curr_dir = queue.popleft()
            
            if pos.y == end.y and pos.x == end.x:
                routes.append(Route(points=history.copy(), score=curr_score))
                continue
                
            visit_key = (pos.y, pos.x, curr_dir)
            if visit_key in visited and visited[visit_key] < curr_score:
                continue
            visited[visit_key] = curr_score
            
            for _dir, direction in enumerate(DIRECTIONS):
                if (curr_dir + 2) % 4 == _dir: 
                    continue
                    
                ny = pos.y + direction.y
                nx = pos.x + direction.x
                new_pos = Point(ny, nx)
                
                if (ny < 0 or ny >= height or nx < 0 or nx >= width or 
                    grid[ny][nx] == '#'):
                    continue
                    
                if any(p.y == ny and p.x == nx for p in history):
                    continue
                
                if _dir == curr_dir:  
                    queue.append((new_pos, history + [new_pos], curr_score + 1, _dir))
                else: 
                    queue.append((pos, history, curr_score + 1000, _dir))
        
        return routes

    def solution_one(self, grid: List[List[str]], start: Point, end: Point) -> int:
        routes = self.find_routes(grid, start, end)
        return min(route.score for route in routes) if routes else self.INF

    def solution_two(self, grid: List[List[str]], start: Point, end: Point) -> int:
        routes = self.find_routes(grid, start, end)
        if not routes:
            return 0
            
        min_score = min(route.score for route in routes)
        best_routes = [route for route in routes if route.score == min_score]
        
        unique_tiles = set()
        for route in best_routes:
            for point in route.points:
                unique_tiles.add((point.y, point.x))
                
        return len(unique_tiles)