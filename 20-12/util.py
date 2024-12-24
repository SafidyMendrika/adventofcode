from collections import deque
from typing import List, Tuple, Set
import sys

class RaceCondition:
    
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def __init__(self, filename: str):

        self.grid = self._parse_grid(filename)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.start = self._find_tile('S')
        self.end = self._find_tile('E')
        
        self.base_distances = self._bfs(self.start)
        self.end_distances = self._bfs(self.end)
        self.normal_shortest_path = self.base_distances[self.end[0]][self.end[1]]
    
    def _parse_grid(self, filename: str) -> List[List[str]]:
        try:
            with open(filename, 'r') as f:
                return [list(line.strip()) for line in f if line.strip()]
        except Exception as e:
            raise RuntimeError(f"Failed to read file: {filename}") from e
    
    def _find_tile(self, tile: str) -> Tuple[int, int]:
        for r, row in enumerate(self.grid):
            try:
                c = row.index(tile)
                return r, c
            except ValueError:
                continue
        raise RuntimeError(f"Tile '{tile}' not found")
    
    def _bfs(self, start: Tuple[int, int]) -> List[List[int]]:
        distances = [[sys.maxsize] * self.cols for _ in range(self.rows)]
        queue = deque([start])
        distances[start[0]][start[1]] = 0
        
        while queue:
            r, c = queue.popleft()
            dist = distances[r][c]
            
            for dr, dc in self.DIRECTIONS:
                nr, nc = r + dr, c + dc
                
                if (self._is_valid_pos(nr, nc) and 
                    self._is_track(nr, nc) and 
                    distances[nr][nc] == sys.maxsize):
                    distances[nr][nc] = dist + 1
                    queue.append((nr, nc))
        
        return distances
    
    def _is_valid_pos(self, r: int, c: int) -> bool:

        return 0 <= r < self.rows and 0 <= c < self.cols
    
    def _is_track(self, r: int, c: int) -> bool:

        return self.grid[r][c] != '#'
    
    def _process_cheats(self, max_steps: int) -> int:

        unique_cheats = set()
        cheats_over_100 = 0
        
        for r in range(self.rows):
            for c in range(self.cols):
                if not self._is_track(r, c) or self.base_distances[r][c] == sys.maxsize:
                    continue
                    
                for er in range(max(0, r - max_steps), min(self.rows, r + max_steps + 1)):
                    for ec in range(max(0, c - max_steps), min(self.cols, c + max_steps + 1)):
                        if not self._is_track(er, ec) or self.end_distances[er][ec] == sys.maxsize:
                            continue
                            
                        cheat_dist = abs(er - r) + abs(ec - c)
                        if cheat_dist > max_steps:
                            continue
                            
                        total_path = self.base_distances[r][c] + cheat_dist + self.end_distances[er][ec]
                        time_saved = self.normal_shortest_path - total_path
                        
                        cheat_key = f"{r},{c}:{er},{ec}"
                        if time_saved >= 100 and cheat_key not in unique_cheats:
                            unique_cheats.add(cheat_key)
                            cheats_over_100 += 1
        
        return cheats_over_100
    
    def solution_one(self) -> int:

        return self._process_cheats(2)
    
    def solution_two(self) -> int:

        return self._process_cheats(20)