
import regex as re

def extract_str_data(file_path : str):
    with open(file_path, 'r') as file:
        return file.read()
    

def extract_list_data(file_path : str) -> str:
    file_content = extract_str_data(file_path)

    return file_content


# part 1 - Solution
def solution_one(file_path : str) -> int:
    data = extract_list_data(file_path)

    mul_pattern = r'mul\((\d+),(\d+)\)'

    matches = re.findall(mul_pattern, data)

    result = 0
    for matched_tuple in matches : 
        result += int(matched_tuple[0]) * int(matched_tuple[1])

    return result


# part 2 - Solution
def solution_two(file_path: str) -> int:
    data = extract_list_data(file_path)

    mul_pattern = r'mul\((\d+),(\d+)\)'
    do_pattern = r'do\(\)'
    dont_pattern = r'don\'t\(\)'

    mul_enabled = True
    result = 0

    instructions = re.finditer(r'(mul\(\d+,\d+\)|do\(\)|don\'t\(\))', data)

    for instruction in instructions:
        match = instruction.group(1)
        
        if re.match(do_pattern, match):
            mul_enabled = True
            continue
        
        if re.match(dont_pattern, match):
            mul_enabled = False
            continue
        
        mul_match = re.match(mul_pattern, match)
        if mul_match and mul_enabled:
            x = int(mul_match.group(1))
            y = int(mul_match.group(2))
            result += x * y

    return result
