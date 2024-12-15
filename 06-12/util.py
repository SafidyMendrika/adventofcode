
import regex as re
import time
import copy

def extract_str_data(file_path : str):
    with open(file_path, 'r') as file:
        return file.read()
    

def extract_matrix_data(file_path : str) -> list[str]: 
    input_str = extract_str_data(file_path)

    input_splited = input_str.split('\n')
    matrix = [list(line) for line in input_splited]

    return matrix
def display_matrix(matrix: list[str]):
    print("\n\n")
    for line in matrix:
        print(''.join(line))

def join_matrix(matrix: list[str]):
    result = ""
    for line in matrix:
        result += ''.join(line)

    return result

def find_guard_location(matrix: list[list[str]]) -> tuple[int, int, str]:
    directions = ['>', '^', 'v', '<']
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] in directions:
                return (row, col, matrix[row][col])
    return (-1, -1, '')

def is_present(arr,tuple)-> bool : 
    for element in arr:
        if element[0] == tuple[0] and element[1] == tuple[1]:
            return True
    return False

def solution_one(path : str) -> int:
    input_data = extract_str_data(path)
    lines = input_data.strip().split('\n')
    grid = [list(line) for line in lines]
    copyGrid = copy.deepcopy(grid)
    rows, cols = len(grid), len(grid[0])

    visited_coordinates = set()

    direction_map = {
        '>': [0, 1],
        '^': [-1, 0],
        'v': [1, 0],
        '<': [0, -1]
    }

    turn_around = {
        '>': 'v',
        '^': '>',
        'v': '<',
        '<': '^'
    }

    directions = ['>', '^', 'v', '<']

    # Find the starting guard
    guard = None
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] in directions:
                guard = [grid[row][col], [row, col]]
                break
        if guard:
            break

    visited_coordinates.add(f"{guard[1][0]},{guard[1][1]}")

    is_out = False
    while not is_out:
        current_direction, current_position = guard
        move_position = direction_map[current_direction]
        new_position = [
            current_position[0] + move_position[0],
            current_position[1] + move_position[1]
        ]

        if (new_position[0] < 0 or 
            new_position[1] < 0 or 
            new_position[0] >= rows or 
            new_position[1] >= cols):
            is_out = True
        else:
            cell = grid[new_position[0]][new_position[1]]
            if cell != '#':
                visited_coordinates.add(f"{new_position[0]},{new_position[1]}")
                guard[1] = new_position
            else:
                guard[0] = turn_around[current_direction]

    return len(visited_coordinates)

def solution_two(path : str) -> int:
    input_data = extract_str_data(path)
    lines = input_data.strip().split('\n')
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])

    direction_map = {
        '>': [0, 1],
        '^': [-1, 0],
        'v': [1, 0],
        '<': [0, -1]
    }

    turn_around = {
        '>': 'v',
        '^': '>',
        'v': '<',
        '<': '^'
    }

    directions = ['>', '^', 'v', '<']

    start_guard = None
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] in directions:
                start_guard = [grid[row][col], [row, col]]
                break
        if start_guard:
            break

    def move_guard(guard, current_grid):
        visited = set()
        is_out = False

        while not is_out:
            current_direction, current_position = guard
            move = direction_map[current_direction]
            new_position = [
                current_position[0] + move[0],
                current_position[1] + move[1]
            ]

            if (new_position[0] < 0 or 
                new_position[1] < 0 or 
                new_position[0] >= rows or 
                new_position[1] >= cols):
                is_out = True
                break

            cell = current_grid[new_position[0]][new_position[1]]

            state = f"{new_position[0]},{new_position[1]},{current_direction}"
            if state in visited:
                return True

            visited.add(state)

            if cell != '#':
                guard[1] = new_position
            else:
                guard[0] = turn_around[current_direction]

        return False

    obstruction_count = 0
    for row in range(rows):
        for col in range(cols):
            if (grid[row][col] == '.' and 
                not (row == start_guard[1][0] and col == start_guard[1][1])):
                current_grid = copy.deepcopy(grid)
                current_grid[row][col] = '#'

                if move_guard(start_guard[:], current_grid):
                    obstruction_count += 1

                current_grid[row][col] = '.'

    return obstruction_count