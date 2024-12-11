
import regex as re

def extract_str_data(file_path : str):
    with open(file_path, 'r') as file:
        return file.read()
    

def extract_list_data(file_path : str) -> list:
    file_content = extract_str_data(file_path)
    result = []
    temp_array = []
    for line in file_content.split('\n'):
        temp_array = [int(x) for x in re.split(r'\s+', line)]
        result.append(temp_array)

    return result

# part 1 - solution
def solution_one(file_path : str) -> list:
    data = extract_list_data(file_path)
    safe_count = 0
    for line in data : 
        if is_monotonic_sequence(line):
            safe_count += 1            
    return safe_count

def is_monotonic_sequence(arr: list) -> bool:
    if len(arr) <= 1:
        return True

    is_increasing = None
    
    for i in range(1, len(arr)):
        current = int(arr[i])
        previous = int(arr[i-1])
        
        if is_increasing is None:
            if current > previous:
                is_increasing = True
            elif current < previous:
                is_increasing = False
        
        if is_increasing:
            if current <= previous or abs(current - previous) > 3:
                return False
        else:
            if current >= previous or abs(current - previous) > 3:
                return False
    return True



# part 2 - solution
def solution_two(file_path: str) -> int:
    data = extract_list_data(file_path)
    safe_count = 0
    for line in data:
        if is_safe_with_problem_dampener(line):
            safe_count += 1
    return safe_count

def is_safe_with_problem_dampener(arr: list) -> bool:
    if is_monotonic_sequence(arr):
        return True
    
    for i in range(len(arr)):
        dampened_arr = arr[:i] + arr[i+1:]
                
        if is_monotonic_sequence(dampened_arr):
            return True
    
    return False

def is_monotonic_sequence(arr: list) -> bool:
    if len(arr) <= 1:
        return True

    is_increasing = None
    
    for i in range(1, len(arr)):
        current = int(arr[i])
        previous = int(arr[i-1])
        
        if is_increasing is None:
            if current > previous:
                is_increasing = True
            elif current < previous:
                is_increasing = False
        
        if is_increasing:
            if current <= previous or abs(current - previous) > 3:
                return False
        else:
            if current >= previous or abs(current - previous) > 3:
                return False
    return True