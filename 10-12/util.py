
import regex as re
import time
import copy
from itertools import product
from dataclasses import dataclass


def extract_str_data(file_path : str) -> str:
    with open(file_path, 'r') as file:
        return file.read().strip()
    


def get_grid(lines: list[str]) -> list[list[int]]:
    return [[int(char) for char in line] for line in lines]

def get_starting_points(grid: list[list[int]]) -> list[tuple[int, int]]:
    return [
        (row, col) 
        for row in range(len(grid)) 
        for col in range(len(grid[row])) 
        if grid[row][col] == 0
    ]

def calculate_trailhead_score(grid: list[list[int]], start: tuple[int, int]) -> int:
    rows, cols = len(grid), len(grid[0])
    
    def is_valid_move(current_row: int, current_col: int, next_row: int, next_col: int) -> bool:
        return (
            0 <= next_row < rows and 
            0 <= next_col < cols and
            grid[next_row][next_col] == grid[current_row][current_col] + 1
        )
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    reachable_peaks = set()
    visited = set([(start[0], start[1], 0)])
    queue = [(start[0], start[1], 0)]
    
    while queue:
        current_row, current_col, current_height = queue.pop(0)
        
        if grid[current_row][current_col] == 9:
            reachable_peaks.add((current_row, current_col))
        
        for dx, dy in directions:
            next_row, next_col = current_row + dx, current_col + dy
            
            if (
                is_valid_move(current_row, current_col, next_row, next_col) and
                (next_row, next_col, grid[next_row][next_col]) not in visited
            ):
                new_height = grid[next_row][next_col]
                queue.append((next_row, next_col, new_height))
                visited.add((next_row, next_col, new_height))
    
    return len(reachable_peaks)

def solution_one(path: str) -> int:
    input_data = extract_str_data(path)
    lines = input_data.strip().split('\n')
    
    grid = get_grid(lines)
    
    starting_points = get_starting_points(grid)
    
    total_score = sum(
        calculate_trailhead_score(grid, start) 
        for start in starting_points
    )
    
    return total_score


def calculate_unique_trails(grid: list[list[int]], point: tuple[int, int]) -> int:
    rows, cols = len(grid), len(grid[0])
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def is_valid_move(current_row: int, current_col: int, next_row: int, next_col: int) -> bool:
        return (
            0 <= next_row < rows and 
            0 <= next_col < cols and
            grid[next_row][next_col] == grid[current_row][current_col] + 1
        )
    
    distinct_trails = set()
    
    queue = [(point[0], point[1], f"{point[0]},{point[1]}")]
    
    while queue:
        current_row, current_col, current_trail = queue.pop()
        
        if grid[current_row][current_col] == 9:
            distinct_trails.add(current_trail)
            continue
        
        for dx, dy in directions:
            next_row, next_col = current_row + dx, current_col + dy
            
            if is_valid_move(current_row, current_col, next_row, next_col):
                new_trail = f"{current_trail}->{next_row},{next_col}"
                queue.append((next_row, next_col, new_trail))
    
    return len(distinct_trails)

def solution_two(path: str) -> int:
    input_data = extract_str_data(path)
    lines = input_data.split('\n')
    
    grid = get_grid(lines)
    
    starting_points = get_starting_points(grid)
    
    score = sum(
        calculate_unique_trails(grid, point) 
        for point in starting_points
    )
    
    return score