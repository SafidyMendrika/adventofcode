
import regex as re

def extract_str_data(file_path : str):
    with open(file_path, 'r') as file:
        return file.read()
    

def extract_list_data(file_path : str) -> list:
    file_content = extract_str_data(file_path)
    result = [list(line) for line in file_content.split('\n')]
    return result

# Part 1 - Solution
def solution_one(path : str) -> int:
    grid = extract_list_data(path)
    rows, cols = len(grid), len(grid[0])
    target = 'XMAS'
    directions = [
        (0, 1),  
        (0, -1),  
        (1, 0),   
        (-1, 0),  
        (1, 1),   
        (1, -1),  
        (-1, 1), 
        (-1, -1)  
    ]
    
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols
    
    def check_direction(start_x, start_y, dx, dy):
        x, y = start_x, start_y
        for letter in target:
            if not is_valid(x, y) or grid[x][y] != letter:
                return False
            x += dx
            y += dy
        return True
    
    count = 0
    for x in range(rows):
        for y in range(cols):
            for dx, dy in directions:
                if check_direction(x, y, dx, dy):
                    count += 1
    
    return count